# First Six Python Tools for the SPICE Educational Agent

Author: Dr. Francisco E. Rangel-Patiño

## Included scripts

1. `parse_netlist.py`
2. `build_circuit_model.py`
3. `build_oriented_graph.py`
4. `build_incidence_matrix.py`
5. `build_nodal_system.py`
6. `solve_linear_system.py`

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

## MVP limitation

`build_nodal_system.py` intentionally rejects ideal voltage sources because classical nodal analysis cannot represent their unknown current directly. Use the future Tableau or MNA tools for those circuits.

## Sign convention

- Branch orientation follows the node order written in the netlist.
- `+1` in the incidence matrix means the branch leaves a node.
- `-1` means the branch enters a node.
- Current source values follow the same branch orientation.
