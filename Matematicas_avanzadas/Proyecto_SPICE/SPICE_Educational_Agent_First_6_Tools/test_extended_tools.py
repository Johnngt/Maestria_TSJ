"""Regression tests for the constitutive, Tableau, AC, and reporting tools."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from build_circuit_model import build_circuit, circuit_to_dict
from build_constitutive_matrices import build_constitutive_matrices
from build_incidence_matrix import build_incidence_matrices
from build_nodal_system import NodalCompatibilityError, build_nodal_system
from build_mna_system import MNAAssemblyError, build_mna_system
from build_oriented_graph import build_graph, graph_to_dict
from build_tableau_system import TableauAssemblyError, build_tableau_system
from compare_reference import ReferenceComparisonError, compare_reference
from generate_report import ReportGenerationError, _align_markdown_tables, generate_report
from parse_netlist import parse_netlist_text
from plot_results import plot_results
from solve_ac_sweep import generate_frequencies, solve_ac_sweep
from solve_linear_system import (
    LinearSystemError,
    solve_matrix_system,
    solve_mna_system,
    solve_nodal_system,
)
from stamp_elements import StampError, constitutive_stamp, nodal_stamp
from validate_solution import validate_solution
from validate_netlist import validate_netlist_text


def make_circuit(text: str, source_name: str = "<test>"):
    circuit = build_circuit(parse_netlist_text(text, source_name))
    return circuit, build_incidence_matrices(circuit)


class ExtendedToolsTests(unittest.TestCase):
    def test_netlist_validation_collects_circuit_diagnostics(self) -> None:
        report = validate_netlist_text(
            "\n".join(
                [
                    "R1 1 2 1k",
                    "R1 2 3 2k",
                    "I1 3 4 AC 1m nan",
                    ".AC LIN 3 1 10",
                    ".AC DEC 10 1 100",
                    ".END",
                ]
            ),
            "invalid.cir",
        )
        self.assertEqual(report["status"], "FAIL")
        codes = {item["code"] for item in report["diagnostics"]}
        self.assertTrue(
            {
                "DUPLICATE_COMPONENT",
                "INVALID_AC_PHASE",
                "MISSING_REFERENCE_NODE",
                "MULTIPLE_AC_DIRECTIVES",
            }.issubset(codes)
        )

        valid = validate_netlist_text("R1 1 0 1k", "valid.cir")
        self.assertEqual(valid["status"], "PASS")
        self.assertEqual(valid["diagnostics"][0]["code"], "MISSING_END_DIRECTIVE")

    def test_netlist_parser_enforces_validation_and_allows_zero_conductance(self) -> None:
        with self.assertRaisesRegex(ValueError, "Netlist validation failed"):
            parse_netlist_text("R1 1 2 1k\n.END", "missing-ground.cir")
        circuit, _ = make_circuit("G1 1 0 0\nR1 1 0 1k\n.END")
        self.assertEqual(circuit.branches[0].value_si, 0)
        self.assertEqual(nodal_stamp(circuit.branches[0]).admittance, 0j)

    def test_shared_component_stamps_agree_between_tableau_and_nodal(self) -> None:
        circuit, _ = make_circuit(
            "\n".join(
                [
                    "R1 1 0 1k",
                    "G1 1 0 1m",
                    "C1 1 0 1u",
                    "L1 1 0 1m",
                    "I1 0 1 AC 2m 90",
                    ".END",
                ]
            )
        )
        frequency = 1000.0
        for branch in circuit.branches[:4]:
            constitutive = constitutive_stamp(branch, frequency)
            nodal = nodal_stamp(branch, frequency)
            self.assertAlmostEqual(
                nodal.admittance,
                -constitutive.y / constitutive.z,
            )
        source = nodal_stamp(circuit.branches[4], frequency)
        source_model = constitutive_stamp(circuit.branches[4], frequency)
        self.assertIsNone(source.admittance)
        self.assertAlmostEqual(source.current, source_model.w / source_model.z)
        with self.assertRaises(StampError):
            nodal_stamp(circuit.branches[3])

    def test_mna_ideal_opamp_non_inverting_gain_and_validation(self) -> None:
        circuit, incidence = make_circuit(
            "\n".join(
                [
                    "V1 NP 0 AC 20 0",
                    "RA NM 0 10k",
                    "RB OUT NM 10k",
                    ".OPAMP U1 NP NM OUT IDEAL",
                    ".AC LIN 1 1k 1k",
                    ".END",
                ]
            ),
            "non_inverting.cir",
        )
        self.assertEqual(len(circuit.opamps), 1)
        self.assertIn("OUT", [node.id for node in circuit.nodes])
        system = build_mna_system(circuit, incidence, 1000.0)
        solution = solve_mna_system(system, circuit)
        validation = validate_solution(system, solution)
        values = {item["label"]: complex(item["real"], item["imag"]) for item in solution["unknowns"]}
        self.assertAlmostEqual(values["V(NOUT)"], 40.0 + 0.0j, places=10)
        self.assertAlmostEqual(values["V(NNP)"], 20.0 + 0.0j, places=10)
        self.assertEqual(validation["status"], "PASS")
        checks = {item["name"]: item["passed"] for item in validation["checks"]}
        self.assertTrue(checks["KCL"])
        self.assertTrue(checks["voltage_source_constraints"])
        self.assertTrue(checks["opamp_differential_constraint"])
        with self.assertRaises(NodalCompatibilityError):
            build_nodal_system(circuit, incidence, 1000.0)
        with self.assertRaises(TableauAssemblyError):
            build_tableau_system(
                circuit,
                incidence,
                build_constitutive_matrices(circuit, 1000.0),
            )

    def test_mna_active_filter_ac_sweep_validates_every_point(self) -> None:
        text = "\n".join(
            [
                "V1 IN 0 AC 20 0",
                "C1 IN N1 10n",
                "C2 N1 NP 10n",
                "G1 N1 OUT 100u",
                "G2 NP 0 100u",
                "RA NM 0 10k",
                "RB OUT NM 10k",
                ".OPAMP U1 NP NM OUT IDEAL",
                ".AC DEC 10 1 1Meg",
                ".END",
            ]
        )
        circuit, incidence = make_circuit(text, "active_filter.cir")
        sweep = next(item for item in circuit.directives if item["command"] == "AC")
        result = solve_ac_sweep(
            circuit,
            incidence,
            sweep,
            "MNA",
            {"H": {"numerator": "V(NOUT)", "denominator": "V(NIN)"}},
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["sweep"]["frequency_count"], 61)
        self.assertTrue(all(point["status"] == "PASS" for point in result["points"]))
        self.assertTrue(
            all(point["validation"]["status"] == "PASS" for point in result["points"])
        )
        self.assertEqual(result["points"][0]["transfer_functions"]["H"]["status"], "PASS")
        self.assertGreater(
            result["points"][-1]["transfer_functions"]["H"]["magnitude"], 1.99
        )

    def test_opamp_netlist_diagnostics_reject_bad_model_and_duplicate_name(self) -> None:
        invalid_model = validate_netlist_text(
            "V1 NP 0 AC 1\n.OPAMP U1 NP NM OUT GENERIC\n.END"
        )
        self.assertEqual(invalid_model["status"], "FAIL")
        self.assertIn("INVALID_DIRECTIVE", {item["code"] for item in invalid_model["diagnostics"]})

        duplicate = validate_netlist_text(
            "R1 NP 0 1k\n.OPAMP R1 NP NM OUT IDEAL\n.END"
        )
        self.assertEqual(duplicate["status"], "FAIL")
        self.assertIn("DUPLICATE_COMPONENT", {item["code"] for item in duplicate["diagnostics"]})

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

    def test_report_aligns_markdown_table_columns(self) -> None:
        lines = [
            "| Nodo | Valor complejo |",
            "|---|---:|",
            "| N1 | 1 + j2 |",
            "| Nodo_largo | -0.003 |",
        ]
        aligned = _align_markdown_tables(lines)
        self.assertEqual(len({len(line) for line in aligned}), 1)
        self.assertIn(":", aligned[1])

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

    def test_report_includes_ac_node_voltage_vector_per_frequency(self) -> None:
        bundle = {
            "source_name": "ac.cir",
            "ac_sweep": {
                "status": "PASS",
                "formulation": "MNA",
                "sweep": {"type": "DEC", "frequency_count": 1},
                "points": [
                    {
                        "frequency_hz": 10.0,
                        "status": "PASS",
                        "solution": {
                            "node_voltages": [
                                {"label": "V(NIN)", "real": 0.001, "imag": 0.0, "unit": "volt"},
                                {"label": "V(NOUT)", "real": 0.002, "imag": -0.001, "unit": "volt"},
                            ]
                        },
                        "transfer_functions": {
                            "Vo_Vi": {"magnitude": 2.236, "phase_deg": -26.565, "magnitude_db": 6.99}
                        },
                    }
                ],
            },
        }
        report = generate_report(bundle)
        self.assertIn("### Vector de voltajes nodales Vn por frecuencia", report)
        self.assertIn("V(NIN) (V)", report)
        self.assertIn("V(NOUT) (V)", report)
        self.assertIn("0.002 - j0.001", report)

    def test_report_describes_ideal_opamp_mna_and_terminals(self) -> None:
        text = "\n".join(
            [
                "V1 NP 0 AC 20 0",
                "RA NM 0 10k",
                "RB OUT NM 10k",
                ".OPAMP U1 NP NM OUT IDEAL",
                ".AC LIN 1 1k 1k",
                ".END",
            ]
        )
        circuit, incidence = make_circuit(text, "non_inverting.cir")
        system = build_mna_system(circuit, incidence, 1000.0)
        solution = solve_mna_system(system, circuit)
        validation = validate_solution(system, solution)
        bundle = {
            "source_name": "non_inverting.cir",
            "netlist_text": text,
            "circuit": circuit_to_dict(circuit),
            "system": system,
            "solution": solution,
            "validation": validation,
        }
        report = generate_report(bundle)
        self.assertIn("## Amplificadores operacionales ideales", report)
        self.assertIn("V(n+)=V(n-)", report)
        self.assertIn("| U1     | NP        | NM        | OUT    |", report)

    def test_oriented_graph_preserves_multiterminal_opamp_metadata(self) -> None:
        circuit, _ = make_circuit(
            "\n".join(
                [
                    "V1 NP 0 AC 1",
                    "RA NM 0 10k",
                    "RB OUT NM 10k",
                    ".OPAMP U1 NP NM OUT IDEAL",
                    ".END",
                ]
            )
        )
        topology = graph_to_dict(build_graph(circuit), circuit)
        self.assertEqual(
            topology["opamps"],
            [{"name": "U1", "node_plus": "NP", "node_minus": "NM", "node_out": "OUT", "model": "IDEAL", "line_number": 4}],
        )

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