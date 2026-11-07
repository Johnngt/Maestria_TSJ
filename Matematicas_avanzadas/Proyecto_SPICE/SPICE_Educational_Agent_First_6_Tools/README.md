# SPICE Educational Agent Python Tools

Author: Dr. Francisco E. Rangel-Patiño

## Implemented scripts

The methodological guide lists the main tools in this order:

1. `parse_netlist.py`
2. `validate_netlist.py`
3. `build_circuit_model.py`
4. `build_oriented_graph.py`
5. `build_incidence_matrix.py`
6. `stamp_elements.py`
7. `build_constitutive_matrices.py`
8. `build_nodal_system.py`
9. `build_tableau_system.py`
10. `solve_linear_system.py`
11. `solve_ac_sweep.py`
12. `validate_solution.py`
13. `compare_reference.py`
14. `generate_report.py`
15. `plot_results.py`

The netlist validator and shared component-stamp module are implemented. The stamp module is used by both nodal assembly and constitutive matrix generation to keep their component models consistent. `build_mna_system.py` adds the project-specific ideal-op-amp extension with an auxiliary output-current unknown; this is a linear ideal model without rails or saturation, not portable SPICE syntax.

## Dependencies

```bash
python -m pip install numpy networkx matplotlib
```

## End-to-end example

Run these commands from the package directory:

```bash
python validate_netlist.py examples/current_source_resistive.cir -o artifacts/validation_netlist.json
python parse_netlist.py examples/current_source_resistive.cir -o artifacts/parsed.json
python build_circuit_model.py artifacts/parsed.json -o artifacts/circuit.json
python build_oriented_graph.py artifacts/circuit.json -o artifacts/topology.json --image artifacts/graph.png
python build_incidence_matrix.py artifacts/circuit.json -o artifacts/incidence.json --markdown artifacts/incidence.md --npz artifacts/incidence.npz
python build_nodal_system.py artifacts/circuit.json artifacts/incidence.json -o artifacts/nodal.json
python solve_linear_system.py artifacts/nodal.json artifacts/circuit.json -o artifacts/results.json
```

`parse_netlist.py` also invokes the validator before producing parsed data. The standalone validation report uses `PASS`/`FAIL` plus structured diagnostics (code, severity, line, and suggested action); the CLI exits non-zero on `FAIL`.

The project-only ideal-op-amp directive is `.OPAMP U1 NP NM OUT IDEAL`, where the terminals are non-inverting input, inverting input, and output. For circuits containing it, use MNA; nodal and Tableau assembly reject the directive rather than silently omit the device. Ideal op-amps have zero input current, `V(NP)=V(NM)` in the assumed linear operating region, and an unconstrained auxiliary output current. They do not model physical output limits or saturation.

The shared `stamp_elements.py` module defines the Tableau constitutive stamps and the nodal admittance/current-source stamps. Zero conductance is valid and produces a zero stamp; negative conductance is rejected.

For Tableau, build the constitutive matrices, assemble the Tableau system, and solve without a circuit argument:

```bash
python build_constitutive_matrices.py artifacts/circuit.json -o artifacts/constitutive.json
python build_tableau_system.py artifacts/circuit.json artifacts/incidence.json artifacts/constitutive.json -o artifacts/tableau.json
python solve_linear_system.py artifacts/tableau.json -o artifacts/tableau_results.json
python validate_solution.py artifacts/tableau.json artifacts/tableau_results.json -o artifacts/validation.json
```

For AC, use the parsed circuit's single `.AC` directive and provide any desired transfer functions in a JSON file. Select MNA for the `.OPAMP` extension:

```bash
python solve_ac_sweep.py artifacts/circuit.json artifacts/incidence.json --formulation MNA --transfers artifacts/transfers.json -o artifacts/ac_results.json
```

To inspect and solve a single MNA point, assemble the system with `build_mna_system.py`, then pass both the system and circuit to the generic solver CLI; validate that solution with `validate_solution.py`.

For validated AC sweeps, `generate_report.py` also renders the complex nodal-voltage vector `Vn` for every frequency when per-point solutions are present, alongside transfer magnitude/phase data.


## Tests

Run the original DC integration test and the extended tool regressions from this directory:

```bash
python test_integration.py
python -m unittest test_extended_tools.py
```

## MVP limitation

`build_nodal_system.py` intentionally rejects ideal voltage sources and ideal op-amps because classical nodal analysis cannot represent their unknown currents/constraints directly. Use Tableau for supported ideal voltage-source networks, or MNA for the project ideal-op-amp extension.

## Sign convention

- Branch orientation follows the node order written in the netlist.
- `+1` in the incidence matrix means the branch leaves a node.
- `-1` means the branch enters a node.
- Current source values follow the same branch orientation.
