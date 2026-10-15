"""Regression tests for the constitutive, Tableau, AC, and reporting tools."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from build_circuit_model import build_circuit, circuit_to_dict
from build_constitutive_matrices import build_constitutive_matrices
from build_incidence_matrix import build_incidence_matrices
from build_nodal_system import build_nodal_system
from build_oriented_graph import build_graph, graph_to_dict
from build_tableau_system import build_tableau_system
from compare_reference import ReferenceComparisonError, compare_reference
from generate_report import ReportGenerationError, generate_report
from parse_netlist import parse_netlist_text
from plot_results import plot_results
from solve_ac_sweep import generate_frequencies, solve_ac_sweep
from solve_linear_system import LinearSystemError, solve_matrix_system, solve_nodal_system
from validate_solution import validate_solution


def make_circuit(text: str, source_name: str = "<test>"):
    circuit = build_circuit(parse_netlist_text(text, source_name))
    return circuit, build_incidence_matrices(circuit)


class ExtendedToolsTests(unittest.TestCase):
    def test_constitutive_models_cover_dc_and_ac_sources(self) -> None:
        text = "\n".join(
            [
                "R1 1 0 1k",
                "G1 1 0 1m",
                "C1 1 0 1u",
                "L1 1 0 1m",
                "V1 1 0 DC 10",
                "I1 1 0 AC 2m 90",
                ".END",
            ]
        )
        circuit, _ = make_circuit(text)
        dc = build_constitutive_matrices(circuit)
        ac = build_constitutive_matrices(circuit, 1000.0)
        self.assertEqual(dc["shape"], [6, 6])
        self.assertAlmostEqual(dc["Y"][0][0]["real"], 1.0)
        self.assertAlmostEqual(dc["Z"][1][1]["real"], -1.0)
        self.assertEqual(dc["Z"][2][2], {"real": 1.0, "imag": 0.0})
        self.assertEqual(dc["Y"][3][3], {"real": 1.0, "imag": 0.0})
        self.assertEqual(dc["W"][4], {"real": 10.0, "imag": 0.0})
        self.assertEqual(dc["W"][5], {"real": 0.0, "imag": 0.0})
        self.assertAlmostEqual(ac["Y"][2][2]["imag"], 2 * np.pi * 1000 * 1e-6)
        self.assertAlmostEqual(ac["Z"][3][3]["imag"], -2 * np.pi * 1000 * 1e-3)
        self.assertEqual(ac["W"][4], {"real": 0.0, "imag": 0.0})
        self.assertAlmostEqual(ac["W"][5]["real"], 0.0, delta=1e-12)
        self.assertAlmostEqual(ac["W"][5]["imag"], 2e-3)

    def test_tableau_solves_voltage_source_divider(self) -> None:
        text = "\n".join(["V1 1 0 DC 10", "R1 1 2 1k", "R2 2 0 2k", ".END"])
        circuit, incidence = make_circuit(text, "divider.cir")
        constitutive = build_constitutive_matrices(circuit)
        tableau = build_tableau_system(circuit, incidence, constitutive)
        solution = solve_matrix_system(tableau)
        values = {item["label"]: item["real"] for item in solution["unknowns"]}
        self.assertEqual(tableau["shape"], [8, 8])
        self.assertAlmostEqual(values["V(N2)"], 20 / 3)
        self.assertEqual(validate_solution(tableau, solution)["status"], "PASS")

    def test_nodal_source_semantics_and_order_guard(self) -> None:
        circuit, incidence = make_circuit(
            "\n".join(["I1 0 1 DC 2m", "R1 1 0 1k", ".END"])
        )
        ac_system = build_nodal_system(circuit, incidence, 1000.0)
        self.assertTrue(all(value["real"] == 0 and value["imag"] == 0 for value in ac_system["rhs"]))
        dc_system = build_nodal_system(circuit, incidence)
        result = solve_nodal_system(dc_system, circuit)
        self.assertAlmostEqual(result["node_voltages"][0]["real"], 2.0)
        reordered = circuit.__class__(
            **{**circuit.__dict__, "branches": list(reversed(circuit.branches))}
        )
        with self.assertRaises(LinearSystemError):
            solve_nodal_system(dc_system, reordered)

    def test_frequency_generation_and_rc_sweep(self) -> None:
        self.assertEqual(generate_frequencies("LIN", 3, 10, 30), [10.0, 20.0, 30.0])
        decade = generate_frequencies("DEC", 10, 10, 100000)
        self.assertEqual(len(decade), 41)
        self.assertEqual((decade[0], decade[-1]), (10, 100000))
        with self.assertRaises(ValueError):
            generate_frequencies("LIN", 2, 0, 10)

        example = Path(__file__).parent / "examples" / "rc_ac.cir"
        from parse_netlist import parse_netlist_file

        circuit = build_circuit(parse_netlist_file(example))
        incidence = build_incidence_matrices(circuit)
        sweep = next(item for item in circuit.directives if item["command"] == "AC")
        result = solve_ac_sweep(
            circuit,
            incidence,
            sweep,
            "NODAL",
            {"Zin": {"numerator": "V(N1)", "denominator": "B1 (I1)"}},
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(result["points"]), 41)
        self.assertTrue(all(point["validation"]["status"] == "PASS" for point in result["points"]))

    def test_reference_comparison_checks_values_units_and_frequency(self) -> None:
        actual = {
            "analysis": "DC",
            "node_voltages": [{"label": "V(N2)", "real": 5.0, "imag": 0.0, "unit": "volt"}],
        }
        reference = {"variables": {"V(N2)": {"real": 5.0, "imag": 0.0, "unit": "volt"}}}
        self.assertEqual(compare_reference(actual, reference)["status"], "PASS")
        wrong_unit = {"variables": {"V(N2)": {"real": 5.0, "imag": 0.0, "unit": "ampere"}}}
        self.assertEqual(compare_reference(actual, wrong_unit)["status"], "FAIL")

        ac_actual = {
            "analysis": "AC",
            "points": [{
                "frequency_hz": 100.0,
                "transfer_functions": {"H": {"real": 1.0, "imag": 0.0, "magnitude": 1.0}},
            }],
        }
        ac_reference = {
            "points": [{
                "frequency_hz": 100.0,
                "variables": {"H": {"real": 1.0, "imag": 0.0, "unit": "ratio"}},
            }]
        }
        self.assertEqual(compare_reference(ac_actual, ac_reference)["status"], "PASS")
        misaligned = {"points": [{"frequency_hz": 200.0, "variables": {"H": 1.0}}]}
        with self.assertRaises(ReferenceComparisonError):
            compare_reference(ac_actual, misaligned)

    def test_report_uses_validated_bundle_and_rejects_mixed_runs(self) -> None:
        text = "\n".join(["V1 1 0 DC 10", "R1 1 2 1k", "R2 2 0 2k", ".END"])
        circuit, incidence = make_circuit(text, "divider.cir")
        constitutive = build_constitutive_matrices(circuit)
        system = build_tableau_system(circuit, incidence, constitutive)
        solution = solve_matrix_system(system)
        validation = validate_solution(system, solution)
        bundle = {
            "run_id": "run-1",
            "source_name": "divider.cir",
            "netlist_text": text,
            "circuit": circuit_to_dict(circuit),
            "incidence": incidence,
            "constitutive": constitutive,
            "system": system,
            "solution": solution,
            "validation": validation,
        }
        report = generate_report(bundle)
        self.assertIn("## Matriz de incidencia reducida", report)
        self.assertIn("## Validación", report)
        self.assertIn("V(N2)", report)
        mixed = {**bundle, "system": {**system, "run_id": "run-2"}}
        with self.assertRaises(ReportGenerationError):
            generate_report(mixed)

    def test_plot_results_writes_topology_and_bode_files(self) -> None:
        from parse_netlist import parse_netlist_file

        base = Path(__file__).parent
        dc_circuit = build_circuit(parse_netlist_file(base / "examples" / "current_source_resistive.cir"))
        topology = graph_to_dict(build_graph(dc_circuit), dc_circuit)
        ac_circuit = build_circuit(parse_netlist_file(base / "examples" / "rc_ac.cir"))
        incidence = build_incidence_matrices(ac_circuit)
        sweep = next(item for item in ac_circuit.directives if item["command"] == "AC")
        results = solve_ac_sweep(
            ac_circuit,
            incidence,
            sweep,
            "NODAL",
            {"Zin": {"numerator": "V(N1)", "denominator": "B1 (I1)"}},
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            files = plot_results(results, temp_dir, topology)
            self.assertEqual(len(files), 3)
            self.assertTrue(all(Path(path).is_file() and Path(path).stat().st_size > 0 for path in files))


if __name__ == "__main__":
    unittest.main()