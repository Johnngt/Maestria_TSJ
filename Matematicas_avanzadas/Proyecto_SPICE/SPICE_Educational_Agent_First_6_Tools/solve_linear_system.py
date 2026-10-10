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
    parser.add_argument("circuit_json")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--atol", type=float, default=1e-10)
    parser.add_argument("--rtol", type=float, default=1e-8)
    args = parser.parse_args()
    system = json.loads(Path(args.system_json).read_text(encoding="utf-8"))
    circuit = load_circuit(args.circuit_json)
    result = solve_nodal_system(system, circuit, args.atol, args.rtol)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Solved {result['analysis']} system: PASS -> {args.output}")
    for item in result["node_voltages"]:
        print(f"{item['label']} = {item['real']:.9g} + j{item['imag']:.9g} {item['unit']}")


if __name__ == "__main__":
    main()
