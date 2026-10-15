#!/usr/bin/env python3
"""Assemble the Tableau system from incidence and constitutive matrices."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from build_circuit_model import Circuit, load_circuit
from build_constitutive_matrices import (
    complex_matrix_to_json,
    complex_to_json,
    complex_vector_to_json,
)


class TableauAssemblyError(ValueError):
    """Raised when Tableau inputs have incompatible dimensions or ordering."""


def build_tableau_system(
    circuit: Circuit,
    incidence_data: dict[str, Any],
    constitutive_data: dict[str, Any],
) -> dict[str, Any]:
    """Build T*X=Wp using X=[Vb; I; Vn]."""
    branch_order = [branch.id for branch in circuit.branches]
    if incidence_data.get("branch_order") != branch_order:
        raise TableauAssemblyError("Incidence branch order does not match circuit branch order")
    if constitutive_data.get("branch_order") != branch_order:
        raise TableauAssemblyError("Constitutive branch order does not match circuit branch order")
    node_order = incidence_data.get("node_order_reduced", [])
    if node_order != [node.id for node in circuit.nodes if not node.is_reference]:
        raise TableauAssemblyError("Reduced node order does not match circuit node order")

    branch_count = len(branch_order)
    node_count = len(node_order)
    a = np.asarray(incidence_data.get("A_reduced"), dtype=float)
    y = np.asarray(
        [[complex(item["real"], item["imag"]) for item in row]
         for row in constitutive_data.get("Y", [])],
        dtype=complex,
    )
    z = np.asarray(
        [[complex(item["real"], item["imag"]) for item in row]
         for row in constitutive_data.get("Z", [])],
        dtype=complex,
    )
    w = np.asarray(
        [complex(item["real"], item["imag"]) for item in constitutive_data.get("W", [])],
        dtype=complex,
    )
    if a.shape != (node_count, branch_count):
        raise TableauAssemblyError("Reduced incidence matrix has incorrect dimensions")
    if y.shape != (branch_count, branch_count) or z.shape != (branch_count, branch_count):
        raise TableauAssemblyError("Y and Z must both have shape (branch_count, branch_count)")
    if w.shape != (branch_count,):
        raise TableauAssemblyError("W must have one entry per branch")

    identity = np.eye(branch_count, dtype=complex)
    zero_bb = np.zeros((branch_count, branch_count), dtype=complex)
    zero_bn = np.zeros((branch_count, node_count), dtype=complex)
    zero_nb = np.zeros((node_count, branch_count), dtype=complex)
    zero_nn = np.zeros((node_count, node_count), dtype=complex)
    matrix = np.block(
        [
            [identity, zero_bb, -a.T],
            [y, z, zero_bn],
            [zero_nb, a, zero_nn],
        ]
    )
    rhs = np.concatenate(
        [np.zeros(branch_count, dtype=complex), w, np.zeros(node_count, dtype=complex)]
    )
    dimension = 2 * branch_count + node_count
    if matrix.shape != (dimension, dimension) or rhs.shape != (dimension,):
        raise TableauAssemblyError("Assembled Tableau dimensions are inconsistent")

    unknown_order = (
        [f"V({branch_id})" for branch_id in branch_order]
        + [f"I({branch_id})" for branch_id in branch_order]
        + [f"V(N{node_id})" for node_id in node_order]
    )
    equation_order = (
        [f"KVL({branch_id})" for branch_id in branch_order]
        + [f"CONSTITUTIVE({branch_id})" for branch_id in branch_order]
        + [f"KCL(N{node_id})" for node_id in node_order]
    )
    return {
        "schema_version": "1.0",
        "source_name": circuit.source_name,
        "analysis": constitutive_data.get("analysis"),
        "frequency_hz": constitutive_data.get("frequency_hz"),
        "formulation": "TABLEAU",
        "M": complex_matrix_to_json(matrix),
        "T": complex_matrix_to_json(matrix),
        "rhs": complex_vector_to_json(rhs),
        "Wp": complex_vector_to_json(rhs),
        "unknown_order": unknown_order,
        "equation_order": equation_order,
        "branch_order": branch_order,
        "node_order": node_order,
        "Y": constitutive_data["Y"],
        "Z": constitutive_data["Z"],
        "W": constitutive_data["W"],
        "A_reduced": incidence_data["A_reduced"],
        "unknown_blocks": {
            "Vb": [0, branch_count],
            "I": [branch_count, 2 * branch_count],
            "Vn": [2 * branch_count, dimension],
        },
        "equation_blocks": {
            "KVL": [0, branch_count],
            "constitutive": [branch_count, 2 * branch_count],
            "KCL": [2 * branch_count, dimension],
        },
        "shape": list(matrix.shape),
        "convention": "X=[Vb; I; Vn], T*X=Wp",
    }


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Tableau linear system")
    parser.add_argument("circuit_json")
    parser.add_argument("incidence_json")
    parser.add_argument("constitutive_json")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    circuit = load_circuit(args.circuit_json)
    data = build_tableau_system(
        circuit, load_json(args.incidence_json), load_json(args.constitutive_json)
    )
    Path(args.output).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Built Tableau system {tuple(data['shape'])} -> {args.output}")


if __name__ == "__main__":
    main()