#!/usr/bin/env python3
"""
solve_linear_system.py

Purpose:
    Solve the nodal system created by build_nodal_system.py with NumPy,
    compute numerical diagnostics, recover passive/source branch currents,
    and verify the linear-system and KCL residuals.

Author: Dr. Francisco E. Rangel-Patiño
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from build_circuit_model import Circuit, load_circuit


class LinearSystemError(RuntimeError):
    """Raised when a system is singular, malformed, or fails validation."""


def json_to_complex(value: dict[str, float]) -> complex:
    return complex(value["real"], value["imag"])


def json_to_complex_matrix(data: list[list[dict[str, float]]]) -> np.ndarray:
    return np.array([[json_to_complex(v) for v in row] for row in data], dtype=complex)


def json_to_complex_vector(data: list[dict[str, float]]) -> np.ndarray:
    return np.array([json_to_complex(v) for v in data], dtype=complex)


def complex_to_json(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def vector_records(labels: list[str], values: np.ndarray, unit: str) -> list[dict[str, Any]]:
    return [
        {
            "label": label,
            "real": float(complex(value).real),
            "imag": float(complex(value).imag),
            "magnitude": float(abs(value)),
            "phase_deg": float(np.degrees(np.angle(value))),
            "unit": unit,
        }
        for label, value in zip(labels, values.reshape(-1))
    ]


def solve_matrix_system(
    system: dict[str, Any],
    atol: float = 1e-10,
    rtol: float = 1e-8,
) -> dict[str, Any]:
    """Solve a serialized generic linear system, including Tableau systems."""
    matrix_data = system.get("M", system.get("T"))
    rhs_data = system.get("rhs", system.get("Wp"))
    if matrix_data is None or rhs_data is None:
        raise LinearSystemError("System must contain matrix M/T and vector rhs/Wp")
    matrix = json_to_complex_matrix(matrix_data)
    rhs = json_to_complex_vector(rhs_data)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise LinearSystemError("Linear-system matrix must be square")
    if rhs.shape != (matrix.shape[0],):
        raise LinearSystemError("Linear-system vector has incompatible dimensions")
    if not np.all(np.isfinite(matrix)) or not np.all(np.isfinite(rhs)):
        raise LinearSystemError("Linear system contains NaN or Inf")

    rank = int(np.linalg.matrix_rank(matrix))
    condition = float(np.linalg.cond(matrix))
    if rank < matrix.shape[0] or not np.isfinite(condition):
        raise LinearSystemError(
            f"Singular linear system: rank={rank}, size={matrix.shape[0]}, condition={condition}"
        )
    try:
        values = np.linalg.solve(matrix, rhs)
    except np.linalg.LinAlgError as exc:
        raise LinearSystemError(f"NumPy could not solve the system: {exc}") from exc

    residual = matrix @ values - rhs
    residual_norm = float(np.linalg.norm(residual))
    scale = float(np.linalg.norm(matrix) * np.linalg.norm(values) + np.linalg.norm(rhs))
    normalized_residual = residual_norm / scale if scale else residual_norm
    if not np.allclose(matrix @ values, rhs, atol=atol, rtol=rtol):
        raise LinearSystemError(f"Solution failed validation: residual={residual_norm:.3e}")

    labels = system.get("unknown_order", [f"x[{index}]" for index in range(len(values))])
    if len(labels) != len(values):
        raise LinearSystemError("Unknown labels do not match system dimension")
    records = []
    for label, value in zip(labels, values):
        unit = "volt" if label.startswith("V(") else "ampere" if label.startswith("I(") else "unknown"
        records.extend(vector_records([label], np.asarray([value]), unit))

    raw: dict[str, Any] = {"X": [complex_to_json(value) for value in values]}
    blocks = system.get("unknown_blocks", {})
    for block_name, bounds in blocks.items():
        if len(bounds) == 2:
            raw[block_name] = [complex_to_json(value) for value in values[bounds[0]:bounds[1]]]

    return {
        "schema_version": "1.0",
        "source_name": system.get("source_name", "<unknown>"),
        "analysis": system.get("analysis"),
        "frequency_hz": system.get("frequency_hz"),
        "formulation": system.get("formulation", "LINEAR"),
        "status": "PASS",
        "rank": rank,
        "condition_number": condition,
        "residual_norm": residual_norm,
        "normalized_residual": normalized_residual,
        "atol": atol,
        "rtol": rtol,
        "unknowns": records,
        "raw": raw,
    }



def solve_mna_system(
    system: dict[str, Any],
    circuit: Circuit,
    atol: float = 1e-10,
    rtol: float = 1e-8,
) -> dict[str, Any]:
    """Solve an MNA system and recover node and branch observables."""
    if system.get("formulation") != "MNA":
        raise LinearSystemError("System formulation must be MNA")
    branch_order = [branch.id for branch in circuit.branches]
    if system.get("branch_order") != branch_order:
        raise LinearSystemError("Circuit branch order does not match MNA system branch order")
    solved = solve_matrix_system(system, atol, rtol)
    raw_x = json_to_complex_vector(solved["raw"]["X"])
    blocks = system.get("unknown_blocks", {})
    try:
        vn = raw_x[slice(*blocks["Vn"])]
        source_currents = raw_x[slice(*blocks["I_voltage_sources"])]
        opamp_currents = raw_x[slice(*blocks["I_opamps"])]
        a = np.asarray(system["A_reduced"], dtype=float)
        branch_admittances = json_to_complex_vector(system["branch_admittances"])
        current_sources = json_to_complex_vector(system["current_sources"])
        source_indices = [int(value) for value in system["voltage_source_branch_indices"]]
    except (KeyError, TypeError, ValueError) as error:
        raise LinearSystemError(f"Malformed MNA recovery metadata: {error}") from error
    if a.shape != (vn.size, len(branch_order)):
        raise LinearSystemError("MNA incidence matrix and unknown dimensions do not match")
    if branch_admittances.shape != (len(branch_order),) or current_sources.shape != (len(branch_order),):
        raise LinearSystemError("MNA branch stamp dimensions do not match circuit")
    if len(source_indices) != source_currents.size:
        raise LinearSystemError("MNA voltage-source current map does not match unknown vector")

    vb = a.T @ vn
    branch_currents = branch_admittances * vb + current_sources
    for source_index, current in zip(source_indices, source_currents):
        if source_index < 0 or source_index >= len(branch_order):
            raise LinearSystemError("MNA voltage-source branch index is out of range")
        branch_currents[source_index] = current

    node_labels = [f"V(N{node})" for node in system["node_order"]]
    branch_labels = [
        f"{branch.id} ({branch.component_name})" for branch in circuit.branches
    ]
    opamp_labels = [f"I({name})" for name in system.get("opamp_names", [])]
    solved["formulation"] = "MNA"
    solved["node_voltages"] = vector_records(node_labels, vn, "volt")
    solved["branch_voltages"] = vector_records(branch_labels, vb, "volt")
    solved["branch_currents"] = vector_records(branch_labels, branch_currents, "ampere")
    solved["opamp_output_currents"] = vector_records(opamp_labels, opamp_currents, "ampere")
    solved["raw"].update({
        "Vn": [complex_to_json(value) for value in vn],
        "Vb": [complex_to_json(value) for value in vb],
        "I": [complex_to_json(value) for value in branch_currents],
        "I_voltage_sources": [complex_to_json(value) for value in source_currents],
        "I_opamps": [complex_to_json(value) for value in opamp_currents],
    })
    return solved

def solve_nodal_system(
    system: dict[str, Any],
    circuit: Circuit,
    atol: float = 1e-10,
    rtol: float = 1e-8,
) -> dict[str, Any]:
    m = json_to_complex_matrix(system["M"])
    rhs = json_to_complex_vector(system["rhs"])
    a = np.array(system["A_reduced"], dtype=float)
    y = json_to_complex_matrix(system["Y_branch"])
    j_branch = json_to_complex_vector(system["J_branch"])
    expected_branch_order = [branch.id for branch in circuit.branches]
    if system.get("branch_order") != expected_branch_order:
        raise LinearSystemError("Circuit branch order does not match nodal-system branch order")
    if a.ndim != 2 or a.shape[1] != len(expected_branch_order):
        raise LinearSystemError("Reduced incidence matrix has incorrect dimensions")
    if y.shape != (len(expected_branch_order), len(expected_branch_order)):
        raise LinearSystemError("Branch admittance matrix has incorrect dimensions")
    if j_branch.shape != (len(expected_branch_order),):
        raise LinearSystemError("Current-source vector has incorrect dimensions")
    if m.shape[0] != m.shape[1] or rhs.shape != (m.shape[0],):
        raise LinearSystemError("Malformed linear-system dimensions")
    rank = int(np.linalg.matrix_rank(m))
    condition = float(np.linalg.cond(m))
    if rank < m.shape[0] or not np.isfinite(condition):
        raise LinearSystemError(
            f"Singular nodal system: rank={rank}, size={m.shape[0]}, condition={condition}"
        )
    try:
        vn = np.linalg.solve(m, rhs)
    except np.linalg.LinAlgError as exc:
        raise LinearSystemError(f"NumPy could not solve the system: {exc}") from exc

    vb = a.T @ vn
    currents = y @ vb + j_branch
    residual = m @ vn - rhs
    kcl = a @ currents
    residual_norm = float(np.linalg.norm(residual))
    kcl_norm = float(np.linalg.norm(kcl))
    scale = float(np.linalg.norm(m) * np.linalg.norm(vn) + np.linalg.norm(rhs))
    normalized_residual = residual_norm / scale if scale else residual_norm
    passed = bool(
        np.allclose(m @ vn, rhs, atol=atol, rtol=rtol)
        and np.allclose(kcl, 0.0, atol=atol, rtol=rtol)
    )
    if not passed:
        raise LinearSystemError(
            f"Solution failed validation: residual={residual_norm:.3e}, KCL={kcl_norm:.3e}"
        )
    branch_labels = [
        f"{branch.id} ({branch.component_name})" for branch in circuit.branches
    ]
    return {
        "schema_version": "1.0",
        "source_name": system["source_name"],
        "analysis": system["analysis"],
        "frequency_hz": system.get("frequency_hz"),
        "status": "PASS",
        "rank": rank,
        "condition_number": condition,
        "residual_norm": residual_norm,
        "normalized_residual": normalized_residual,
        "kcl_norm": kcl_norm,
        "atol": atol,
        "rtol": rtol,
        "node_voltages": vector_records([f"V(N{n})" for n in system["node_order"]], vn, "volt"),
        "branch_voltages": vector_records(branch_labels, vb, "volt"),
        "branch_currents": vector_records(branch_labels, currents, "ampere"),
        "raw": {
            "Vn": [complex_to_json(v) for v in vn],
            "Vb": [complex_to_json(v) for v in vb],
            "I": [complex_to_json(v) for v in currents],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve and validate a nodal linear system")
    parser.add_argument("system_json")
    parser.add_argument("circuit_json", nargs="?", help="Required for nodal current recovery")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--atol", type=float, default=1e-10)
    parser.add_argument("--rtol", type=float, default=1e-8)
    args = parser.parse_args()
    system = json.loads(Path(args.system_json).read_text(encoding="utf-8"))
    if system.get("formulation") == "MNA":
        if not args.circuit_json:
            parser.error("circuit_json is required for MNA physical-variable recovery")
        circuit = load_circuit(args.circuit_json)
        result = solve_mna_system(system, circuit, args.atol, args.rtol)
    elif system.get("formulation") == "TABLEAU" or "unknown_blocks" in system:
        result = solve_matrix_system(system, args.atol, args.rtol)
    else:
        if not args.circuit_json:
            parser.error("circuit_json is required for nodal systems")
        circuit = load_circuit(args.circuit_json)
        result = solve_nodal_system(system, circuit, args.atol, args.rtol)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Solved {result['analysis']} system: PASS -> {args.output}")
    for item in result.get("node_voltages", result.get("unknowns", [])):
        if item.get("unit") == "volt":
            print(f"{item['label']} = {item['real']:.9g} + j{item['imag']:.9g} {item['unit']}")


if __name__ == "__main__":
    main()
