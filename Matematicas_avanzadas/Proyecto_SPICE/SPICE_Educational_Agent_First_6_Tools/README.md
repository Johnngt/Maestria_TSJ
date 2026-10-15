# SPICE Educational Agent Python Tools

Author: Dr. Francisco E. Rangel-Patiño

## Implemented scripts

The methodological guide lists the main tools in this order:

1. `parse_netlist.py`
2. `validate_netlist.py` (planned)
3. `build_circuit_model.py`
4. `build_oriented_graph.py`
5. `build_incidence_matrix.py`
6. `stamp_elements.py` (its branch models are currently implemented in `build_constitutive_matrices.py`)
7. `build_constitutive_matrices.py`
8. `build_nodal_system.py`
9. `build_tableau_system.py`
10. `solve_linear_system.py`
11. `solve_ac_sweep.py`
12. `validate_solution.py`
13. `compare_reference.py`
14. `generate_report.py`
15. `plot_results.py`

Scripts 1-5 and 8, 10 existed in the original package. Scripts 7, 9, and 11-15 are implemented in this package. Scripts marked as planned are not implemented yet.

## Dependencies

```bash
python -m pip install numpy networkx matplotlib
```

## End-to-end example

Run these commands from the package directory:

```bash
python parse_netlist.py examples/current_source_resistive.cir -o artifacts/parsed.json
python build_circuit_model.py artifacts/parsed.json -o artifacts/circuit.json
python build_oriented_graph.py artifacts/circuit.json -o artifacts/topology.json --image artifacts/graph.png
python build_incidence_matrix.py artifacts/circuit.json -o artifacts/incidence.json --markdown artifacts/incidence.md --npz artifacts/incidence.npz
python build_nodal_system.py artifacts/circuit.json artifacts/incidence.json -o artifacts/nodal.json
python solve_linear_system.py artifacts/nodal.json artifacts/circuit.json -o artifacts/results.json
```

For Tableau, build the constitutive matrices, assemble the Tableau system, and solve without a circuit argument:

```bash
python build_constitutive_matrices.py artifacts/circuit.json -o artifacts/constitutive.json
python build_tableau_system.py artifacts/circuit.json artifacts/incidence.json artifacts/constitutive.json -o artifacts/tableau.json
python solve_linear_system.py artifacts/tableau.json -o artifacts/tableau_results.json
python validate_solution.py artifacts/tableau.json artifacts/tableau_results.json -o artifacts/validation.json
```

For AC, use the parsed circuit's single `.AC` directive and provide any desired transfer functions in a JSON file:

```bash
python solve_ac_sweep.py artifacts/circuit.json artifacts/incidence.json --formulation NODAL -o artifacts/ac_results.json
```

## Tests

Run the original DC integration test and the extended tool regressions from this directory:

```bash
python test_integration.py
python -m unittest test_extended_tools.py
```

## MVP limitation

`build_nodal_system.py` intentionally rejects ideal voltage sources because classical nodal analysis cannot represent their unknown current directly. Use the future Tableau or MNA tools for those circuits.

## Sign convention

- Branch orientation follows the node order written in the netlist.
- `+1` in the incidence matrix means the branch leaves a node.
- `-1` means the branch enters a node.
- Current source values follow the same branch orientation.
