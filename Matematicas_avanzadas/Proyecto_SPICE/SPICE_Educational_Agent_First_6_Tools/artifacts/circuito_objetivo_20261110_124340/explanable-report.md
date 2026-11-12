# Explainable report: analisis del filtro activo objetivo

**Ejecucion:** `circuito_objetivo_20261110_124340`  
**Entrada:** diagrama suministrado por el usuario; netlist conservado en `circuito_objetivo.cir`  
**Metodo para el circuito completo:** MNA con op-amp ideal del proyecto  
**Resultado del barrido:** PASS (300 de 300 puntos)

## 1. Objetivo y alcance

Se modelo el filtro activo de dos capacitores, dos conductancias, la red de realimentacion resistiva y un amplificador operacional ideal. Se ejecuto el analisis AC pedido en el diagrama: 300 frecuencias lineales de 10 Hz a 100 kHz, con excitacion `Vi` y transferencia `Vo/Vi`. La directiva `.OPAMP ... IDEAL` es una extension educativa del proyecto, no una sintaxis portable a cualquier simulador SPICE.

La MNA completa es el resultado que representa el circuito con el op-amp. Se produjo ademas una Tableau parcial separada, solo para las siete ramas de dos terminales, siguiendo las notas de sesion; esa matriz excluye U1 y **no** es una solucion del circuito completo.

## 2. Datos tomados del diagrama y supuestos

| Dato | Valor modelado | Evidencia / interpretacion |
|---|---:|---|
| $C_1$, $C_2$ | 0.1 uF cada uno | Valores indicados en el diagrama |
| $R_A$ | 1.27 kohm | Valor indicado en el diagrama |
| $R_B$ | 2.3 kohm | Valor indicado en el diagrama |
| $G_1$ | 1/$R_A$ = 0.00078740157480315 S | Conductancia indicada; valor decimal guardado en el netlist |
| $G_2$ | 1/$R_B$ = 0.000434782608695652 S | Conductancia indicada; valor decimal guardado en el netlist |
| $V_i$ | 1 mV, fase 0 deg | Fuente AC para todo el barrido |
| Tierra | nodo `0` | Referencia del netlist |
| Op-amp | U1, IDEAL | Entradas `NP`, `NM`; salida `OUT` |
| Frecuencias | `.AC LIN 300 10 100k` | 300 puntos linealmente distribuidos, extremos incluidos por la herramienta |

El diagrama solicita condiciones iniciales iguales a cero, pero no se ejecuto transitorio: en el analisis fasorial AC esas condiciones no son una entrada del analisis realizado. El fasor de 1 mV se usa con la convencion de la herramienta; no se atribuye aqui interpretacion pico/RMS.

Imagen de entrada adjunta a la solicitud: `C:\Users\johng\AppData\Roaming\Code\agentSessionData\faa347df-72d0-4016-a602-544c0747c0d7\attachments\6287233e-4813-4991-94ff-5725a05a7a25\Pasted Image.png`.

## 3. Netlist creado

```spice
* Filtro activo objetivo, valores tomados del diagrama suministrado
V1 IN 0 AC 1m 0
C1 IN N1 0.1u
C2 N1 NP 0.1u
G1 N1 OUT 0.00078740157480315
G2 NP 0 0.000434782608695652
RB OUT NM 2.3k
RA NM 0 1.27k
.OPAMP U1 NP NM OUT IDEAL
.AC LIN 300 10 100k
.END
```

La salida del parser registro 7 elementos de dos terminales y las directivas OPAMP, AC y END. El netlist original de esta ejecucion no se modifico despues del analisis.

### Elementos normalizados

| Orden/branch | Elemento | Tipo | Terminal inicial -> final | Valor normalizado |
|---|---|---|---|---:|
| B1 | V1 | V | `IN` -> `0` | 0.001 V |
| B2 | C1 | C | `IN` -> `N1` | 1e-07 F |
| B3 | C2 | C | `N1` -> `NP` | 1e-07 F |
| B4 | G1 | G | `N1` -> `OUT` | 0.00078740157480315 S |
| B5 | G2 | G | `NP` -> `0` | 0.000434782608695652 S |
| B6 | RB | R | `OUT` -> `NM` | 2300 ohm |
| B7 | RA | R | `NM` -> `0` | 1270 ohm |

La conversion de unidades procede del parser. `G1` y `G2` se guardaron en S con las cifras decimales mostradas en el netlist.

## 4. Validacion, parseo y topologia

1. `validate_netlist.py`: **PASS**, diagnosticos: 0.
2. `parse_netlist.py`: proceso terminado correctamente; creo `parsed.json`.
3. `build_circuit_model.py`: modelo de 6 nodos incluyendo referencia y 7 ramas; conservo U1 como dispositivo multipuerto separado.
4. `build_oriented_graph.py`: grafo conectado = **True**; conservo terminales de U1 por separado.
5. `build_incidence_matrix.py`: matriz de incidencia reducida de 5 x 7.

Orden de nodos no de referencia, tal como en el artefacto: `IN`, `N1`, `NM`, `NP`, `OUT`. Referencia: `0`. El orden de ramas se conserva desde el netlist:

| Branch | Elemento | Orientacion (inicio -> fin) |
|---|---|---|
| B1 | V1 | `IN` -> `0` |
| B2 | C1 | `IN` -> `N1` |
| B3 | C2 | `N1` -> `NP` |
| B4 | G1 | `N1` -> `OUT` |
| B5 | G2 | `NP` -> `0` |
| B6 | RB | `OUT` -> `NM` |
| B7 | RA | `NM` -> `0` |

Convencion: la orientacion de cada rama sigue el orden de terminales del netlist; en incidencia, +1 significa rama saliente y -1 entrante. Las etiquetas `N...` que aparecen en algunos JSON son nombres auxiliares de presentacion de las herramientas; el netlist conserva los nombres de nodos originales.

### Matriz de incidencia reducida $A$

Filas en el orden de nodos no de referencia y columnas en el orden de ramas anterior:

| Nodo / branch | B1 | B2 | B3 | B4 | B5 | B6 | B7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| IN | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| N1 | 0 | -1 | 1 | 1 | 0 | 0 | 0 |
| NM | 0 | 0 | 0 | 0 | 0 | -1 | 1 |
| NP | 0 | 0 | -1 | 0 | 1 | 0 | 0 |
| OUT | 0 | 0 | 0 | -1 | 0 | 1 | 0 |

### Grafo orientado

El grafo y su imagen se generaron desde el modelo. Los elementos de dos terminales se dibujan como aristas; U1 se conserva como metadato de tres terminales y no se inventa una rama para el op-amp.

## 5. Formulacion y solucion MNA del circuito completo

Se selecciono MNA porque el netlist contiene `.OPAMP U1 NP NM OUT IDEAL`. Para ese modelo el proyecto impone corriente de entrada cero, la restriccion lineal $V(NP)-V(NM)=0$ y una corriente auxiliar de salida. No se convierte el op-amp en componente pasivo ni se modela saturacion, rieles o ancho de banda.

A 10 Hz, `build_mna_system.py` ensamblo el sistema complejo $M X=b$ de dimension 7 x 7. El orden (sin reordenar) es:

- Incognitas: `V(NIN)`, `V(NN1)`, `V(NNM)`, `V(NNP)`, `V(NOUT)`, `I(V1)`, `I(U1)`.
- Ecuaciones: `KCL(IN)`, `KCL(N1)`, `KCL(NM)`, `KCL(NP)`, `KCL(OUT)`, `VSOURCE(V1)`, `OPAMP_DIFF(U1)`.
- Bloques de ecuaciones: KCL de cinco nodos, ecuacion de fuente `V1` y restriccion diferencial de `U1`.

### Matriz MNA numerica $M$ a 10 Hz

Las entradas complejas se muestran como `real +/- imag*j`, en el orden de incognitas documentado. La matriz sin redondeo de presentacion y sus metadatos estan en `mna_system_10Hz.json`.

| Ecuacion \ Incognita | V(IN) | V(N1) | V(NM) | V(NP) | V(OUT) | I(V1) | I(U1) | RHS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| KCL(IN) | 6.283185e-06j | -6.283185e-06j | 0 | 0 | 0 | 1 | 0 | 0 |
| KCL(N1) | -6.283185e-06j | 0.0007874016+1.256637e-05j | 0 | -6.283185e-06j | -0.0007874016 | 0 | 0 | 0 |
| KCL(NM) | 0 | 0 | 0.001222184 | 0 | -0.0004347826 | 0 | 0 | 0 |
| KCL(NP) | 0 | -6.283185e-06j | 0 | 0.0004347826+6.283185e-06j | 0 | 0 | 0 | 0 |
| KCL(OUT) | 0 | -0.0007874016 | -0.0004347826 | 0 | 0.001222184 | 0 | 1 | 0 |
| VSOURCE(V1) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0.001 |
| OPAMP_DIFF(U1) | 0 | 0 | -1 | 1 | 0 | 0 | 0 | 0 |

La fuente aparece como el lado derecho de la ecuacion `VSOURCE(V1)` con fasor 0.001 + 0j V. Las filas KCL tienen RHS cero; el ultimo renglon representa la igualdad de las entradas del op-amp.

## 6. Barrido AC MNA

- Estado global: **PASS**.
- Formulacion: **MNA**; tipo: **LIN**.
- Intervalo: 10 to 100000 Hz; cantidad: **300**.
- Observable: $H(j*omega)=V_o/V_i$, etiquetado por el JSON de transferencias como `V(NOUT)/V(NIN)`.
- Estados por punto: solver {'PASS': 300}; validacion {'PASS': 300}; transferencia {'PASS': 300}.
- Tolerancias solver/validacion: atol = 1e-10, rtol = 1e-08; limite de condicion = 1e+12.
- Numero de condicion reportado en los puntos: 3260.8 to 25614.5; rango completo reportado PASS.
- Residuo lineal reportado por el solver en los puntos: minimo 1.58686e-24, maximo 5.15784e-20.

Magnitud, dB y fase a continuacion son salidas directas del solver; no se estimaron desde la grafica. El maximo indicado es solo el maximo entre los 300 puntos muestreados, no una busqueda continua.

| Punto | Frecuencia (Hz) | Estado | $|H|$ | dB | Fase (degrees) |
|---|---:|---|---:|---:|---:|
| Inicio del barrido | 10 | PASS | 0.000324177764 | -69.784336 | -179.414825 |
| Maximo muestreado | 1347.65886 | PASS | 3.34820094 | 10.496230 | -51.509838 |
| Fin del barrido | 100000 | PASS | 2.81115716 | 8.977703 | -0.507441 |

### Fasores de salida y vectores solucion seleccionados

Los valores de la tabla se copiaron de `solution.unknowns` en los puntos indicados. Se quita solo el prefijo N auxiliar en las etiquetas de presentacion. Cada valor complejo se expresa como `real + imag*j`; magnitud y fase tambien proceden de los resultados del solver.

#### Inicio: 10 Hz

| Variable | Valor complejo | Magnitud | Fase (degrees) |
|---|---:|---:|---:|
| V(IN) | 0.001 +0j | 0.001 volt | 0 |
| V(N1) | -1.96819373e-07 +7.9785554e-06j | 7.98098266e-06 volt | 91.413117 |
| V(NM) | -1.15317728e-07 -1.17780686e-09j | 1.15323742e-07 volt | -179.41483 |
| V(NP) | -1.15317728e-07 -1.17780686e-09j | 1.15323742e-07 volt | -179.41483 |
| V(OUT) | -3.24160856e-07 -3.31084292e-09j | 3.24177764e-07 volt | -179.41483 |
| I(V1) | -5.01307421e-11 -6.28442196e-09j | 6.2846219e-09 ampere | -90.457038 |
| I(U1) | 1.91070245e-10 +6.28586146e-09j | 6.28876475e-09 ampere | 88.258926 |

Punto PASS; validacion PASS; rango 7/7.

#### Maximo muestreado: 1347.65886 Hz

| Variable | Valor complejo | Magnitud | Fase (degrees) |
|---|---:|---:|---:|
| V(IN) | 0.001 -0j | 0.001 volt | -0 |
| V(N1) | 0.000262615514 -0.00131292992j | 0.00133893685 volt | -78.688828 |
| V(NM) | 0.000741315061 -0.000932289284j | 0.00119109669 volt | -51.509838 |
| V(NP) | 0.000741315061 -0.000932289284j | 0.00119109669 volt | -51.509838 |
| V(OUT) | 0.00208385415 -0.0026206872j | 0.00334820094 volt | -51.509838 |
| I(V1) | 1.11173527e-06 -6.24386977e-07j | 1.27507428e-06 ampere | -29.319995 |
| I(U1) | -2.01775881e-06 +1.76381619e-06j | 2.67999966e-06 ampere | 138.84179 |

Punto PASS; validacion PASS; rango 7/7.

#### Fin: 100000 Hz

| Variable | Valor complejo | Magnitud | Fase (degrees) |
|---|---:|---:|---:|
| V(IN) | 0.001 -0j | 0.001 volt | -0 |
| V(N1) | 0.000999946996 -1.57766589e-05j | 0.00100007145 volt | -0.90390888 |
| V(NM) | 0.00100000828 -8.8568214e-06j | 0.0010000475 volt | -0.50744102 |
| V(NP) | 0.00100000828 -8.8568214e-06j | 0.0010000475 volt | -0.50744102 |
| V(OUT) | 0.00281104691 -2.48967342e-05j | 0.00281115716 volt | -0.50744102 |
| I(V1) | 9.91276711e-07 -3.33036976e-09j | 9.91282306e-07 ampere | -0.1924946 |
| I(U1) | -2.21347102e-06 +1.41550368e-08j | 2.21351628e-06 ampere | 179.6336 |

Punto PASS; validacion PASS; rango 7/7.

### Graficas

- Magnitud de transferencia, dB: [`plots/magnitude.png`](./plots/magnitude.png).
- Fase: [`plots/phase.png`](./plots/phase.png).
- Topologia orientada: [`plots/graph.png`](./plots/graph.png).

Las imagenes ilustran los datos; no reemplazan la validacion cuantitativa del solver.

### Ecuaciones constitutivas y matrices diagonales de la Tableau parcial

Valores extraidos del artefacto constitutivo a 10 Hz. `Ykk`, `Zkk` y `Wk` son las entradas diagonales/no nulas por rama en $YV_b+ZI=W$; las partes complejas se muestran como `real +/- imag*j`.

| Branch | Elemento | Ecuacion de rama | Ykk | Zkk | Wk |
|---|---|---|---:|---:|---:|
| B1 | V1 | `V = E` | 1 | 0 | 0.001 |
| B2 | C1 | `s*C*V - I = 0` | 6.283185e-06j | -1 | 0 |
| B3 | C2 | `s*C*V - I = 0` | 6.283185e-06j | -1 | 0 |
| B4 | G1 | `G*V - I = 0` | 0.0007874016 | -1 | 0 |
| B5 | G2 | `G*V - I = 0` | 0.0004347826 | -1 | 0 |
| B6 | RB | `V - R*I = 0` | 1 | -2300 | 0 |
| B7 | RA | `V - R*I = 0` | 1 | -1270 | 0 |

U1 no tiene ecuacion constitutiva en esta Tableau parcial porque fue excluido explicitamente; no se asigno ningun stamp Tableau al op-amp.
## 7. Tableau parcial (no equivale al circuito completo)

Las notas de sesion recomiendan mostrar la Tableau de las ramas compatibles cuando un componente impide ensamblar la Tableau completa. Se genero una copia derivada del modelo en la que se excluyo expresamente U1 y se conservaron las siete ramas pasivas/fuente y el orden de nodos/ramas. Se ensamblo a 10 Hz con `build_constitutive_matrices.py` y `build_tableau_system.py`; la dimension resultante es 19 x 19, con $X=[V_b; I; V_n]$ y $T X=W_p$.

**Alcance del PASS:** la solucion y validacion `PASS` corresponden solo a este circuito parcial sin op-amp. No se debe comparar esa solucion como si fuera el circuito objetivo completo ni usarla para reemplazar el barrido MNA.

La siguiente seccion reproduce la matriz $T$ numerica completa, generada desde `tableau_partial_10Hz.json`; `j` indica parte imaginaria. La visualizacion colorea los bloques.

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

- Imagen coloreada: [`tableau_partial_T_colored_blocks_10Hz.png`](./tableau_partial_T_colored_blocks_10Hz.png).
- Sistema complejo completo (fuente de la matriz): [`tableau_partial_10Hz.json`](./tableau_partial_10Hz.json).
- Matrices constitutivas $Y/Z/W$: [`constitutive_tableau_partial_10Hz.json`](./constitutive_tableau_partial_10Hz.json).
- Validacion parcial: **PASS**, rango 19/19, residuo lineal 5.44127e-22, residuo KCL 2.47572e-24, residuo constitutivo 1.05879e-22, condicion 4.48564e+07.
- Estado de solucion parcial del solver: **PASS**.

## 8. Puertas de aceptacion y validaciones

| Etapa | Estado | Alcance / evidencia |
|---|---|---|
| Validacion netlist | **PASS** | 0 diagnosticos; ver `netlist_validation.json` |
| Parseo y modelo | **OK** | Siete elementos; modelo serializado en `parsed.json` y `circuit.json`. |
| Topologia e incidencia | **OK** | Grafo conectado; incidencia reducida 5x7. |
| Sistema MNA a 10 Hz | **ENSAMBLADO** | 7x7; no equivale por si solo a una solucion. La solucion/validacion AC del punto se encuentra en `ac_results.json`. |
| Barrido AC MNA global | **PASS** | 300 puntos; {'PASS': 300} solver y {'PASS': 300} validacion. |
| Tableau parcial | **PASS** | PASS aplica solo al sistema sin U1; no representa circuito completo. |
| Comparacion externa | **NO EJECUTADA** | No se proporciono referencia independiente compatible. |
| Reporte automatico | **NO EJECUTADO** | El paquete no ensambla automaticamente estos artefactos separados en un bundle de reporte validado; este documento los referencia directamente. |

## 9. Inventario de artefactos de esta ejecucion

Todos los archivos siguientes estan en el mismo directorio que este reporte:

| Artefacto | Contenido |
|---|---|
| `circuito_objetivo.cir` | Netlist de entrada para esta ejecucion. |
| `netlist_validation.json` | Diagnosticos y estado del validador. |
| `parsed.json` | Elementos, directivas y valores normalizados. |
| `circuit.json` | Modelo de circuito, nodos, ramas y dispositivo op-amp. |
| `topology.json`, `graph.png` | Grafo orientado y visualizacion inicial. |
| `incidence.json`, `incidence.md`, `incidence.npz` | Incidencia reducida y formatos de salida. |
| `transfers.json` | Definicion de transferencia acordada `Vo/Vi`. |
| `mna_system_10Hz.json` | Matriz MNA compleja completa y RHS a 10 Hz. |
| `ac_results.json` | Solucion, transferencia, estado y validacion por cada uno de los 300 puntos. |
| `plots/graph.png`, `plots/magnitude.png`, `plots/phase.png` | Topologia y graficas AC. |
| `circuit_tableau_partial.json`, `incidence_tableau_partial.json` | Copia derivada usada para separar el circuito compatible con Tableau; excluye U1. |
| `constitutive_tableau_partial_10Hz.json` | Matrices constitutivas parciales Y/Z/W. |
| `tableau_partial_10Hz.json` | Matriz T, RHS, orden y particiones de bloques. |
| `tableau_partial_solution_10Hz.json`, `tableau_partial_validation_10Hz.json` | Solucion y validacion exclusivamente parciales. |
| `tableau_partial_10Hz.md`, `tableau_partial_T_colored_blocks_10Hz.png` | Matriz legible completa y visualizacion coloreada. |
| `tableau_not_applicable.md` | Explica por que Tableau no es aplicable al circuito completo. |
| `explanable-report.md` | Este reporte explicable. |

### Secuencia de comandos reproducible

Ejecutados desde `SPICE_Educational_Agent_First_6_Tools` (las rutas de salida se encuentran dentro de la carpeta de ejecucion indicada):

```powershell
python validate_netlist.py <RUN>\circuito_objetivo.cir -o <RUN>\netlist_validation.json
python parse_netlist.py <RUN>\circuito_objetivo.cir -o <RUN>\parsed.json
python build_circuit_model.py <RUN>\parsed.json -o <RUN>\circuit.json
python build_oriented_graph.py <RUN>\circuit.json -o <RUN>\topology.json --image <RUN>\graph.png
python build_incidence_matrix.py <RUN>\circuit.json -o <RUN>\incidence.json --markdown <RUN>\incidence.md --npz <RUN>\incidence.npz
python build_mna_system.py <RUN>\circuit.json <RUN>\incidence.json --frequency 10 -o <RUN>\mna_system_10Hz.json
python solve_ac_sweep.py <RUN>\circuit.json <RUN>\incidence.json --formulation MNA --transfers <RUN>\transfers.json -o <RUN>\ac_results.json
python plot_results.py <RUN>\ac_results.json --topology <RUN>\topology.json --output-dir <RUN>\plots --title "Filtro activo objetivo: Vi a Vo"
python build_constitutive_matrices.py <RUN>\circuit_tableau_partial.json -o <RUN>\constitutive_tableau_partial_10Hz.json --frequency 10
python build_tableau_system.py <RUN>\circuit_tableau_partial.json <RUN>\incidence_tableau_partial.json <RUN>\constitutive_tableau_partial_10Hz.json -o <RUN>\tableau_partial_10Hz.json
python solve_linear_system.py <RUN>\tableau_partial_10Hz.json -o <RUN>\tableau_partial_solution_10Hz.json
python validate_solution.py <RUN>\tableau_partial_10Hz.json <RUN>\tableau_partial_solution_10Hz.json -o <RUN>\tableau_partial_validation_10Hz.json
```

`<RUN>` representa `artifacts\circuito_objetivo_20261110_124340`. Las ultimas cuatro herramientas actuan sobre la copia parcial sin U1, no sobre el circuito completo. Las graficas coloreadas y este Markdown se generaron a partir de los JSON resultantes; sus salidas no sustituyen las validaciones numericas.

## 10. Limitaciones, advertencias y conclusion

- **Resultado aceptado para el circuito completo:** barrido AC MNA global PASS y 300/300 puntos PASS en solucion, validacion y transferencia.
- **Tableau:** solo parcial; omite U1 y no es una validacion independiente ni una alternativa al resultado completo.
- **Modelo del op-amp:** ideal lineal; no considera saturacion, rieles, ancho de banda ni otros limites fisicos.
- **Validacion externa:** no se comparo con SPICE externo; no se proporciono referencia. La validacion presentada es interna (residuos, rango, KCL, tensiones de rama/fuente y restriccion diferencial, segun las comprobaciones del validador).
- **Transitorio/condiciones iniciales:** no ejecutados; el analisis aqui documentado es exclusivamente AC fasorial.
- **Maximo de ganancia:** se informa como maximo observado en la malla de 300 frecuencias, no como extremo continuo exacto.
- No se calculo manualmente la solucion; matrices, vectores, respuesta compleja, magnitud, dB, fase y estados se tomaron de las herramientas y artefactos enumerados.

### Reproduccion

Las herramientas se ejecutaron desde `SPICE_Educational_Agent_First_6_Tools`. Los comandos y datos de entrada quedan documentados en el netlist y los JSON. No se sobrescribieron los artefactos previos de la ejecucion al crear este reporte.
