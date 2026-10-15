#!/usr/bin/env python3
"""Compare solver outputs with analytical or documented reference values."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


class ReferenceComparisonError(ValueError):
    """Raised when actual and reference artifacts cannot be aligned."""


def _records(data: dict[str, Any]) -> dict[str, tuple[complex, str | None]]:
    result: dict[str, tuple[complex, str | None]] = {}
    for key in ("unknowns", "node_voltages", "branch_voltages", "branch_currents"):
        for item in data.get(key, []):
            result[item["label"]] = (
                complex(float(item["real"]), float(item["imag"])), item.get("unit")
            )
    if not result and isinstance(data.get("variables"), dict):
        for label, item in data["variables"].items():
            if isinstance(item, dict):
                value = complex(float(item.get("real", 0.0)), float(item.get("imag", 0.0)))
                result[label] = (value, item.get("unit"))
            else:
                result[label] = (complex(float(item)), None)
    return result


def _points(data: dict[str, Any], *, is_reference: bool) -> list[dict[str, Any]]:
    if "points" not in data:
        payload = data.get("solution", data)
        return [{"frequency_hz": data.get("frequency_hz"), "variables": _records(payload)}]
    points: list[dict[str, Any]] = []
    for point in data["points"]:
        if point.get("status") == "FAIL":
            points.append({"frequency_hz": point.get("frequency_hz"), "variables": {}, "failed": True})
            continue
        if not is_reference and point.get("transfer_functions"):
            payload = {
                "variables": {
                    name: {
                        "real": item.get("real", 0.0),
                        "imag": item.get("imag", 0.0),
                        "unit": item.get("unit", "ratio"),
                    }
                    for name, item in point["transfer_functions"].items()
                    if item.get("real") is not None and item.get("imag") is not None
                }
            }
        elif is_reference and isinstance(point.get("variables"), dict):
            payload = {"variables": point["variables"]}
        else:
            payload = point.get("solution", point)
        points.append(
            {
                "frequency_hz": point.get("frequency_hz"),
                "variables": _records(payload),
                "failed": False,
            }
        )
    return points


def compare_reference(
    actual: dict[str, Any],
    reference: dict[str, Any],
    atol: float = 1e-8,
    rtol: float = 1e-6,
    frequency_atol: float = 1e-9,
    frequency_rtol: float = 1e-8,
) -> dict[str, Any]:
    """Compare requested complex variables, units, and matching frequencies."""
    if any(value < 0 or not math.isfinite(value) for value in (atol, rtol, frequency_atol, frequency_rtol)):
        raise ReferenceComparisonError("Tolerances must be finite and non-negative")
    actual_points = _points(actual, is_reference=False)
    reference_points = _points(reference, is_reference=True)
    if len(actual_points) != len(reference_points):
        raise ReferenceComparisonError(
            f"Point count differs: actual={len(actual_points)}, reference={len(reference_points)}"
        )

    comparisons: list[dict[str, Any]] = []
    diagnostics: list[str] = []
    for index, (actual_point, reference_point) in enumerate(zip(actual_points, reference_points)):
        actual_frequency = actual_point.get("frequency_hz")
        reference_frequency = reference_point.get("frequency_hz")
        if actual_frequency is not None or reference_frequency is not None:
            if actual_frequency is None or reference_frequency is None or not math.isclose(
                float(actual_frequency), float(reference_frequency),
                rel_tol=frequency_rtol, abs_tol=frequency_atol,
            ):
                raise ReferenceComparisonError(
                    f"Frequency mismatch at point {index}: actual={actual_frequency}, "
                    f"reference={reference_frequency}"
                )
        if actual_point.get("failed") or reference_point.get("failed"):
            comparisons.append(
                {"point": index, "frequency_hz": actual_frequency, "status": "FAIL", "checks": []}
            )
            diagnostics.append(f"Point {index} contains a failed simulation or reference result")
            continue

        variable_checks: list[dict[str, Any]] = []
        reference_variables = reference_point["variables"]
        for label, (reference_value, reference_unit) in reference_variables.items():
            if label not in actual_point["variables"]:
                variable_checks.append({"label": label, "passed": False, "error": "missing actual variable"})
                continue
            actual_value, actual_unit = actual_point["variables"][label]
            if actual_unit and reference_unit and actual_unit != reference_unit:
                variable_checks.append(
                    {
                        "label": label,
                        "passed": False,
                        "error": f"unit mismatch: actual={actual_unit}, reference={reference_unit}",
                    }
                )
                continue
            if not actual_unit or not reference_unit:
                diagnostics.append(f"Point {index}, {label}: unit metadata is incomplete")
            absolute_error = abs(actual_value - reference_value)
            relative_error = absolute_error / abs(reference_value) if abs(reference_value) else (
                0.0 if absolute_error == 0 else None
            )
            threshold = atol + rtol * abs(reference_value)
            variable_checks.append(
                {
                    "label": label,
                    "unit": actual_unit or reference_unit,
                    "actual": {"real": actual_value.real, "imag": actual_value.imag},
                    "reference": {"real": reference_value.real, "imag": reference_value.imag},
                    "absolute_error": absolute_error,
                    "relative_error": relative_error,
                    "threshold": threshold,
                    "passed": bool(absolute_error <= threshold),
                }
            )
        if not variable_checks:
            diagnostics.append(f"Point {index} contains no reference variables")
        point_status = "FAIL" if any(item.get("passed") is False for item in variable_checks) else "PASS"
        comparisons.append(
            {
                "point": index,
                "frequency_hz": actual_frequency,
                "status": point_status,
                "checks": variable_checks,
            }
        )

    status = "FAIL" if any(item["status"] == "FAIL" for item in comparisons) else (
        "WARN" if diagnostics else "PASS"
    )
    return {
        "schema_version": "1.0",
        "source_name": actual.get("source_name", "<unknown>"),
        "analysis": actual.get("analysis"),
        "reference_info": reference.get("reference_info", {}),
        "status": status,
        "atol": atol,
        "rtol": rtol,
        "frequency_atol": frequency_atol,
        "frequency_rtol": frequency_rtol,
        "comparisons": comparisons,
        "diagnostics": diagnostics,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare results with a reference JSON")
    parser.add_argument("actual_json")
    parser.add_argument("reference_json")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--atol", type=float, default=1e-8)
    parser.add_argument("--rtol", type=float, default=1e-6)
    args = parser.parse_args()
    actual = json.loads(Path(args.actual_json).read_text(encoding="utf-8"))
    reference = json.loads(Path(args.reference_json).read_text(encoding="utf-8"))
    result = compare_reference(actual, reference, args.atol, args.rtol)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Reference comparison {result['status']} -> {args.output}")
    if result["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()