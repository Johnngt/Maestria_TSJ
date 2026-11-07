# Especificacion tecnica: amplificador operacional ideal mediante MNA

- **Fecha de registro:** 2026-11-02
- **Estado:** especificacion aprobada por el usuario e implementada como extension educativa del proyecto
- **Implementacion:** `build_mna_system.py`, integracion en `solve_linear_system.py`, `validate_solution.py` y `solve_ac_sweep.py`
- **Directiva:** `.OPAMP <id> <n+> <n-> <out> IDEAL`
- **Compatibilidad:** extension propia del proyecto; no es sintaxis SPICE portable

## 1. Objetivo y alcance

Modelar un op-amp ideal como bloque multipuerto en la formulacion Modified Nodal Analysis (MNA), sin convertirlo en rama pasiva, corto, circuito abierto ni componente equivalente improvisado.

La implementacion soporta el modelo lineal ideal para circuitos con elementos R, G, C, L, fuentes independientes V/I y uno o mas bloques `.OPAMP ... IDEAL`, en DC o AC fasorial de frecuencia positiva. La solucion solo es aceptable si el solver y la validacion entregan `PASS`.

El modelo no representa rieles de alimentacion, saturacion, slew rate, ancho de banda, ruido, corrientes de polarizacion, offsets ni dinamica fisica. La igualdad de entradas es una restriccion de operacion lineal y realimentacion compatible; no es una propiedad universal de cualquier estado/topologia. Un resultado matematico dentro de este modelo no prueba que un dispositivo fisico pueda producirlo.

## 2. Interfaz de netlist

```spice
.OPAMP U1 NP NM OUT IDEAL
```

Campos posicionales:

1. `U1`: identificador unico del dispositivo.
2. `NP`: terminal no inversor `n+`.
3. `NM`: terminal inversor `n-`.
4. `OUT`: terminal de salida.
5. `IDEAL`: modelo soportado.

El parser/validador preserva nombre, pines, modelo, linea fuente y numero de linea. Los pines son nodos del circuito. No tratar la directiva como una rama de dos terminales ni asumir portabilidad a simuladores SPICE externos.

## 3. Modelo matematico y signos

Convencion: las corrientes de rama se orientan segun el orden del netlist; en la incidencia reducida `+1` significa que la rama sale del nodo y `-1` que entra.

Para un op-amp ideal:

- No se agregan corrientes de entrada ni stamps de conductancia desde `NP` o `NM`.
- Se impone `V(NP)-V(NM)=0` bajo la hipotesis de operacion lineal.
- Se agrega una incognita auxiliar `I(U1)` sin relacion constitutiva entre su valor y el voltaje de salida.
- La columna de esa incognita se agrega con coeficiente `+1` en KCL del nodo `OUT`, salvo que `OUT` sea referencia. La corriente puede tomar cualquiera de los signos para representar entrega o absorcion.

Con `n` nodos no de referencia, `p` ramas fuente ideal de voltaje y `q` op-amps, el orden del vector es `X=[Vn; Iv; Iop]`, de dimension `n+p+q`:

```text
[ G    Bv    Cop ] [ Vn  ]   [ -A J ]
[ Bv^T  0     0  ] [ Iv  ] = [  Ev  ]
[ Dop   0     0  ] [ Iop ]   [   0  ]
```

- `A`: matriz de incidencia reducida, conservando el orden de nodos y ramas de los artefactos.
- `G = A diag(y_branch) A^T`: matriz nodal ensamblada desde los stamps admitidos.
- `J`: fuentes independientes de corriente, en orientacion de rama; su contribucion a KCL es `-A J`.
- `Bv`: columnas de incidencia para fuentes ideales de voltaje; `Ev` contiene sus valores fasoriales/DC.
- `Cop`: incidencia de corrientes auxiliares de op-amp, con `+1` en su nodo de salida no referencia.
- `Dop`: una fila por op-amp, con `+1` en `NP`, `-1` en `NM`; los pines en referencia contribuyen implicitamente cero.

El sistema debe ser cuadrado y conservar etiquetas, orden, bloques, terminales y metadatos de origen. No invertir la matriz explicitamente para resolver.

## 4. Analisis y tratamiento de fuentes

- **DC:** capacitores tratados segun el modelo DC de componentes aprobado; inductores ideales requieren corriente auxiliar/restriccion conforme a la implementacion MNA. La interfaz debe informar errores de singularidad o condicion.
- **AC puntual o barrido:** frecuencias finitas y positivas. Los componentes R/G/C/L y las fuentes AC usan los stamps compartidos existentes; el sistema se ensambla/resuelve por frecuencia.
- Los fasores se almacenan como pares `real`/`imag`; las frecuencias se expresan en Hz. La magnitud AC declarada es el fasor del netlist; no atribuirle interpretacion pico o RMS para un modelo fisico sin especificacion expresa.
- `.OPAMP` no define fuente de excitacion ni seleccion de observables. El usuario debe proporcionar esos datos y, para transferencia, acordar etiquetas exactas de entrada y salida.

## 5. Arquitectura y contratos de herramientas

1. `validate_netlist.py` comprueba la directiva y emite diagnosticos estructurados; se exige `PASS` antes de parseo/construccion.
2. `parse_netlist.py` conserva la directiva, terminales y trazabilidad.
3. `build_circuit_model.py` guarda los op-amps como dispositivos multipuerto separados de las ramas pasivas.
4. `build_oriented_graph.py` conserva los tres terminales como metadatos `opamps`; no inventa una arista orientada para el dispositivo.
5. `build_incidence_matrix.py` conserva la incidencia de ramas fisicas de dos terminales; las restricciones multipuerto se almacenan aparte.
6. `build_mna_system.py` ensambla la matriz MNA y reporta `unknown_order`, `equation_order`, bloques, matrices y terminales.
7. `solve_linear_system.py` resuelve el sistema MNA y recupera voltajes, corrientes de fuentes y corrientes auxiliares.
8. `validate_solution.py` valida rango/condicion, residuo lineal, KCL, voltajes de fuentes ideales, restriccion diferencial del op-amp y admitancias de rama.
9. `solve_ac_sweep.py --formulation MNA` produce estado global y estado/validacion por frecuencia; no ocultar puntos fallidos.
10. `plot_results.py` y `generate_report.py` consumen solo artefactos coherentes y verificados. El informe indica topologia, terminales, formulacion, estados, supuestos y limitaciones.

Los ensambladores nodal clasico y Tableau rechazan circuitos que contengan `.OPAMP` en lugar de omitir el dispositivo. `stamp_elements.py` es un modulo importable, no un comando CLI independiente.

## 6. Errores y puertas de aceptacion

Rechazar con diagnostico explicito antes de presentar resultados cuando haya directiva/modelo desconocido, nombre duplicado, terminal faltante/invalido, dimensiones u orden de incidencia incompatibles, valores no finitos o frecuencia AC invalida.

Una solucion se acepta solo con estado `PASS` de solver y `validate_solution.py`. Ante matriz singular, restricciones incompatibles, mal condicionamiento que exceda limite, residuo fuera de tolerancia o punto de barrido fallido, no describir el resultado como correcto. `WARN` debe reportarse sin ocultar el diagnostico.

## 7. Pruebas y aceptacion implementadas

- No inversor con fuente AC ideal de prueba y `RA=RB=10 kOhm`: MNA valida y los voltajes de salida/entrada coinciden con la referencia analitica de ganancia 2 para el modelo ideal.
- Filtro activo objetivo: validador `PASS`, analisis MNA AC de 61 puntos desde 1 Hz hasta 1 MHz, estado/validacion `PASS` por punto.
- Validacion de restriccion `V(NP)=V(NM)`, KCL, fuentes ideales y corrientes auxiliares.
- Rechazo de op-amps por ensambladores nodal y Tableau.
- Diagnosticos de modelo `.OPAMP` invalido e identificador duplicado.
- Grafo/reporting preservan metadatos de los tres pines.
- Regresion: `python -m unittest -v test_extended_tools.py` (15 pruebas) y `python test_integration.py` pasaron en la ejecucion registrada el 2026-11-02.

Los estados de prueba son evidencia de la implementacion local; no son comparacion SPICE externa. La validacion independiente requiere una referencia compatible proporcionada con modelo, circuito, unidades, frecuencias y convenciones coincidentes.

## 8. Limitaciones y extensiones futuras

Este modelo no es un op-amp real ni un modelo no lineal de saturacion. No extrapolar a comportamiento fisico, estabilidad, producto ganancia-ancho de banda, transitorio o limites de potencia. Extensiones como rieles/saturacion, slew rate, ancho de banda finito, ruido y modelos de fabricante requieren especificacion separada, aprobacion, implementacion y pruebas propias.

## 9. Aprendizajes tecnicos

- Un bloque de tres terminales requiere preservar los pines y una incognita auxiliar; la matriz de incidencia ordinaria de ramas no basta para describir la restriccion diferencial.
- La corriente de entrada cero se expresa por ausencia de stamps de entrada; la corriente de salida entra en KCL como incognita, no como una fuente fijada externamente.
- `V+=V-` solo se impone bajo operacion lineal compatible; la ausencia de saturacion puede permitir tensiones ilimitadas.
- Parser, grafo, ensamblador, solver, validador, barrido y reporte deben tratar el dispositivo consistentemente; aceptar sintaxis no basta.
- La validacion interna y el exito de cada punto no sustituyen una comparacion cuantitativa con una referencia externa compatible.
