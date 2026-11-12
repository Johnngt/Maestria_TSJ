# Partial Tableau for the target circuit (10 Hz)

> **Important:** this system excludes U1 (`.OPAMP IDEAL`). It does not model or solve the complete circuit; MNA remains the valid formulation for the complete circuit.

- Source: `circuito_objetivo_tableau_parcial_sin_U1.cir` (derived copy; the op-amp was explicitly excluded).
- Analysis: AC, 10 Hz.
- Assembled system: 19 x 19; branches in order: B1, B2, B3, B4, B5, B6, B7.
- Partial solution validation: **PASS**; this status applies only to the reduced system.
- Unknown blocks: `Vb`, `I`, `Vn`; equation blocks: `KVL`, constitutive, `KCL`.
- Presentation labels remove the tools' auxiliary `N` prefix from node labels. Original JSON labels are unchanged.

## Numeric matrix T

Entries use the values from `tableau_partial_10Hz.json`; `j` denotes the imaginary part. Row and column order follows the assembler artifact.

| Equation / Unknown | V(B1) | V(B2) | V(B3) | V(B4) | V(B5) | V(B6) | V(B7) | I(B1) | I(B2) | I(B3) | I(B4) | I(B5) | I(B6) | I(B7) | V(IN) | V(N1) | V(NM) | V(NP) | V(OUT) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| KVL(B1) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 0 | 0 | 0 |
| KVL(B2) | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 1 | 0 | 0 | 0 |
| KVL(B3) | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 1 | 0 |
| KVL(B4) | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 0 | 1 |
| KVL(B5) | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 |
| KVL(B6) | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | -1 |
| KVL(B7) | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 0 |
| CONSTITUTIVE(B1) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CONSTITUTIVE(B2) | 0 | 6.28319e-06j | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CONSTITUTIVE(B3) | 0 | 0 | 6.28319e-06j | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CONSTITUTIVE(B4) | 0 | 0 | 0 | 0.000787402 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CONSTITUTIVE(B5) | 0 | 0 | 0 | 0 | 0.000434783 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CONSTITUTIVE(B6) | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | -2300 | 0 | 0 | 0 | 0 | 0 | 0 |
| CONSTITUTIVE(B7) | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | -1270 | 0 | 0 | 0 | 0 | 0 |
| KCL(IN) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| KCL(N1) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| KCL(NM) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 1 | 0 | 0 | 0 | 0 | 0 |
| KCL(NP) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| KCL(OUT) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

The image `tableau_partial_T_colored_blocks_10Hz.png` colors the nine equation-block x unknown-block regions.

## Artifacts

- `circuit_tableau_partial.json` and `incidence_tableau_partial.json`: derived model retaining branch/node order and excluding only the op-amp directive.
- `constitutive_tableau_partial_10Hz.json`: constitutive matrices Y/Z/W.
- `tableau_partial_10Hz.json`: assembled system T*X = Wp.
- `tableau_partial_solution_10Hz.json` and `tableau_partial_validation_10Hz.json`: reduced-system solution and checks.
- `mna_system_10Hz.json` and `ac_results.json`: complete-circuit MNA artifacts; unchanged.
