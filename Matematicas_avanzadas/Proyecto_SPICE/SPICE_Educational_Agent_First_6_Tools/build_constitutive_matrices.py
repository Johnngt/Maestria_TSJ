#!/usr/bin/env python3
"""Build branch constitutive matrices Y, Z, and W for the Tableau system."""
from __future__ import annotations

import argparse
import cmath
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from build_circuit_model import Circuit, load_circuit


class ConstitutiveModelError(ValueError):
    """Raised when a branch has no valid constitutive model."""


def complex_to_json(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def complex_matrix_to_json(matrix: np.ndarray) -> list[list[dict[str, float]]]:
    return [[complex_to_json(complex(value)) for value in row] for row in matrix]


def complex_vector_to_json(vector: np.ndarray) -> list[dict[str, float]]:
    return [complex_to_json(complex(value)) for value in vector.reshape(-1)]


def source_value(branch: Any, frequency_hz: float | None) -> complex:
    source_kind = (branch.source_kind or "DC").upper()
    if frequency_hz is None:
        if source_kind == "AC":
            return 0.0 + 0.0j
        return complex(branch.value_si)
    if source_kind != "AC":
        return 0.0 + 0.0j
    magnitude = branch.ac_magnitude
    if magnitude is None:
        magnitude = branch.value_si
    phase_deg = branch.ac_phase_deg or 0.0
    if not math.isfinite(float(magnitude)) or not math.isfinite(float(phase_deg)):
        raise ConstitutiveModelError(
            f"{branch.component_name}: AC magnitude and phase must be finite"
        )
    return cmath.rect(float(magnitude), math.radians(float(phase_deg)))


def branch_model(
    branch: Any, frequency_hz: float | None
) -> tuple[complex, complex, complex, str]:
    """Return coefficients for Y*Vb + Z*I = W and its source equation."""
    element_type = branch.element_type.upper()
    value = float(branch.value_si)
    if not math.isfinite(value):
        raise ConstitutiveModelError(f"{branch.component_name}: value must be finite")

    if element_type == "R":
        if value <= 0:
            raise ConstitutiveModelError(f"{branch.component_name}: resistance must be positive")
        return 1.0 + 0.0j, -value + 0.0j, 0.0 + 0.0j, "V - R*I = 0"
    if element_type == "G":
        if value < 0:
            raise ConstitutiveModelError(f"{branch.component_name}: conductance cannot be negative")
        return value + 0.0j, -1.0 + 0.0j, 0.0 + 0.0j, "G*V - I = 0"
    if element_type == "C":
        if value <= 0:
            raise ConstitutiveModelError(f"{branch.component_name}: capacitance must be positive")
        if frequency_hz is None:
            return 0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j, "I = 0 (DC steady state)"
        s = 1j * 2.0 * math.pi * frequency_hz
        return s * value, -1.0 + 0.0j, 0.0 + 0.0j, "s*C*V - I = 0"
    if element_type == "L":
        if value <= 0:
            raise ConstitutiveModelError(f"{branch.component_name}: inductance must be positive")
        if frequency_hz is None:
            return 1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, "V = 0 (DC steady state)"
        s = 1j * 2.0 * math.pi * frequency_hz
        return 1.0 + 0.0j, -s * value, 0.0 + 0.0j, "V - s*L*I = 0"
    if element_type == "V":
        return 1.0 + 0.0j, 0.0 + 0.0j, source_value(branch, frequency_hz), "V = E"
    if element_type == "I":
        return 0.0 + 0.0j, 1.0 + 0.0j, source_value(branch, frequency_hz), "I = J"
    raise ConstitutiveModelError(
        f"{branch.component_name}: unsupported element type {branch.element_type!r}"
    )


def build_constitutive_matrices(
    circuit: Circuit, frequency_hz: float | None = None
) -> dict[str, Any]:
    """Build diagonal Y/Z matrices and W in the circuit's branch order."""
    if frequency_hz is not None and (not math.isfinite(frequency_hz) or frequency_hz < 0):
        raise ConstitutiveModelError("Frequency must be finite and non-negative")

    branch_count = len(circuit.branches)
    y_matrix = np.zeros((branch_count, branch_count), dtype=complex)
    z_matrix = np.zeros((branch_count, branch_count), dtype=complex)
    w_vector = np.zeros(branch_count, dtype=complex)
    row_sources: list[dict[str, Any]] = []

    for expected_index, branch in enumerate(circuit.branches):
        if branch.index != expected_index:
            raise ConstitutiveModelError(
                f"{branch.component_name}: expected branch index {expected_index}, got {branch.index}"
            )
        y, z, w, equation = branch_model(branch, frequency_hz)
        y_matrix[branch.index, branch.index] = y
        z_matrix[branch.index, branch.index] = z
        w_vector[branch.index] = w
        row_sources.append(
            {
                "row": branch.index,
                "branch_id": branch.id,
                "component_name": branch.component_name,
                "element_type": branch.element_type,
                "equation": equation,
                "source_line": branch.source_line,
                "line_number": branch.line_number,
            }
        )

    return {
        "schema_version": "1.0",
        "source_name": circuit.source_name,
        "analysis": "AC" if frequency_hz is not None else "DC",
        "frequency_hz": frequency_hz,
        "branch_order": [branch.id for branch in circuit.branches],
        "component_order": [branch.component_name for branch in circuit.branches],
        "Y": complex_matrix_to_json(y_matrix),
        "Z": complex_matrix_to_json(z_matrix),
        "W": complex_vector_to_json(w_vector),
        "shape": list(y_matrix.shape),
        "equations": row_sources,
        "convention": "Y*Vb + Z*I = W",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build branch constitutive matrices")
    parser.add_argument("circuit_json", help="Normalized circuit JSON")
    parser.add_argument("-o", "--output", required=True, help="Output matrices JSON")
    parser.add_argument("--frequency", type=float, help="Frequency in Hz; omit for DC")
    args = parser.parse_args()
    circuit = load_circuit(args.circuit_json)
    data = build_constitutive_matrices(circuit, args.frequency)
    Path(args.output).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Built Y/Z/W{tuple(data['shape'])} -> {args.output}")


if __name__ == "__main__":
    main()