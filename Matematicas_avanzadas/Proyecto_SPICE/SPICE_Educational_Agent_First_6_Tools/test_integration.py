#!/usr/bin/env python3
"""Integration smoke test for the first six tools.

Author: Dr. Francisco E. Rangel-Patiño
"""
import json
import tempfile
from pathlib import Path

from parse_netlist import parse_netlist_file
from build_circuit_model import build_circuit, circuit_to_dict
from build_oriented_graph import build_graph
from build_incidence_matrix import build_incidence_matrices
from build_nodal_system import build_nodal_system
from solve_linear_system import solve_nodal_system


def main() -> None:
    base = Path(__file__).parent
    parsed = parse_netlist_file(base / "examples/current_source_resistive.cir")
    circuit = build_circuit(parsed)
    graph = build_graph(circuit)
    assert graph.number_of_edges() == 4
    incidence = build_incidence_matrices(circuit)
    system = build_nodal_system(circuit, incidence)
    result = solve_nodal_system(system, circuit)
    values = {x["label"]: x["real"] for x in result["node_voltages"]}
    # Analytical solution: V1=750 mV, V2=250 mV.
    assert abs(values["V(N1)"] - 0.75) < 1e-10
    assert abs(values["V(N2)"] - 0.25) < 1e-10
    assert result["status"] == "PASS"
    print(json.dumps({"status": "PASS", "node_voltages": values}, indent=2))


if __name__ == "__main__":
    main()
