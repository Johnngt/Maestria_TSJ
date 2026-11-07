# Reporte de simulación de circuito

- **Fuente:** opamp_active_filter.cir
- **Método:** MNA
- **Ejecución:** opamp_filter_20261102
- **Estado:** PASS

## Netlist original

```spice
* Ideal non-inverting active filter; project-specific .OPAMP extension
V1 IN 0 AC 20 0
C1 IN N1 10n
C2 N1 NP 10n
G1 N1 OUT 100u
G2 NP 0 100u
RA NM 0 10k
RB OUT NM 10k
.OPAMP U1 NP NM OUT IDEAL
.AC DEC 10 1 1Meg
.END

```

## Componentes normalizados

| Componente | Tipo | Desde | Hacia | Valor SI | Unidad | Rama | Línea |
|---|---|---|---|---:|---|---|---:|
| V1 | V | IN | 0 | 20 | volt | B1 | 2 |
| C1 | C | IN | N1 | 1e-08 | farad | B2 | 3 |
| C2 | C | N1 | NP | 1e-08 | farad | B3 | 4 |
| G1 | G | N1 | OUT | 0.0001 | siemens | B4 | 5 |
| G2 | G | NP | 0 | 0.0001 | siemens | B5 | 6 |
| RA | R | NM | 0 | 10000 | ohm | B6 | 7 |
| RB | R | OUT | NM | 10000 | ohm | B7 | 8 |

## Amplificadores operacionales ideales

Modelo MNA ideal lineal: corrientes de entrada nulas, restriccion V(n+)=V(n-) y corriente auxiliar en la salida. No modela rieles ni saturacion.

| Op-amp | Entrada + | Entrada - | Salida | Linea |
|---|---|---|---|---:|
| U1 | NP | NM | OUT | 9 |

## Nodos

| Nodo | Referencia | Índice completo | Índice reducido |
|---|:---:|---:|---:|
| 0 | sí | 0 | None |
| IN | no | 1 | 0 |
| N1 | no | 2 | 1 |
| NM | no | 3 | 2 |
| NP | no | 4 | 3 |
| OUT | no | 5 | 4 |

## Topología

Conectado: **True**

| Desde | Hacia | Rama | Componente |
|---|---|---|---|
| IN | 0 | B1 | V1 |
| IN | N1 | B2 | C1 |
| N1 | NP | B3 | C2 |
| N1 | OUT | B4 | G1 |
| NM | 0 | B6 | RA |
| NP | 0 | B5 | G2 |
| OUT | NM | B7 | RB |

## Matriz de incidencia reducida

| | B1 | B2 | B3 | B4 | B5 | B6 | B7 |
|---|---|---|---|---|---|---|---|
| IN | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| N1 | 0 | -1 | 1 | 1 | 0 | 0 | 0 |
| NM | 0 | 0 | 0 | 0 | 0 | 1 | -1 |
| NP | 0 | 0 | -1 | 0 | 1 | 0 | 0 |
| OUT | 0 | 0 | 0 | -1 | 0 | 0 | 1 |

## Ecuaciones constitutivas

| Rama | Componente | Ecuación | Línea de origen |
|---|---|---|---:|
| B1 | V1 | V = E | 2 |
| B2 | C1 | s*C*V - I = 0 | 3 |
| B3 | C2 | s*C*V - I = 0 | 4 |
| B4 | G1 | G*V - I = 0 | 5 |
| B5 | G2 | G*V - I = 0 | 6 |
| B6 | RA | V - R*I = 0 | 7 |
| B7 | RB | V - R*I = 0 | 8 |

### Matriz Y

| | B1 | B2 | B3 | B4 | B5 | B6 | B7 |
|---|---|---|---|---|---|---|---|
| B1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| B2 | 0 | 0 + j6.2831853e-05 | 0 | 0 | 0 | 0 | 0 |
| B3 | 0 | 0 | 0 + j6.2831853e-05 | 0 | 0 | 0 | 0 |
| B4 | 0 | 0 | 0 | 0.0001 | 0 | 0 | 0 |
| B5 | 0 | 0 | 0 | 0 | 0.0001 | 0 | 0 |
| B6 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| B7 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

### Matriz Z

| | B1 | B2 | B3 | B4 | B5 | B6 | B7 |
|---|---|---|---|---|---|---|---|
| B1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B2 | 0 | -1 | 0 | 0 | 0 | 0 | 0 |
| B3 | 0 | 0 | -1 | 0 | 0 | 0 | 0 |
| B4 | 0 | 0 | 0 | -1 | 0 | 0 | 0 |
| B5 | 0 | 0 | 0 | 0 | -1 | 0 | 0 |
| B6 | 0 | 0 | 0 | 0 | 0 | -10000 | 0 |
| B7 | 0 | 0 | 0 | 0 | 0 | 0 | -10000 |

### Vector W

| Label | Value |
|---|---|
| B1 | 20 |
| B2 | 0 |
| B3 | 0 |
| B4 | 0 |
| B5 | 0 |
| B6 | 0 |
| B7 | 0 |

## Sistema ensamblado

Formulación: `MNA`; dimensiones: `7 × 7`.

| | V(NIN) | V(NN1) | V(NNM) | V(NNP) | V(NOUT) | I(V1) | I(U1) |
|---|---|---|---|---|---|---|---|
| KCL(NIN) | 0 + j6.2831853e-05 | 0 - j6.2831853e-05 | 0 | 0 | 0 | 1 | 0 |
| KCL(NN1) | 0 - j6.2831853e-05 | 0.0001 + j0.00012566371 | 0 | 0 - j6.2831853e-05 | -0.0001 | 0 | 0 |
| KCL(NNM) | 0 | 0 | 0.0002 | 0 | -0.0001 | 0 | 0 |
| KCL(NNP) | 0 | 0 - j6.2831853e-05 | 0 | 0.0001 + j6.2831853e-05 | 0 | 0 | 0 |
| KCL(NOUT) | 0 | -0.0001 | -0.0001 | 0 | 0.0002 | 0 | 1 |
| VSOURCE(V1) | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| OPAMP_DIFF(U1) | 0 | 0 | -1 | 1 | 0 | 0 | 0 |

### Vector del lado derecho

| Label | Value |
|---|---|
| KCL(NIN) | -0 |
| KCL(NN1) | -0 |
| KCL(NNM) | -0 |
| KCL(NNP) | -0 |
| KCL(NOUT) | -0 |
| VSOURCE(V1) | 20 |
| OPAMP_DIFF(U1) | 0 |

## Resultados AC

Barrido `DEC`; estado global: **PASS**.

| Frecuencia (Hz) | Estado | Transferencias calculadas |
|---:|---|---|
| 1 | PASS | H: |H|=7.8956851e-07, fase=179.964°, dB=-122.0522 |
| 1.2589254 | PASS | H: |H|=1.2513819e-06, fase=179.95468°, dB=-118.0522 |
| 1.5848932 | PASS | H: |H|=1.983307e-06, fase=179.94294°, dB=-114.0522 |
| 1.9952623 | PASS | H: |H|=3.1433307e-06, fase=179.92817°, dB=-110.0522 |
| 2.5118864 | PASS | H: |H|=4.9818457e-06, fase=179.90957°, dB=-106.05219 |
| 3.1622777 | PASS | H: |H|=7.8956991e-06, fase=179.88616°, dB=-102.05219 |
| 3.9810717 | PASS | H: |H|=1.2513854e-05, fase=179.85668°, dB=-98.052178 |
| 5.0118723 | PASS | H: |H|=1.9833159e-05, fase=179.81957°, dB=-94.052162 |
| 6.3095734 | PASS | H: |H|=3.1433529e-05, fase=179.77285°, dB=-90.052137 |
| 7.9432823 | PASS | H: |H|=4.9819016e-05, fase=179.71404°, dB=-86.052097 |
| 10 | PASS | H: |H|=7.8958394e-05, fase=179.63999°, dB=-82.052034 |
| 12.589254 | PASS | H: |H|=0.00012514207, fase=179.54677°, dB=-78.051934 |
| 15.848932 | PASS | H: |H|=0.00019834044, fase=179.4294°, dB=-74.051775 |
| 19.952623 | PASS | H: |H|=0.00031435752, fase=179.28163°, dB=-70.051523 |
| 25.118864 | PASS | H: |H|=0.00049824599, fase=179.09557°, dB=-66.051124 |
| 31.622777 | PASS | H: |H|=0.00078972419, fase=178.86128°, dB=-62.050491 |
| 39.810717 | PASS | H: |H|=0.0012517729, fase=178.56622°, dB=-58.049489 |
| 50.118723 | PASS | H: |H|=0.0019842892, fase=178.19453°, dB=-54.047901 |
| 63.095734 | PASS | H: |H|=0.0031457974, fase=177.72617°, dB=-50.045385 |
| 79.432823 | PASS | H: |H|=0.0049880403, fase=177.13567°, dB=-46.041401 |
| 100 | PASS | H: |H|=0.0079112534, fase=176.39051°, dB=-42.035094 |
| 125.89254 | PASS | H: |H|=0.012552901, fase=175.44893°, dB=-38.025118 |
| 158.48932 | PASS | H: |H|=0.019931146, fase=174.25655°, dB=-34.009355 |
| 199.52623 | PASS | H: |H|=0.031679271, fase=172.74144°, dB=-29.984497 |
| 251.18864 | PASS | H: |H|=0.050434657, fase=170.80594°, dB=-25.945419 |
| 316.22777 | PASS | H: |H|=0.080497818, fase=168.31274°, dB=-21.884318 |
| 398.10717 | PASS | H: |H|=0.12897785, fase=165.05965°, dB=-17.789697 |
| 501.18723 | PASS | H: |H|=0.20783065, fase=160.73188°, dB=-13.645808 |
| 630.95734 | PASS | H: |H|=0.33747862, fase=154.80919°, dB=-9.4350748 |
| 794.32823 | PASS | H: |H|=0.55253084, fase=146.38999°, dB=-5.1528695 |
| 1000 | PASS | H: |H|=0.9050599, fase=133.92704°, dB=-0.86645349 |
| 1258.9254 | PASS | H: |H|=1.4299886, fase=115.32382°, dB=3.1066514 |
| 1584.8932 | PASS | H: |H|=1.9915656, fase=90.480244°, dB=5.9838922 |
| 1995.2623 | PASS | H: |H|=2.2813323, fase=65.487203°, dB=7.1637711 |
| 2511.8864 | PASS | H: |H|=2.2945944, fase=46.630124°, dB=7.2141186 |
| 3162.2777 | PASS | H: |H|=2.2210442, fase=33.980936°, dB=6.9311442 |
| 3981.0717 | PASS | H: |H|=2.1495187, fase=25.446389°, dB=6.6468247 |
| 5011.8723 | PASS | H: |H|=2.097345, fase=19.4517°, dB=6.4333975 |
| 6309.5734 | PASS | H: |H|=2.0623801, fase=15.076653°, dB=6.2873742 |
| 7943.2823 | PASS | H: |H|=2.0396848, fase=11.790861°, dB=6.1912612 |
| 10000 | PASS | H: |H|=2.0251554, fase=9.2740444°, dB=6.1291672 |
| 12589.254 | PASS | H: |H|=2.0159149, fase=7.3209483°, dB=6.0894438 |
| 15848.932 | PASS | H: |H|=2.0100578, fase=5.7924377°, dB=6.0641711 |
| 19952.623 | PASS | H: |H|=2.0063523, fase=4.5897025°, dB=6.048144 |
| 25118.864 | PASS | H: |H|=2.0040105, fase=3.6400298°, dB=6.0379998 |
| 31622.777 | PASS | H: |H|=2.0025314, fase=2.8885247°, dB=6.0315867 |
| 39810.717 | PASS | H: |H|=2.0015976, fase=2.2930075°, dB=6.0275354 |
| 50118.723 | PASS | H: |H|=2.0010082, fase=1.8206846°, dB=6.0249772 |
| 63095.734 | PASS | H: |H|=2.0006362, fase=1.4458624°, dB=6.0233623 |
| 79432.823 | PASS | H: |H|=2.0004014, fase=1.1483096°, dB=6.0223431 |
| 100000 | PASS | H: |H|=2.0002533, fase=0.91204465°, dB=6.0216999 |
| 125892.54 | PASS | H: |H|=2.0001598, fase=0.72441767°, dB=6.021294 |
| 158489.32 | PASS | H: |H|=2.0001008, fase=0.57540279°, dB=6.0210378 |
| 199526.23 | PASS | H: |H|=2.0000636, fase=0.45704734°, dB=6.0208762 |
| 251188.64 | PASS | H: |H|=2.0000401, fase=0.36303992°, dB=6.0207743 |
| 316227.77 | PASS | H: |H|=2.0000253, fase=0.28837001°, dB=6.0207099 |
| 398107.17 | PASS | H: |H|=2.000016, fase=0.22905902°, dB=6.0206693 |
| 501187.23 | PASS | H: |H|=2.0000101, fase=0.18194733°, dB=6.0206437 |
| 630957.34 | PASS | H: |H|=2.0000064, fase=0.14452554°, dB=6.0206275 |
| 794328.23 | PASS | H: |H|=2.000004, fase=0.11480054°, dB=6.0206173 |
| 1000000 | PASS | H: |H|=2.0000025, fase=0.091189219°, dB=6.0206109 |

## Validación

**Estado: PASS**

| Métrica | Norma | Umbral | Resultado |
|---|---:|---:|---|
| linear_residual | 4.9979251e-19 | 9.6850171e-07 | PASS |
| full_rank |  |  | PASS |
| KCL | 5.3114842e-19 | 2.0654749e-10 | PASS |
| branch_node_voltage | 0 | 8.1697375e-07 | PASS |
| voltage_source_constraints | 0 | 5.4373968e-07 | PASS |
| opamp_differential_constraint | 0 | 4.860799e-07 | PASS |
| branch_admittance | 0 | 1.5742977e-10 | PASS |

Número de condición: `87792.402`.

## Advertencias y limitaciones

- .OPAMP es una extension educativa no portable a SPICE.
- El modelo ideal lineal no incluye rieles ni saturacion.
- No se proporciono una referencia SPICE externa; no se ejecuto comparacion independiente.
- El barrido 1 Hz-1 MHz fue seleccionado para este ejemplo y no es una especificacion del usuario.

## Artefactos y reproducibilidad

- `artifacts\opamp_filter_20261102\opamp_active_filter.cir`
- `artifacts\opamp_filter_20261102\netlist_validation.json`
- `artifacts\opamp_filter_20261102\parsed.json`
- `artifacts\opamp_filter_20261102\circuit.json`
- `artifacts\opamp_filter_20261102\topology.json`
- `artifacts\opamp_filter_20261102\topology.png`
- `artifacts\opamp_filter_20261102\incidence.json`
- `artifacts\opamp_filter_20261102\incidence.md`
- `artifacts\opamp_filter_20261102\incidence.npz`
- `artifacts\opamp_filter_20261102\constitutive_1khz.json`
- `artifacts\opamp_filter_20261102\mna_1khz.json`
- `artifacts\opamp_filter_20261102\solution_1khz.json`
- `artifacts\opamp_filter_20261102\validation_1khz.json`
- `artifacts\opamp_filter_20261102\ac_results.json`
- `artifacts\opamp_filter_20261102\plots\graph.png`
- `artifacts\opamp_filter_20261102\plots\magnitude.png`
- `artifacts\opamp_filter_20261102\plots\phase.png`
