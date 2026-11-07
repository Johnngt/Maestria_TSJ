#!/usr/bin/env python3
"""Validate linear-system, Kirchhoff, branch, and constitutive residuals."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from solve_linear_system import json_to_complex_matrix, json_to_complex_vector


def _metric(name: str, residual: np.ndarray, scale: float, atol: float, rtol: float) -> dict[str, Any]:
    norm = float(np.linalg.norm(residual))
    threshold = atol + rtol * scale
    return {
        "name": name,
        "norm": norm,
        "scale": float(scale),
        "threshold": float(threshold),
        "passed": bool(np.isfinite(norm) and norm <= threshold),
    }


def validate_solution(
    system: dict[str, Any],
    solution: dict[str, Any],
    atol: float = 1e-10,
    rtol: float = 1e-8,
    condition_limit: float = 1e12,
) -> dict[str, Any]:
    """Return auditable checks for a nodal or Tableau solution."""
    checks: list[dict[str, Any]] = []
    diagnostics: list[str] = []
    if atol < 0 or rtol < 0 or not math.isfinite(atol + rtol):
        raise ValueError("atol and rtol must be finite and non-negative")
    if condition_limit <= 0 or not math.isfinite(condition_limit):
        raise ValueError("condition_limit must be finite and positive")

    matrix_data = system.get("M", system.get("T"))
    rhs_data = system.get("rhs", system.get("Wp"))
    raw = solution.get("raw", {})
    try:
        if matrix_data is None or rhs_data is None:
            raise ValueError("System is missing its matrix or right-hand side")
        matrix = json_to_complex_matrix(matrix_data)
        rhs = json_to_complex_vector(rhs_data)
        tableau = solution.get("formulation") == "TABLEAU" or "X" in raw
        unknowns = json_to_complex_vector(raw["X"]) if tableau else json_to_complex_vector(raw["Vn"])
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("System matrix must be square")
        if rhs.shape != (matrix.shape[0],) or unknowns.shape != rhs.shape:
            raise ValueError("Solution and system dimensions do not match")
        if not all(np.all(np.isfinite(item)) for item in (matrix, rhs, unknowns)):
            raise ValueError("System or solution contains NaN or Inf")

        residual = matrix @ unknowns - rhs
        scale = float(np.linalg.norm(matrix) * np.linalg.norm(unknowns) + np.linalg.norm(rhs))
        checks.append(_metric("linear_residual", residual, scale, atol, rtol))
        rank = int(np.linalg.matrix_rank(matrix))
        condition = float(np.linalg.cond(matrix))
        if rank < matrix.shape[0]:
            diagnostics.append(f"System is rank deficient ({rank}/{matrix.shape[0]})")
            checks.append({"name": "full_rank", "rank": rank, "size": matrix.shape[0], "passed": False})
        else:
            checks.append({"name": "full_rank", "rank": rank, "size": matrix.shape[0], "passed": True})
        if not np.isfinite(condition):
            diagnostics.append("Condition number is not finite")
        elif condition > condition_limit:
            diagnostics.append(
                f"Condition number {condition:.3e} exceeds configured limit {condition_limit:.3e}"
            )

        a_data = system.get("A_reduced")
        if a_data is not None:
            a = np.asarray(a_data, dtype=float)
            currents = json_to_complex_vector(raw["I"])
            if a.ndim != 2 or a.shape[1] != currents.size:
                raise ValueError("Incidence matrix and branch-current dimensions do not match")
            kcl_residual = a @ currents
            if system.get("formulation") == "MNA":
                opamp_incidence = json_to_complex_matrix(system["opamp_output_incidence"])
                opamp_currents = json_to_complex_vector(raw["I_opamps"])
                if opamp_incidence.shape != (a.shape[0], opamp_currents.size):
                    raise ValueError("Op-amp output incidence and current dimensions do not match")
                kcl_residual = kcl_residual + opamp_incidence @ opamp_currents
            checks.append(
                _metric("KCL", kcl_residual, float(np.linalg.norm(a) * np.linalg.norm(currents)), atol, rtol)
            )

            if "Vb" in raw and "Vn" in raw:
                vb = json_to_complex_vector(raw["Vb"])
                vn = json_to_complex_vector(raw["Vn"])
                if vb.shape != (a.shape[1],) or vn.shape != (a.shape[0],):
                    raise ValueError("Branch and node voltage dimensions do not match incidence matrix")
                relation = vb - a.T @ vn
                checks.append(
                    _metric(
                        "branch_node_voltage",
                        relation,
                        float(np.linalg.norm(vb) + np.linalg.norm(a.T @ vn)),
                        atol,
                        rtol,
                    )
                )

        if all(key in system for key in ("Y", "Z", "W")) and all(
            key in raw for key in ("Vb", "I")
        ):
            y = json_to_complex_matrix(system["Y"])
            z = json_to_complex_matrix(system["Z"])
            w = json_to_complex_vector(system["W"])
            vb = json_to_complex_vector(raw["Vb"])
            currents = json_to_complex_vector(raw["I"])
            if y.shape != z.shape or y.shape != (vb.size, vb.size) or w.shape != (vb.size,):
                raise ValueError("Constitutive matrix dimensions do not match branch vectors")
            constitutive_residual = y @ vb + z @ currents - w
            constitutive_scale = float(
                np.linalg.norm(y) * np.linalg.norm(vb)
                + np.linalg.norm(z) * np.linalg.norm(currents)
                + np.linalg.norm(w)
            )
            checks.append(
                _metric("constitutive_residual", constitutive_residual, constitutive_scale, atol, rtol)
            )
        if system.get("formulation") == "MNA":
            vn = json_to_complex_vector(raw["Vn"])
            voltage_incidence = json_to_complex_matrix(system["voltage_source_incidence"])
            voltage_values = json_to_complex_vector(system["voltage_source_values"])
            if voltage_incidence.shape != (vn.size, voltage_values.size):
                raise ValueError("Voltage-source incidence and value dimensions do not match")
            source_residual = voltage_incidence.T @ vn - voltage_values
            checks.append(
                _metric(
                    "voltage_source_constraints",
                    source_residual,
                    float(np.linalg.norm(voltage_incidence) * np.linalg.norm(vn) + np.linalg.norm(voltage_values)),
                    atol,
                    rtol,
                )
            )

            differential = json_to_complex_matrix(system["opamp_differential_matrix"])
            if differential.shape != (len(system.get("opamp_names", [])), vn.size):
                raise ValueError("Op-amp differential matrix dimensions do not match nodes")
            differential_residual = differential @ vn
            checks.append(
                _metric(
                    "opamp_differential_constraint",
                    differential_residual,
                    float(np.linalg.norm(differential) * np.linalg.norm(vn)),
                    atol,
                    rtol,
                )
            )

            admittances = json_to_complex_vector(system["branch_admittances"])
            source_currents = json_to_complex_vector(system["current_sources"])
            source_indices = {int(index) for index in system["voltage_source_branch_indices"]}
            if admittances.size != vb.size or source_currents.size != vb.size:
                raise ValueError("MNA branch stamps do not match branch-voltage vector")
            regular_indices = [index for index in range(vb.size) if index not in source_indices]
            branch_residual = currents[regular_indices] - (
                admittances[regular_indices] * vb[regular_indices] + source_currents[regular_indices]
            )
            checks.append(
                _metric(
                    "branch_admittance",
                    branch_residual,
                    float(
                        np.linalg.norm(currents[regular_indices])
                        + np.linalg.norm(admittances[regular_indices] * vb[regular_indices])
                        + np.linalg.norm(source_currents[regular_indices])
                    ),
                    atol,
                    rtol,
                )
            )

        elif all(key in system for key in ("Y_branch", "J_branch")) and all(
            key in raw for key in ("Vb", "I")
        ):
            y = json_to_complex_matrix(system["Y_branch"])
            j = json_to_complex_vector(system["J_branch"])
            vb = json_to_complex_vector(raw["Vb"])
            currents = json_to_complex_vector(raw["I"])
            branch_residual = currents - (y @ vb + j)
            checks.append(
                _metric(
                    "branch_admittance",
                    branch_residual,
                    float(np.linalg.norm(currents) + np.linalg.norm(y @ vb) + np.linalg.norm(j)),
                    atol,
                    rtol,
                )
            )
    except (KeyError, TypeError, ValueError, np.linalg.LinAlgError) as exc:
        diagnostics.append(str(exc))

    if solution.get("status") not in {None, "PASS", "WARN"}:
        diagnostics.append(f"Solver status is {solution.get('status')!r}")
    failed = any(check.get("passed") is False for check in checks)
    if diagnostics and not checks:
        status = "FAIL"
    elif failed or any("NaN" in item or "missing" in item or "dimensions" in item for item in diagnostics):
        status = "FAIL"
    elif diagnostics:
        status = "WARN"
    else:
        status = "PASS"
    if failed:
        status = "FAIL"

    return {
        "schema_version": "1.0",
        "source_name": system.get("source_name", solution.get("source_name", "<unknown>")),
        "analysis": system.get("analysis", solution.get("analysis")),
        "frequency_hz": system.get("frequency_hz", solution.get("frequency_hz")),
        "status": status,
        "checks": checks,
        "diagnostics": diagnostics,
        "condition_number": condition if "condition" in locals() else None,
        "atol": atol,
        "rtol": rtol,
        "condition_limit": condition_limit,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a solved nodal or Tableau system")
    parser.add_argument("system_json")
    parser.add_argument("solution_json")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--atol", type=float, default=1e-10)
    parser.add_argument("--rtol", type=float, default=1e-8)
    parser.add_argument("--condition-limit", type=float, default=1e12)
    args = parser.parse_args()
    system = json.loads(Path(args.system_json).read_text(encoding="utf-8"))
    solution = json.loads(Path(args.solution_json).read_text(encoding="utf-8"))
    result = validate_solution(system, solution, args.atol, args.rtol, args.condition_limit)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Validation {result['status']} -> {args.output}")
    if result["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()