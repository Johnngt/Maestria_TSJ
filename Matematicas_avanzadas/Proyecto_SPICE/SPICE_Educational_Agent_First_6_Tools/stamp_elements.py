#!/usr/bin/env python3
"""Shared constitutive and nodal stamps for supported linear branches."""
from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Any


class StampError(ValueError):
    """Raised when a branch cannot be represented by an approved stamp."""


@dataclass(frozen=True)
class ConstitutiveStamp:
    y: complex
    z: complex
    w: complex
    equation: str


@dataclass(frozen=True)
class NodalStamp:
    admittance: complex | None
    current: complex | None


def _source_value(branch: Any, frequency_hz: float | None) -> complex:
    source_kind = (branch.source_kind or "DC").upper()
    if frequency_hz is None:
        return complex(branch.value_si) if source_kind == "DC" else 0.0 + 0.0j
    if source_kind != "AC":
        return 0.0 + 0.0j

    magnitude = branch.ac_magnitude
    if magnitude is None:
        magnitude = branch.value_si
    phase_deg = branch.ac_phase_deg or 0.0
    if (
        not math.isfinite(float(magnitude))
        or float(magnitude) < 0
        or not math.isfinite(float(phase_deg))
    ):
        raise StampError(
            f"{branch.component_name}: AC magnitude must be non-negative and "
            "AC phase must be finite"
        )
    return cmath.rect(float(magnitude), math.radians(float(phase_deg)))


def constitutive_stamp(
    branch: Any, frequency_hz: float | None = None
) -> ConstitutiveStamp:
    """Return a branch stamp for Y*Vb + Z*I = W."""
    element_type = branch.element_type.upper()
    value = float(branch.value_si)
    if not math.isfinite(value):
        raise StampError(f"{branch.component_name}: value must be finite")

    if element_type == "R":
        if value <= 0:
            raise StampError(f"{branch.component_name}: resistance must be positive")
        return ConstitutiveStamp(1.0, -value, 0.0, "V - R*I = 0")
    if element_type == "G":
        if value < 0:
            raise StampError(f"{branch.component_name}: conductance cannot be negative")
        return ConstitutiveStamp(value, -1.0, 0.0, "G*V - I = 0")
    if element_type == "C":
        if value <= 0:
            raise StampError(f"{branch.component_name}: capacitance must be positive")
        if frequency_hz is None:
            return ConstitutiveStamp(0.0, 1.0, 0.0, "I = 0 (DC steady state)")
        s = 1j * 2.0 * math.pi * frequency_hz
        return ConstitutiveStamp(s * value, -1.0, 0.0, "s*C*V - I = 0")
    if element_type == "L":
        if value <= 0:
            raise StampError(f"{branch.component_name}: inductance must be positive")
        if frequency_hz is None:
            return ConstitutiveStamp(1.0, 0.0, 0.0, "V = 0 (DC steady state)")
        s = 1j * 2.0 * math.pi * frequency_hz
        return ConstitutiveStamp(1.0, -s * value, 0.0, "V - s*L*I = 0")
    if element_type == "V":
        return ConstitutiveStamp(1.0, 0.0, _source_value(branch, frequency_hz), "V = E")
    if element_type == "I":
        return ConstitutiveStamp(0.0, 1.0, _source_value(branch, frequency_hz), "I = J")
    raise StampError(
        f"{branch.component_name}: unsupported element type {branch.element_type!r}"
    )


def nodal_stamp(branch: Any, frequency_hz: float | None = None) -> NodalStamp:
    """Return a passive admittance or oriented current-source injection."""
    stamp = constitutive_stamp(branch, frequency_hz)
    element_type = branch.element_type.upper()
    if element_type == "I":
        return NodalStamp(admittance=None, current=stamp.w / stamp.z)
    if element_type == "V":
        raise StampError(
            f"{branch.component_name}: ideal voltage source is incompatible with "
            "classical nodal analysis; use Tableau or MNA"
        )
    if stamp.z == 0:
        raise StampError(
            f"{branch.component_name}: its DC short-circuit model cannot be "
            "represented by classical nodal analysis; use Tableau or MNA"
        )
    return NodalStamp(admittance=-stamp.y / stamp.z, current=None)
