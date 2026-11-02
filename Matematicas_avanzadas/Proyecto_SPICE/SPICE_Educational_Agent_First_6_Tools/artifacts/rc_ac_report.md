# Reporte de simulación de circuito

- **Fuente:** rc_ac.cir
- **Método:** NODAL
- **Ejecución:** rc-ac-report-001
- **Estado:** PASS

## Netlist original

```spice
* AC current-driven RC network
I1 0 1 AC 1m 0
R1 1 0 1k
C1 1 0 1u
.AC DEC 10 10 100k
.END

```

## Componentes normalizados

| Componente | Tipo | Desde | Hacia | Valor SI | Unidad | Rama | Línea |
|---|---|---|---|---:|---|---|---:|
| I1 | I | 0 | 1 | 0.001 | ampere | B1 | 2 |
| R1 | R | 1 | 0 | 1000 | ohm | B2 | 3 |
| C1 | C | 1 | 0 | 1e-06 | farad | B3 | 4 |

## Nodos

| Nodo | Referencia | Índice completo | Índice reducido |
|---|:---:|---:|---:|
| 0 | sí | 0 | None |
| 1 | no | 1 | 0 |

## Topología

Conectado: **True**

| Desde | Hacia | Rama | Componente |
|---|---|---|---|
| 0 | 1 | B1 | I1 |
| 1 | 0 | B2 | R1 |
| 1 | 0 | B3 | C1 |

## Matriz de incidencia reducida

| | B1 | B2 | B3 |
|---|---|---|---|
| 1 | -1 | 1 | 1 |

## Sistema ensamblado

Formulación: `nodal`; dimensiones: `1 × 1`.

| | x[0] |
|---|---|
| eq[0] | 0.001 + j0.00039478418 |

### Vector del lado derecho

| Label | Value |
|---|---|
| eq[0] | 0.001 |

## Resultados AC

Barrido `DEC`; estado global: **PASS**.

| Frecuencia (Hz) | Estado | Transferencias calculadas |
|---:|---|---|
| 10 | PASS | H: |H|=998.0319, fase=-3.5952738°, dB=59.982888 |
| 12.589254 | PASS | H: |H|=996.88615, fase=-4.5227144°, dB=59.972911 |
| 15.848932 | PASS | H: |H|=995.07831, fase=-5.686867°, dB=59.957145 |
| 19.952623 | PASS | H: |H|=992.23311, fase=-7.1456647°, dB=59.932274 |
| 25.118864 | PASS | H: |H|=987.77335, fase=-8.9688108°, dB=59.893146 |
| 31.622777 | PASS | H: |H|=980.82666, fase=-11.237841°, dB=59.831845 |
| 39.810717 | PASS | H: |H|=970.11097, fase=-14.043691°, dB=59.736428 |
| 50.118723 | PASS | H: |H|=953.82455, fase=-17.479487°, dB=59.58937 |
| 63.095734 | PASS | H: |H|=929.61279, fase=-21.625464°, dB=59.366042 |
| 79.432823 | PASS | H: |H|=894.75223, fase=-26.523377°, dB=59.034056 |
| 100 | PASS | H: |H|=846.73302, fase=-32.141908°, dB=58.55493 |
| 125.89254 | PASS | H: |H|=784.29786, fase=-38.344214°, dB=57.889621 |
| 158.48932 | PASS | H: |H|=708.58697, fase=-44.879937°, dB=57.007863 |
| 199.52623 | PASS | H: |H|=623.58101, fase=-51.421887°, dB=55.897858 |
| 251.18864 | PASS | H: |H|=535.21721, fase=-57.641357°, dB=54.570601 |
| 316.22777 | PASS | H: |H|=449.56459, fase=-63.284248°, dB=53.055842 |
| 398.10717 | PASS | H: |H|=371.21388, fase=-68.2095°, dB=51.392484 |
| 501.18723 | PASS | H: |H|=302.66186, fase=-72.382449°, dB=49.619154 |
| 630.95734 | PASS | H: |H|=244.58256, fase=-75.842834°, dB=47.76851 |
| 794.32823 | PASS | H: |H|=196.45949, fase=-78.670004°, dB=45.86546 |
| 1000 | PASS | H: |H|=157.17673, fase=-80.956939°, dB=43.927765 |
| 1258.9254 | PASS | H: |H|=125.42296, fase=-82.794818°, dB=41.967541 |
| 1584.8932 | PASS | H: |H|=99.917452, fase=-84.265583°, dB=39.992827 |
| 1995.2623 | PASS | H: |H|=79.513866, fase=-85.439377°, dB=38.008857 |
| 2511.8864 | PASS | H: |H|=63.233922, fase=-86.374544°, dB=36.019002 |
| 3162.2777 | PASS | H: |H|=50.26559, fase=-87.11878°, dB=34.025416 |
| 3981.0717 | PASS | H: |H|=39.946005, fase=-87.710653°, dB=32.029467 |
| 5011.8723 | PASS | H: |H|=31.739587, fase=-88.18115°, dB=30.032025 |
| 6309.5734 | PASS | H: |H|=25.216338, fase=-88.555057°, dB=28.03364 |
| 7943.2823 | PASS | H: |H|=20.0324, fase=-88.852151°, dB=26.034659 |
| 10000 | PASS | H: |H|=15.913479, fase=-89.088186°, dB=24.035303 |
| 12589.254 | PASS | H: |H|=12.641116, fase=-89.275698°, dB=22.035709 |
| 15848.932 | PASS | H: |H|=10.041492, fase=-89.424655°, dB=20.035965 |
| 19952.623 | PASS | H: |H|=7.9763888, fase=-89.542982°, dB=18.036126 |
| 25118.864 | PASS | H: |H|=6.3359452, fase=-89.636975°, dB=16.036228 |
| 31622.777 | PASS | H: |H|=5.0328575, fase=-89.711637°, dB=14.036293 |
| 39810.717 | PASS | H: |H|=3.9977595, fase=-89.770945°, dB=12.036333 |
| 50118.723 | PASS | H: |H|=3.1755426, fase=-89.818055°, dB=10.036359 |
| 63095.734 | PASS | H: |H|=2.5224278, fase=-89.855475°, dB=8.036375 |
| 79432.823 | PASS | H: |H|=2.003638, fase=-89.8852°, dB=6.0363852 |
| 100000 | PASS | H: |H|=1.5915474, fase=-89.908811°, dB=4.0363916 |

## Validación

**Estado: PASS**

| Métrica | Norma | Umbral | Resultado |
|---|---:|---:|---|
| linear_residual | 2.1684043e-19 | 1.2e-10 | PASS |
| full_rank |  |  | PASS |
| KCL | 1.1689055e-19 | 1.244949e-10 | PASS |
| branch_node_voltage | 0 | 3.4672839e-08 | PASS |
| branch_admittance | 0 | 1.3414214e-10 | PASS |

Número de condición: `1`.

## Comparación de referencia

Estado: **PASS**

| Punto | Frecuencia (Hz) | Estado | Variables comparadas |
|---:|---:|---|---:|
| 0 | 10 | PASS | 1 |
| 1 | 12.589254 | PASS | 1 |
| 2 | 15.848932 | PASS | 1 |
| 3 | 19.952623 | PASS | 1 |
| 4 | 25.118864 | PASS | 1 |
| 5 | 31.622777 | PASS | 1 |
| 6 | 39.810717 | PASS | 1 |
| 7 | 50.118723 | PASS | 1 |
| 8 | 63.095734 | PASS | 1 |
| 9 | 79.432823 | PASS | 1 |
| 10 | 100 | PASS | 1 |
| 11 | 125.89254 | PASS | 1 |
| 12 | 158.48932 | PASS | 1 |
| 13 | 199.52623 | PASS | 1 |
| 14 | 251.18864 | PASS | 1 |
| 15 | 316.22777 | PASS | 1 |
| 16 | 398.10717 | PASS | 1 |
| 17 | 501.18723 | PASS | 1 |
| 18 | 630.95734 | PASS | 1 |
| 19 | 794.32823 | PASS | 1 |
| 20 | 1000 | PASS | 1 |
| 21 | 1258.9254 | PASS | 1 |
| 22 | 1584.8932 | PASS | 1 |
| 23 | 1995.2623 | PASS | 1 |
| 24 | 2511.8864 | PASS | 1 |
| 25 | 3162.2777 | PASS | 1 |
| 26 | 3981.0717 | PASS | 1 |
| 27 | 5011.8723 | PASS | 1 |
| 28 | 6309.5734 | PASS | 1 |
| 29 | 7943.2823 | PASS | 1 |
| 30 | 10000 | PASS | 1 |
| 31 | 12589.254 | PASS | 1 |
| 32 | 15848.932 | PASS | 1 |
| 33 | 19952.623 | PASS | 1 |
| 34 | 25118.864 | PASS | 1 |
| 35 | 31622.777 | PASS | 1 |
| 36 | 39810.717 | PASS | 1 |
| 37 | 50118.723 | PASS | 1 |
| 38 | 63095.734 | PASS | 1 |
| 39 | 79432.823 | PASS | 1 |
| 40 | 100000 | PASS | 1 |

## Advertencias y limitaciones

- La comparaci?n usa la referencia calculada por el mismo modelo de transferencia evaluado en el mismo conjunto de frecuencias.

## Artefactos y reproducibilidad

- `artifacts/rc_ac_report.md`
- `artifacts/rc_ac_report_bundle.json`
