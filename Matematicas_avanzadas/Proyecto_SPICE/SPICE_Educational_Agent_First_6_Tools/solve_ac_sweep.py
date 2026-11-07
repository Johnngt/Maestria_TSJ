#!/usr/bin/env python3
"""Run single-frequency, linear, or decade AC analyses."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from build_circuit_model import Circuit, load_circuit
from build_mna_system import MNAAssemblyError, build_mna_system
from build_constitutive_matrices import build_constitutive_matrices
from build_nodal_system import NodalCompatibilityError, build_nodal_system
from build_tableau_system import build_tableau_system
from solve_linear_system import (
    LinearSystemError,
    solve_matrix_system,
    solve_mna_system,
    solve_nodal_system,
)
from validate_solution import validate_solution


class ACSweepError(ValueError):
    """Raised when an AC sweep request is invalid or ambiguous."""


def generate_frequencies(
    sweep: str, points: int, f_start_hz: float, f_stop_hz: float
) -> list[float]:
    """Generate LIN points including endpoints or DEC points per decade plus stop."""
    if points <= 0:
        raise ACSweepError("Sweep points must be positive")
    if not all(math.isfinite(value) for value in (f_start_hz, f_stop_hz)):
        raise ACSweepError("Sweep frequencies must be finite")
    if f_start_hz <= 0 or f_stop_hz < f_start_hz:
        raise ACSweepError("AC sweep requires 0 < start <= stop")
    mode = sweep.upper()
    if mode == "LIN":
        return np.linspace(f_start_hz, f_stop_hz, points).tolist()
    if mode == "DEC":
        if f_start_hz == f_stop_hz:
            return [f_start_hz]
        decades = math.log10(f_stop_hz / f_start_hz)
        interval_count = int(math.floor(decades * points + 1e-12))
        frequencies = [f_start_hz * 10 ** (index / points) for index in range(interval_count + 1)]
        if not math.isclose(frequencies[-1], f_stop_hz, rel_tol=1e-12, abs_tol=0.0):
            frequencies.append(f_stop_hz)
        else:
            frequencies[-1] = f_stop_hz
        return frequencies
    raise ACSweepError(f"Unsupported sweep type: {sweep!r}; use LIN or DEC")


def _solution_values(result: dict[str, Any]) -> dict[str, complex]:
    values: dict[str, complex] = {}
    for item in result.get("unknowns", []):
        values[item["label"]] = complex(item["real"], item["imag"])
    for field in ("node_voltages", "branch_voltages", "branch_currents"):
        for item in result.get(field, []):
            values[item["label"]] = complex(item["real"], item["imag"])
    return values


def _transfer_records(
    values: dict[str, complex], transfer_functions: dict[str, dict[str, str]]
) -> dict[str, Any]:
    records: dict[str, Any] = {}
    for name, specification in transfer_functions.items():
        numerator_label = specification["numerator"]
        denominator_label = specification["denominator"]
        if numerator_label not in values or denominator_label not in values:
            raise ACSweepError(
                f"Transfer {name!r} references an unavailable variable: "
                f"{numerator_label!r} / {denominator_label!r}"
            )
        denominator = values[denominator_label]
        if abs(denominator) == 0:
            records[name] = {
                "numerator": numerator_label,
                "denominator": denominator_label,
                "real": None,
                "imag": None,
                "magnitude": None,
                "phase_deg": None,
                "magnitude_db": None,
                "status": "ZERO_REFERENCE",
            }
            continue
        transfer = values[numerator_label] / denominator
        magnitude = abs(transfer)
        records[name] = {
            "numerator": numerator_label,
            "denominator": denominator_label,
            "real": float(transfer.real),
            "imag": float(transfer.imag),
            "magnitude": float(magnitude),
            "phase_deg": float(np.degrees(np.angle(transfer))),
            "magnitude_db": float(20.0 * math.log10(magnitude)) if magnitude else None,
            "status": "PASS" if magnitude else "ZERO_TRANSFER",
        }
    return records


def solve_ac_sweep(
    circuit: Circuit,
    incidence_data: dict[str, Any],
    sweep: dict[str, Any],
    formulation: str = "NODAL",
    transfer_functions: dict[str, dict[str, str]] | None = None,
    atol: float = 1e-10,
    rtol: float = 1e-8,
    condition_limit: float = 1e12,
) -> dict[str, Any]:
    frequencies = generate_frequencies(
        sweep["sweep"], int(sweep["points"]), float(sweep["f_start_hz"]), float(sweep["f_stop_hz"])
    )
    mode = formulation.upper()
    if mode not in {"NODAL", "TABLEAU", "MNA"}:
        raise ACSweepError("Formulation must be NODAL, TABLEAU, or MNA")
    if circuit.opamps and mode != "MNA":
        raise ACSweepError("Circuit contains ideal op-amps; select the MNA formulation")
    transfer_functions = transfer_functions or {}
    points: list[dict[str, Any]] = []

    for frequency in frequencies:
        try:
            constitutive = build_constitutive_matrices(circuit, frequency)
            if mode == "NODAL":
                system = build_nodal_system(circuit, incidence_data, frequency)
                solution = solve_nodal_system(system, circuit, atol, rtol)
            elif mode == "TABLEAU":
                system = build_tableau_system(circuit, incidence_data, constitutive)
                solution = solve_matrix_system(system, atol, rtol)
            else:
                system = build_mna_system(circuit, incidence_data, frequency)
                solution = solve_mna_system(system, circuit, atol, rtol)
            validation = validate_solution(
                system, solution, atol=atol, rtol=rtol, condition_limit=condition_limit
            )
            values = _solution_values(solution)
            transfers = _transfer_records(values, transfer_functions)
            status = validation["status"]
            if any(record["status"] == "ZERO_REFERENCE" for record in transfers.values()):
                status = "WARN" if status == "PASS" else status
            points.append(
                {
                    "frequency_hz": frequency,
                    "status": status,
                    "solution": solution,
                    "validation": validation,
                    "transfer_functions": transfers,
                }
            )
        except (
            ACSweepError,
            LinearSystemError,
            NodalCompatibilityError,
            MNAAssemblyError,
            ValueError,
        ) as exc:
            points.append(
                {
                    "frequency_hz": frequency,
                    "status": "FAIL",
                    "diagnostic": str(exc),
                }
            )

    statuses = [point["status"] for point in points]
    overall = "FAIL" if "FAIL" in statuses else "WARN" if "WARN" in statuses else "PASS"
    return {
        "schema_version": "1.0",
        "source_name": circuit.source_name,
        "analysis": "AC",
        "formulation": mode,
        "sweep": {
            "type": sweep["sweep"].upper(),
            "points_per_decade_or_count": int(sweep["points"]),
            "f_start_hz": float(sweep["f_start_hz"]),
            "f_stop_hz": float(sweep["f_stop_hz"]),
            "frequency_count": len(frequencies),
        },
        "status": overall,
        "atol": atol,
        "rtol": rtol,
        "condition_limit": condition_limit,
        "points": points,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an AC frequency analysis")
    parser.add_argument("circuit_json")
    parser.add_argument("incidence_json")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--formulation", choices=("NODAL", "TABLEAU", "MNA"), default="NODAL")
    parser.add_argument("--transfers", help="JSON mapping transfer names to numerator/denominator labels")
    parser.add_argument("--atol", type=float, default=1e-10)
    parser.add_argument("--rtol", type=float, default=1e-8)
    parser.add_argument("--condition-limit", type=float, default=1e12)
    args = parser.parse_args()
    circuit = load_circuit(args.circuit_json)
    incidence = json.loads(Path(args.incidence_json).read_text(encoding="utf-8"))
    directives = [item for item in circuit.directives if item.get("command") == "AC"]
    if len(directives) != 1:
        parser.error("Circuit must contain exactly one .AC directive")
    transfers = json.loads(Path(args.transfers).read_text(encoding="utf-8")) if args.transfers else None
    result = solve_ac_sweep(
        circuit, incidence, directives[0], args.formulation, transfers,
        args.atol, args.rtol, args.condition_limit,
    )
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"AC sweep {result['status']}: {result['sweep']['frequency_count']} points -> {args.output}")
    if result["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()