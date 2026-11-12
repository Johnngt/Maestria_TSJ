# Complete Tableau is not applicable to this run

The netlist contains `.OPAMP U1 NP NM OUT IDEAL`. The project-approved model for this element is MNA; the op-amp is not a passive branch and the Tableau assembler rejects the complete circuit. A partial matrix must not be presented as representing or solving the complete circuit.

Following the recorded lessons, a separate partial Tableau was assembled at 10 Hz for the seven two-terminal branches, excluding U1 from a derived copy of the model. The partial matrix and colored visualization are in `tableau_partial_10Hz.md` and `tableau_partial_T_colored_blocks_10Hz.png`. Its reduced system/solution validated, but it does not replace MNA.

The complete-circuit MNA matrix is `mna_system_10Hz.json`; the MNA AC sweep is `ac_results.json`.
