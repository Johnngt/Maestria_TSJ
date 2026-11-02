#!/usr/bin/env python3
"""Validate the supported educational SPICE netlist subset."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from parse_netlist import NetlistParseError, parse_component, parse_directive


def validate_netlist_text(text: str, source_name: str = "<memory>") -> dict[str, Any]:
    """Collect line-level and circuit-level diagnostics without stopping early."""
    diagnostics: list[dict[str, Any]] = []
    elements: list[dict[str, Any]] = []
    directives: list[dict[str, Any]] = []
    names: set[str] = set()
    saw_end = False

    def add(
        severity: str,
        code: str,
        message: str,
        line_number: int | None = None,
        suggestion: str | None = None,
    ) -> None:
        item: dict[str, Any] = {
            "severity": severity,
            "code": code,
            "message": message,
        }
        if line_number is not None:
            item["line_number"] = line_number
        if suggestion:
            item["suggestion"] = suggestion
        diagnostics.append(item)

    for line_number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("*"):
            continue
        if saw_end:
            break
        tokens = stripped.split()
        if stripped.startswith("."):
            try:
                directive = parse_directive(tokens, line_number, raw)
            except (NetlistParseError, ValueError, OverflowError) as error:
                add(
                    "error",
                    "INVALID_DIRECTIVE",
                    str(error),
                    line_number,
                    "Corrija la directiva según la gramática documentada (.OP, .AC o .END).",
                )
                continue
            directives.append(directive)
            saw_end = directive["command"] == "END"
            continue

        try:
            element = parse_component(tokens, line_number, raw)
        except (NetlistParseError, ValueError, OverflowError) as error:
            add(
                "error",
                "INVALID_ELEMENT",
                str(error),
                line_number,
                "Revise el designador, terminales, valor, unidades y cantidad de tokens.",
            )
            continue

        canonical_name = element["name"].upper()
        if canonical_name in names:
            add(
                "error",
                "DUPLICATE_COMPONENT",
                f"Duplicate component name {element['name']!r}.",
                line_number,
                "Use un identificador único para cada componente.",
            )
        else:
            names.add(canonical_name)
        if element["node_from"] == element["node_to"]:
            add(
                "error",
                "SAME_TERMINAL_NODE",
                f"{element['name']}: both terminals connect to node {element['node_from']!r}.",
                line_number,
                "Conecte los terminales a nodos distintos o retire la rama degenerada.",
            )
        if element["type"] in {"V", "I"} and element["source_kind"] == "AC":
            magnitude = element["ac_magnitude"]
            phase = element["ac_phase_deg"]
            if magnitude is None or not math.isfinite(float(magnitude)) or magnitude < 0:
                add(
                    "error",
                    "INVALID_AC_MAGNITUDE",
                    f"{element['name']}: AC magnitude must be finite and non-negative.",
                    line_number,
                    "Use una magnitud AC finita mayor o igual que cero.",
                )
            if phase is None or not math.isfinite(float(phase)):
                add(
                    "error",
                    "INVALID_AC_PHASE",
                    f"{element['name']}: AC phase must be finite.",
                    line_number,
                    "Use una fase AC finita en grados.",
                )
        elements.append(element)

    if not elements:
        add(
            "error",
            "NO_SUPPORTED_ELEMENTS",
            "The netlist contains no valid supported elements.",
            suggestion="Agregue al menos un componente lineal soportado.",
        )
    else:
        nodes = {element["node_from"] for element in elements}
        nodes.update(element["node_to"] for element in elements)
        if "0" not in nodes:
            add(
                "error",
                "MISSING_REFERENCE_NODE",
                "Reference node 0/GND is not present.",
                suggestion="Conecte el circuito al nodo 0 o use el alias GND.",
            )

    ac_directives = [item for item in directives if item["command"] == "AC"]
    if len(ac_directives) > 1:
        for directive in ac_directives[1:]:
            add(
                "error",
                "MULTIPLE_AC_DIRECTIVES",
                "Only one .AC directive is supported per netlist.",
                directive["line_number"],
                "Conserve una sola directiva .AC por ejecución.",
            )
    if elements and not saw_end:
        add(
            "warning",
            "MISSING_END_DIRECTIVE",
            ".END directive not found; the file will be parsed to its end.",
            suggestion="Agregue .END para delimitar explícitamente el netlist.",
        )

    status = "FAIL" if any(item["severity"] == "error" for item in diagnostics) else "PASS"
    return {
        "schema_version": "1.0",
        "source_name": source_name,
        "status": status,
        "diagnostics": diagnostics,
    }


def validate_netlist_file(path: str | Path) -> dict[str, Any]:
    input_path = Path(path)
    return validate_netlist_text(
        input_path.read_text(encoding="utf-8"),
        input_path.name,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an educational SPICE netlist")
    parser.add_argument("netlist", help="Input .cir/.sp/.net file")
    parser.add_argument("-o", "--output", required=True, help="Output validation JSON")
    args = parser.parse_args()
    report = validate_netlist_file(args.netlist)
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Netlist validation {report['status']} -> {args.output}")
    for diagnostic in report["diagnostics"]:
        location = (
            f"line {diagnostic['line_number']}: "
            if "line_number" in diagnostic
            else ""
        )
        print(
            f"{diagnostic['severity'].upper()} {location}"
            f"{diagnostic['message']}"
        )
        if diagnostic.get("suggestion"):
            print(f"  Suggestion: {diagnostic['suggestion']}")
    if report["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
