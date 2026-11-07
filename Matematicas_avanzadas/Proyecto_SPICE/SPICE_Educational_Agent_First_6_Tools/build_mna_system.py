#!/usr/bin/env python3
"""Assemble an MNA system with ideal op-amp nullor constraints."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from build_circuit_model import Circuit, load_circuit
from stamp_elements import StampError, constitutive_stamp, nodal_stamp


class MNAAssemblyError(ValueError):
    """Raised when circuit data cannot be assembled into an MNA system."""


def _complex_json(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def _matrix_json(matrix: np.ndarray) -> list[list[dict[str, float]]]:
    return [[_complex_json(complex(value)) for value in row] for row in matrix]


def _vector_json(vector: np.ndarray) -> list[dict[str, float]]:
    return [_complex_json(complex(value)) for value in vector.reshape(-1)]


def build_mna_system(
    circuit: Circuit,
    incidence_data: dict[str, Any],
    frequency_hz: float | None = None,
) -> dict[str, Any]:
    """Build M*x=b for nodal voltages, ideal-source currents, and op-amp currents.

    KCL uses outgoing currents. Each op-amp has zero input current,
    V(node_plus)-V(node_minus)=0, and an unconstrained output-current unknown.
    """
    if frequency_hz is not None and (
        not math.isfinite(frequency_hz) or frequency_hz <= 0
    ):
        raise MNAAssemblyError("MNA AC frequency must be finite and positive")
    branches = circuit.branches
    opamps = circuit.opamps
    branch_order = [branch.id for branch in branches]
    node_order = [node.id for node in circuit.nodes if not node.is_reference]
    if incidence_data.get("branch_order") != branch_order:
        raise MNAAssemblyError("Incidence branch order does not match circuit branch order")
    if incidence_data.get("node_order_reduced") != node_order:
        raise MNAAssemblyError("Reduced node order does not match circuit node order")

    a = np.asarray(incidence_data.get("A_reduced"), dtype=float)
    branch_count = len(branches)
    node_count = len(node_order)
    if a.shape != (node_count, branch_count):
        raise MNAAssemblyError("Reduced incidence matrix has incorrect dimensions")
    if not np.all(np.isfinite(a)):
        raise MNAAssemblyError("Incidence matrix contains NaN or Inf")

    node_index = {node: index for index, node in enumerate(node_order)}
    branch_admittance = np.zeros(branch_count, dtype=complex)
    current_sources = np.zeros(branch_count, dtype=complex)
    voltage_branches: list[dict[str, Any]] = []

    for branch in branches:
        kind = branch.element_type.upper()
        try:
            if kind == "V" or (kind == "L" and frequency_hz is None):
                value = constitutive_stamp(branch, frequency_hz).w if kind == "V" else 0.0j
                voltage_branches.append(
                    {"branch_index": branch.index, "component_name": branch.component_name,
                     "branch_id": branch.id, "value": value, "kind": kind}
                )
            elif kind == "I":
                stamp = nodal_stamp(branch, frequency_hz)
                if stamp.current is None:
                    raise MNAAssemblyError(f"{branch.component_name}: current source stamp is missing")
                current_sources[branch.index] = stamp.current
            else:
                stamp = nodal_stamp(branch, frequency_hz)
                if stamp.admittance is None:
                    raise MNAAssemblyError(f"{branch.component_name}: admittance stamp is missing")
                branch_admittance[branch.index] = stamp.admittance
        except StampError as error:
            raise MNAAssemblyError(str(error)) from error

    voltage_count = len(voltage_branches)
    opamp_count = len(opamps)
    b_voltage = np.zeros((node_count, voltage_count), dtype=complex)
    voltage_values = np.zeros(voltage_count, dtype=complex)
    voltage_branch_indices: list[int] = []
    voltage_source_labels: list[str] = []
    for index, item in enumerate(voltage_branches):
        branch_index = int(item["branch_index"])
        b_voltage[:, index] = a[:, branch_index]
        voltage_values[index] = item["value"]
        voltage_branch_indices.append(branch_index)
        voltage_source_labels.append(f"I({item['component_name']})")

    c_opamp = np.zeros((node_count, opamp_count), dtype=complex)
    d_opamp = np.zeros((opamp_count, node_count), dtype=complex)
    for index, opamp in enumerate(opamps):
        if opamp.model != "IDEAL":
            raise MNAAssemblyError(f"{opamp.name}: unsupported op-amp model {opamp.model!r}")
        for pin in (opamp.node_plus, opamp.node_minus, opamp.node_out):
            if pin != circuit.reference_node and pin not in node_index:
                raise MNAAssemblyError(f"{opamp.name}: node {pin!r} is missing from circuit model")
        if opamp.node_out != circuit.reference_node:
            c_opamp[node_index[opamp.node_out], index] = 1.0
        if opamp.node_plus != circuit.reference_node:
            d_opamp[index, node_index[opamp.node_plus]] += 1.0
        if opamp.node_minus != circuit.reference_node:
            d_opamp[index, node_index[opamp.node_minus]] -= 1.0

    g_matrix = a @ np.diag(branch_admittance) @ a.T
    rhs_kcl = -(a @ current_sources)
    zero_vv = np.zeros((voltage_count, voltage_count), dtype=complex)
    zero_vo = np.zeros((voltage_count, opamp_count), dtype=complex)
    zero_ov = np.zeros((opamp_count, voltage_count), dtype=complex)
    zero_oo = np.zeros((opamp_count, opamp_count), dtype=complex)
    matrix = np.block([
        [g_matrix, b_voltage, c_opamp],
        [b_voltage.T, zero_vv, zero_vo],
        [d_opamp, zero_ov, zero_oo],
    ])
    rhs = np.concatenate([rhs_kcl, voltage_values, np.zeros(opamp_count, dtype=complex)])

    dimension = node_count + voltage_count + opamp_count
    if matrix.shape != (dimension, dimension) or rhs.shape != (dimension,):
        raise MNAAssemblyError("Assembled MNA system dimensions are inconsistent")
    if not np.all(np.isfinite(matrix)) or not np.all(np.isfinite(rhs)):
        raise MNAAssemblyError("Assembled MNA system contains NaN or Inf")

    unknown_order = (
        [f"V(N{node})" for node in node_order]
        + voltage_source_labels
        + [f"I({opamp.name})" for opamp in opamps]
    )
    equation_order = (
        [f"KCL(N{node})" for node in node_order]
        + [f"VSOURCE({item['component_name']})" for item in voltage_branches]
        + [f"OPAMP_DIFF({opamp.name})" for opamp in opamps]
    )
    return {
        "schema_version": "1.0",
        "source_name": circuit.source_name,
        "analysis": "AC" if frequency_hz is not None else "DC",
        "frequency_hz": frequency_hz,
        "formulation": "MNA",
        "M": _matrix_json(matrix),
        "rhs": _vector_json(rhs),
        "unknown_order": unknown_order,
        "equation_order": equation_order,
        "branch_order": branch_order,
        "component_order": [branch.component_name for branch in branches],
        "node_order": node_order,
        "unknown_blocks": {
            "Vn": [0, node_count],
            "I_voltage_sources": [node_count, node_count + voltage_count],
            "I_opamps": [node_count + voltage_count, dimension],
        },
        "equation_blocks": {
            "KCL": [0, node_count],
            "voltage_sources": [node_count, node_count + voltage_count],
            "opamp_differential": [node_count + voltage_count, dimension],
        },
        "A_reduced": incidence_data["A_reduced"],
        "branch_admittances": _vector_json(branch_admittance),
        "current_sources": _vector_json(current_sources),
        "voltage_source_incidence": _matrix_json(b_voltage),
        "voltage_source_values": _vector_json(voltage_values),
        "voltage_source_branch_indices": voltage_branch_indices,
        "voltage_source_labels": [item["component_name"] for item in voltage_branches],
        "opamp_output_incidence": _matrix_json(c_opamp),
        "opamp_differential_matrix": _matrix_json(d_opamp),
        "opamp_names": [opamp.name for opamp in opamps],
        "opamp_terminals": [
            {"name": opamp.name, "node_plus": opamp.node_plus,
             "node_minus": opamp.node_minus, "node_out": opamp.node_out,
             "line_number": opamp.line_number}
            for opamp in opamps
        ],
        "shape": list(matrix.shape),
        "convention": "X=[Vn; I_voltage_sources; I_opamps], KCL uses outgoing currents",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an ideal-op-amp MNA system")
    parser.add_argument("circuit_json", help="Circuit JSON with .OPAMP directives")
    parser.add_argument("incidence_json", help="Reduced incidence JSON")
    parser.add_argument("-o", "--output", required=True, help="Output MNA system JSON")
    parser.add_argument("--frequency", type=float, help="AC frequency in Hz; omit for DC")
    args = parser.parse_args()
    circuit = load_circuit(args.circuit_json)
    incidence = json.loads(Path(args.incidence_json).read_text(encoding="utf-8"))
    system = build_mna_system(circuit, incidence, args.frequency)
    Path(args.output).write_text(json.dumps(system, indent=2), encoding="utf-8")
    print(f"Built MNA system {tuple(system['shape'])} -> {args.output}")


if __name__ == "__main__":
    main()
