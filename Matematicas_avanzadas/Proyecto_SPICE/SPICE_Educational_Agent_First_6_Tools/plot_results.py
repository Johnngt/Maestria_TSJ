#!/usr/bin/env python3
"""Create deterministic circuit-topology and AC response plots."""
from __future__ import annotations

import argparse
import cmath
import json
import math
from pathlib import Path
from typing import Any

import networkx as nx


class PlotResultsError(ValueError):
    """Raised when plot inputs do not contain the required data."""


def _topology_graph(topology: dict[str, Any]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for node in topology.get("nodes", []):
        if isinstance(node, dict):
            graph.add_node(str(node.get("id")), **node)
        else:
            graph.add_node(str(node))
    for index, edge in enumerate(topology.get("edges", [])):
        source = str(edge["node_from"])
        target = str(edge["node_to"])
        graph.add_edge(
            source,
            target,
            key=str(edge.get("key", edge.get("branch_id", index))),
            branch_id=edge.get("branch_id", edge.get("key", f"B{index + 1}")),
            component=edge.get("component", ""),
        )
    return graph


def _comparison_lookup(comparison: dict[str, Any] | None) -> dict[tuple[int, str], dict[str, Any]]:
    lookup: dict[tuple[int, str], dict[str, Any]] = {}
    if not comparison:
        return lookup
    for point in comparison.get("comparisons", []):
        for check in point.get("checks", []):
            lookup[(int(point.get("point", 0)), check.get("label", ""))] = check
    return lookup


def plot_results(
    results: dict[str, Any],
    output_dir: str | Path,
    topology: dict[str, Any] | None = None,
    comparison: dict[str, Any] | None = None,
    title: str = "SPICE Educational Agent",
) -> list[str]:
    """Render available topology, magnitude, and phase plots to PNG files."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    generated: list[str] = []

    if topology is not None:
        graph = _topology_graph(topology)
        if graph.number_of_nodes() == 0:
            raise PlotResultsError("Topology contains no nodes")
        position = nx.spring_layout(graph.to_undirected(), seed=42)
        figure, axis = plt.subplots(figsize=(9, 6))
        node_colors = [
            "#ed7d31" if graph.nodes[node].get("is_reference") else "#5b9bd5"
            for node in graph.nodes
        ]
        nx.draw_networkx_nodes(
            graph, position, node_color=node_colors, node_size=1000,
            edgecolors="#202020", ax=axis,
        )
        nx.draw_networkx_labels(
            graph, position, labels={node: f"N{node}" for node in graph.nodes},
            font_weight="bold", ax=axis,
        )
        nx.draw_networkx_edges(
            graph, position, arrows=True, arrowsize=18, edge_color="#555555",
            connectionstyle="arc3,rad=0.12", ax=axis,
        )
        for source, target, key, data in graph.edges(keys=True, data=True):
            start = position[source]
            end = position[target]
            midpoint_x = (start[0] + end[0]) / 2
            midpoint_y = (start[1] + end[1]) / 2
            axis.text(
                midpoint_x, midpoint_y,
                f"{data.get('branch_id', key)} {data.get('component', '')}".strip(),
                fontsize=8, bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
            )
        opamp_lines = [
            f"{item['name']} ideal: +N{item['node_plus']}, -N{item['node_minus']}, out N{item['node_out']}"
            for item in topology.get("opamps", [])
        ]
        if opamp_lines:
            axis.text(
                0.02, 0.98, "\n".join(opamp_lines), transform=axis.transAxes,
                va="top", bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "#555555"},
            )
        axis.set_title(f"{title}: topología orientada")
        axis.axis("off")
        figure.tight_layout()
        path = destination / "graph.png"
        figure.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(figure)
        generated.append(str(path))

    points = results.get("points", [])
    usable_points = [point for point in points if point.get("status") != "FAIL"]
    transfer_names = sorted(
        {name for point in usable_points for name in point.get("transfer_functions", {})}
    )
    if usable_points and transfer_names:
        frequencies = [float(point["frequency_hz"]) for point in usable_points]
        if any(frequency <= 0 for frequency in frequencies):
            raise PlotResultsError("Bode plots require positive frequencies")
        comparison_values = _comparison_lookup(comparison)

        magnitude_figure, magnitude_axis = plt.subplots(figsize=(9, 5))
        phase_figure, phase_axis = plt.subplots(figsize=(9, 5))
        for name in transfer_names:
            magnitude = [
                point.get("transfer_functions", {}).get(name, {}).get("magnitude_db")
                for point in usable_points
            ]
            phase = [
                point.get("transfer_functions", {}).get(name, {}).get("phase_deg")
                for point in usable_points
            ]
            magnitude_axis.semilogx(
                frequencies,
                [float("nan") if value is None else value for value in magnitude],
                label=name,
            )
            phase_axis.semilogx(
                frequencies,
                [float("nan") if value is None else value for value in phase],
                label=name,
            )
            reference_magnitude: list[float] = []
            reference_phase: list[float] = []
            has_reference = False
            for index, _point in enumerate(usable_points):
                check = comparison_values.get((index, name))
                if check and check.get("reference"):
                    reference_value = complex(
                        check["reference"]["real"], check["reference"]["imag"]
                    )
                    reference_magnitude.append(
                        20 * math.log10(abs(reference_value))
                        if abs(reference_value) else float("nan")
                    )
                    reference_phase.append(float(math.degrees(cmath.phase(reference_value))))
                    has_reference = True
                else:
                    reference_magnitude.append(float("nan"))
                    reference_phase.append(float("nan"))
            if has_reference:
                magnitude_axis.semilogx(
                    frequencies, reference_magnitude, "--", label=f"{name} referencia"
                )
                phase_axis.semilogx(
                    frequencies, reference_phase, "--", label=f"{name} referencia"
                )

        magnitude_axis.set_title(f"{title}: magnitud")
        magnitude_axis.set_xlabel("Frecuencia (Hz)")
        magnitude_axis.set_ylabel("Magnitud (dB)")
        magnitude_axis.grid(True, which="both", alpha=0.3)
        magnitude_axis.legend()
        magnitude_figure.tight_layout()
        magnitude_path = destination / "magnitude.png"
        magnitude_figure.savefig(magnitude_path, dpi=180)
        plt.close(magnitude_figure)
        generated.append(str(magnitude_path))

        phase_axis.set_title(f"{title}: fase")
        phase_axis.set_xlabel("Frecuencia (Hz)")
        phase_axis.set_ylabel("Fase (grados)")
        phase_axis.grid(True, which="both", alpha=0.3)
        phase_axis.legend()
        phase_figure.tight_layout()
        phase_path = destination / "phase.png"
        phase_figure.savefig(phase_path, dpi=180)
        plt.close(phase_figure)
        generated.append(str(phase_path))

    if not generated:
        raise PlotResultsError("No topology or transfer-function data was provided")
    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot topology and AC results")
    parser.add_argument("results_json")
    parser.add_argument("--topology")
    parser.add_argument("--comparison")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--title", default="SPICE Educational Agent")
    args = parser.parse_args()
    results = json.loads(Path(args.results_json).read_text(encoding="utf-8"))
    topology = json.loads(Path(args.topology).read_text(encoding="utf-8")) if args.topology else None
    comparison = json.loads(Path(args.comparison).read_text(encoding="utf-8")) if args.comparison else None
    generated = plot_results(results, args.output_dir, topology, comparison, args.title)
    print("Generated plots:")
    for path in generated:
        print(f"- {path}")


if __name__ == "__main__":
    main()