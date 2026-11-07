#!/usr/bin/env python3
"""Generate a traceable Markdown report from calculated run artifacts."""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


class ReportGenerationError(ValueError):
    """Raised when a report bundle is incomplete or mixes different runs."""


def _format_number(value: Any) -> str:
    if isinstance(value, dict) and "real" in value:
        real = float(value["real"])
        imag = float(value.get("imag", 0.0))
        if abs(imag) < 1e-14:
            return f"{real:.8g}"
        sign = "+" if imag >= 0 else "-"
        return f"{real:.8g} {sign} j{abs(imag):.8g}"
    if isinstance(value, (int, float)):
        return f"{value:.8g}"
    return str(value)


def _matrix_table(
    matrix: list[list[Any]], row_labels: list[str], column_labels: list[str]
) -> str:
    if len(matrix) != len(row_labels) or any(len(row) != len(column_labels) for row in matrix):
        raise ReportGenerationError("Matrix labels do not match matrix dimensions")
    header = "| | " + " | ".join(column_labels) + " |"
    separator = "|---|" + "---|" * len(column_labels)
    rows = [
        "| " + label + " | " + " | ".join(_format_number(value) for value in row) + " |"
        for label, row in zip(row_labels, matrix)
    ]
    return "\n".join([header, separator, *rows])

def _display_width(value: str) -> int:
    return sum(
        0 if unicodedata.combining(char) else
        2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
        for char in value
    )


def _split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _align_markdown_tables(lines: list[str]) -> list[str]:
    """Pad Markdown table cells so each column aligns with its header and rule."""
    aligned: list[str] = []
    index = 0
    while index < len(lines):
        if not (lines[index].startswith("|") and lines[index].endswith("|")):
            aligned.append(lines[index])
            index += 1
            continue

        end = index
        while end < len(lines) and lines[end].startswith("|") and lines[end].endswith("|"):
            end += 1
        table_lines = lines[index:end]
        rows = [_split_markdown_row(line) for line in table_lines]
        column_count = len(rows[0])
        if any(len(row) != column_count for row in rows):
            raise ReportGenerationError("Markdown table rows have inconsistent column counts")

        separator_index = next(
            (row_index for row_index, row in enumerate(rows)
             if all(re.fullmatch(r":?-{3,}:?", cell) for cell in row)),
            None,
        )
        if separator_index is None:
            raise ReportGenerationError("Markdown table is missing a valid alignment row")
        separator = rows[separator_index]
        widths = [3] * column_count
        for row_index, row in enumerate(rows):
            if row_index == separator_index:
                continue
            for column, cell in enumerate(row):
                widths[column] = max(widths[column], _display_width(cell))

        for row_index, row in enumerate(rows):
            if row_index == separator_index:
                cells = []
                for width, rule in zip(widths, separator):
                    left = rule.startswith(":")
                    right = rule.endswith(":")
                    dashes = "-" * max(3, width - int(left) - int(right))
                    cells.append((":" if left else "") + dashes + (":" if right else ""))
            else:
                cells = []
                for column, cell in enumerate(row):
                    padding = widths[column] - _display_width(cell)
                    rule = separator[column]
                    left = rule.startswith(":")
                    right = rule.endswith(":")
                    if left and right:
                        before = padding // 2
                        after = padding - before
                        cells.append(" " * before + cell + " " * after)
                    elif right:
                        cells.append(" " * padding + cell)
                    else:
                        cells.append(cell + " " * padding)
            aligned.append("| " + " | ".join(cells) + " |")
        index = end
    return aligned


def _vector_table(values: list[Any], labels: list[str], heading: str) -> str:
    if len(values) != len(labels):
        raise ReportGenerationError(f"{heading} labels do not match vector length")
    return "\n".join(
        ["| Label | Value |", "|---|---|"]
        + [f"| {label} | {_format_number(value)} |" for label, value in zip(labels, values)]
    )


def _check_bundle_consistency(bundle: dict[str, Any]) -> None:
    artifacts = [
        bundle.get(name)
        for name in ("circuit", "topology", "incidence", "system", "solution", "validation", "comparison", "ac_sweep")
    ]
    artifacts = [item for item in artifacts if isinstance(item, dict)]
    run_ids = {item["run_id"] for item in artifacts if item.get("run_id") is not None}
    if bundle.get("run_id") is not None:
        run_ids.add(bundle["run_id"])
    if len(run_ids) > 1:
        raise ReportGenerationError("Bundle contains artifacts from different run_id values")
    source_names = {item["source_name"] for item in artifacts if item.get("source_name") is not None}
    if len(source_names) > 1:
        raise ReportGenerationError("Bundle contains artifacts from different source nets")
    validation = bundle.get("validation")
    ac_sweep = bundle.get("ac_sweep")
    if not isinstance(validation, dict) and not isinstance(ac_sweep, dict):
        raise ReportGenerationError("A validation artifact or validated AC sweep is required")


def generate_report(bundle: dict[str, Any]) -> str:
    """Render a Markdown report; all numerical content comes from input artifacts."""
    _check_bundle_consistency(bundle)
    circuit = bundle.get("circuit", {})
    topology = bundle.get("topology", {})
    incidence = bundle.get("incidence", {})
    system = bundle.get("system", {})
    solution = bundle.get("solution", {})
    validation = bundle.get("validation", {})
    comparison = bundle.get("comparison", {})
    ac_sweep = bundle.get("ac_sweep", {})
    report_lines = [
        "# Reporte de simulación de circuito",
        "",
        f"- **Fuente:** {bundle.get('source_name', circuit.get('source_name', '<unknown>'))}",
        f"- **Método:** {system.get('formulation', solution.get('formulation', ac_sweep.get('formulation', 'no especificado')))}",
        f"- **Ejecución:** {bundle.get('run_id', '<sin run_id>')}",
        f"- **Estado:** {validation.get('status', ac_sweep.get('status', 'sin validar'))}",
        "",
        "## Netlist original",
        "",
    ]
    netlist_text = bundle.get("netlist_text")
    if netlist_text is None:
        branches = circuit.get("branches", [])
        netlist_text = "\n".join(branch.get("source_line", "") for branch in branches).strip()
    report_lines.extend(["```spice", netlist_text or "(no adjunto)", "```", ""])

    elements = circuit.get("branches", circuit.get("elements", []))
    if elements:
        report_lines.extend(
            [
                "## Componentes normalizados",
                "",
                "| Componente | Tipo | Desde | Hacia | Valor SI | Unidad | Rama | L?nea |",
                "|---|---|---|---|---:|---|---|---:|",
            ]
        )
        for item in elements:
            report_lines.append(
                "| {name} | {type} | {node_from} | {node_to} | {value} | {unit} | {branch} | {line} |".format(
                    name=item.get("component_name", item.get("name", "")),
                    type=item.get("element_type", item.get("type", "")),
                    node_from=item.get("node_from", ""),
                    node_to=item.get("node_to", ""),
                    value=_format_number(item.get("value_si", "")),
                    unit=item.get("unit", ""),
                    branch=item.get("id", item.get("branch_id", "")),
                    line=item.get("line_number", ""),
                )
            )
        report_lines.append("")
    opamps = circuit.get("opamps", [])
    if opamps:
        report_lines.extend(
            [
                "## Amplificadores operacionales ideales",
                "",
                "Modelo MNA ideal lineal: corrientes de entrada nulas, restriccion "
                "V(n+)=V(n-) y corriente auxiliar en la salida. No modela rieles ni saturacion.",
                "",
                "| Op-amp | Entrada + | Entrada - | Salida | Linea |",
                "|---|---|---|---|---:|",
            ]
        )
        for opamp in opamps:
            report_lines.append(
                f"| {opamp.get('name', '')} | {opamp.get('node_plus', '')} | "
                f"{opamp.get('node_minus', '')} | {opamp.get('node_out', '')} | "
                f"{opamp.get('line_number', '')} |"
            )
        report_lines.append("")

    nodes = circuit.get("nodes", [])
    if nodes:
        report_lines.extend(["## Nodos", "", "| Nodo | Referencia | Índice completo | Índice reducido |", "|---|:---:|---:|---:|"])
        for node in nodes:
            if isinstance(node, dict):
                report_lines.append(
                    f"| {node.get('id', '')} | {'sí' if node.get('is_reference') else 'no'} | "
                    f"{node.get('index_full', '')} | {node.get('index_reduced', '')} |"
                )
            else:
                report_lines.append(f"| {node} | {'sí' if node == circuit.get('reference_node', '0') else 'no'} | | |")
        report_lines.append("")

    if topology:
        report_lines.extend(
            [
                "## Topología",
                "",
                f"Conectado: **{topology.get('is_connected', 'no disponible')}**",
                "",
                "| Desde | Hacia | Rama | Componente |",
                "|---|---|---|---|",
            ]
        )
        for edge in topology.get("edges", []):
            report_lines.append(
                f"| {edge.get('node_from', '')} | {edge.get('node_to', '')} | "
                f"{edge.get('branch_id', edge.get('key', ''))} | {edge.get('component', '')} |"
            )
        report_lines.append("")

    if incidence:
        matrix = incidence.get("A_reduced", [])
        rows = incidence.get("node_order_reduced", [])
        columns = incidence.get("branch_order", [])
        if matrix:
            report_lines.extend(["## Matriz de incidencia reducida", "", _matrix_table(matrix, rows, columns), ""])

    constitutive = bundle.get("constitutive", system)
    branch_order = constitutive.get("branch_order", system.get("branch_order", []))
    if constitutive.get("equations"):
        report_lines.extend(
            [
                "## Ecuaciones constitutivas",
                "",
                "| Rama | Componente | Ecuación | Línea de origen |",
                "|---|---|---|---:|",
            ]
        )
        for row in constitutive["equations"]:
            report_lines.append(
                f"| {row.get('branch_id', '')} | {row.get('component_name', '')} | "
                f"{row.get('equation', '')} | {row.get('line_number', '')} |"
            )
        report_lines.append("")
    for key in ("Y", "Z"):
        if key in constitutive:
            report_lines.extend(
                [f"### Matriz {key}", "", _matrix_table(constitutive[key], branch_order, branch_order), ""]
            )
    if "W" in constitutive:
        report_lines.extend(
            ["### Vector W", "", _vector_table(constitutive["W"], branch_order, "W"), ""]
        )

    matrix = system.get("M", system.get("T"))
    rhs = system.get("rhs", system.get("Wp"))
    if matrix is not None and rhs is not None:
        row_labels = system.get("equation_order", [f"eq[{index}]" for index in range(len(matrix))])
        column_labels = system.get("unknown_order", [f"x[{index}]" for index in range(len(matrix))])
        report_lines.extend(
            [
                "## Sistema ensamblado",
                "",
                f"Formulación: `{system.get('formulation', 'nodal')}`; dimensiones: `{len(matrix)} × {len(matrix[0]) if matrix else 0}`.",
                "",
                _matrix_table(matrix, row_labels, column_labels),
                "",
                "### Vector del lado derecho",
                "",
                _vector_table(rhs, row_labels, "rhs"),
                "",
            ]
        )

    if ac_sweep:
        report_lines.extend(
            [
                "## Resultados AC",
                "",
                f"Barrido `{ac_sweep.get('sweep', {}).get('type', '')}`; estado global: **{ac_sweep.get('status', 'sin estado')}**.",
                "",
                "| Frecuencia (Hz) | Estado | Transferencias calculadas |",
                "|---:|---|---|",
            ]
        )
        for point in ac_sweep.get("points", []):
            transfers = point.get("transfer_functions", {})
            values = "; ".join(
                f"{name}: magnitud={_format_number(item.get('magnitude'))}, "
                f"fase={_format_number(item.get('phase_deg'))} grados, "
                f"dB={_format_number(item.get('magnitude_db'))}"
                for name, item in transfers.items()
            ) or "(sin transferencias solicitadas)"
            report_lines.append(
                f"| {_format_number(point.get('frequency_hz'))} | {point.get('status', '')} | {values} |"
            )
        report_lines.append("")
        voltage_rows = []
        voltage_labels: list[str] = []
        for point in ac_sweep.get("points", []):
            node_voltages = point.get("solution", {}).get("node_voltages", [])
            voltage_rows.append((point, node_voltages))
            for record in node_voltages:
                label = record.get("label")
                if label and label not in voltage_labels:
                    voltage_labels.append(label)
        if voltage_labels:
            report_lines.extend(
                [
                    "### Vector de voltajes nodales Vn por frecuencia",
                    "",
                    "Fasores complejos en V; se excluye el nodo de referencia 0. "
                    "Los puntos sin solucion conservan su estado y se indican como `n/a`.",
                    "",
                    "| Frecuencia (Hz) | Estado | "
                    + " | ".join(f"{label} (V)" for label in voltage_labels)
                    + " |",
                    "|---:|---|"
                    + "---:|" * len(voltage_labels),
                ]
            )
            for point, records in voltage_rows:
                values_by_label = {record.get("label"): record for record in records}
                values = [
                    _format_number(values_by_label[label])
                    if label in values_by_label
                    else "n/a"
                    for label in voltage_labels
                ]
                report_lines.append(
                    f"| {_format_number(point.get('frequency_hz'))} | "
                    f"{point.get('status', '')} | " + " | ".join(values) + " |"
                )
            report_lines.append("")
    elif solution:
        report_lines.extend(["## Resultados", ""])
        for field, heading in (
            ("node_voltages", "Voltajes nodales"),
            ("branch_voltages", "Voltajes de rama"),
            ("branch_currents", "Corrientes de rama"),
            ("unknowns", "Incógnitas"),
        ):
            records = solution.get(field, [])
            if records:
                report_lines.extend([f"### {heading}", "", "| Variable | Real | Imaginaria | Unidad |", "|---|---:|---:|---|"])
                for record in records:
                    report_lines.append(
                        f"| {record.get('label', '')} | {_format_number(record.get('real'))} | "
                        f"{_format_number(record.get('imag', 0.0))} | {record.get('unit', '')} |"
                    )
                report_lines.append("")

    if validation:
        report_lines.extend(
            [
                "## Validación",
                "",
                f"**Estado: {validation.get('status', 'sin estado')}**",
                "",
                "| Métrica | Norma | Umbral | Resultado |",
                "|---|---:|---:|---|",
            ]
        )
        for check in validation.get("checks", []):
            report_lines.append(
                f"| {check.get('name', '')} | {_format_number(check.get('norm', ''))} | "
                f"{_format_number(check.get('threshold', ''))} | {'PASS' if check.get('passed') else 'FAIL'} |"
            )
        if validation.get("condition_number") is not None:
            report_lines.append(f"\nNúmero de condición: `{_format_number(validation['condition_number'])}`.")
        report_lines.append("")

    if comparison:
        report_lines.extend(
            [
                "## Comparación de referencia",
                "",
                f"Estado: **{comparison.get('status', 'sin estado')}**",
                "",
                "| Punto | Frecuencia (Hz) | Estado | Variables comparadas |",
                "|---:|---:|---|---:|",
            ]
        )
        for item in comparison.get("comparisons", []):
            report_lines.append(
                f"| {item.get('point', '')} | {_format_number(item.get('frequency_hz'))} | "
                f"{item.get('status', '')} | {len(item.get('checks', []))} |"
            )
        report_lines.append("")

    warnings = list(bundle.get("warnings", []))
    for artifact in (validation, comparison, ac_sweep):
        warnings.extend(artifact.get("diagnostics", []))
    report_lines.extend(["## Advertencias y limitaciones", ""])
    report_lines.extend([f"- {warning}" for warning in warnings] or ["- Ninguna registrada."])
    report_lines.extend(["", "## Artefactos y reproducibilidad", ""])
    artifacts = bundle.get("artifacts", [])
    report_lines.extend([f"- `{item}`" for item in artifacts] or ["- El bundle no enumeró archivos de artefactos."])
    report_lines.append("")
    return "\n".join(_align_markdown_tables("\n".join(report_lines).splitlines()))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a report from a validated run bundle")
    parser.add_argument("bundle_json")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    bundle = json.loads(Path(args.bundle_json).read_text(encoding="utf-8"))
    report = generate_report(bundle)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Generated report -> {args.output}")


if __name__ == "__main__":
    main()