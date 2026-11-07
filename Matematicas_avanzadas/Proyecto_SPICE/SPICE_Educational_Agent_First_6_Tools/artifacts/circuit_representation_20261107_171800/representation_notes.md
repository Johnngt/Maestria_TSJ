# Esquema complementario del filtro activo

- Fuente de entrada: `opamp_active_filter.cir`; validacion del netlist: **PASS** (`netlist_validation.json`).
- El dibujo muestra los siete elementos de dos terminales y el op-amp ideal U1 conectado a `NP`, `NM` y `OUT`.
- Los nombres y valores de componentes se copiaron del netlist; no se modificaron el netlist ni los artefactos de la ejecucion original.
- U1 se representa como bloque ideal lineal con entradas sin corriente, restriccion `V(NP)=V(NM)` durante operacion lineal y corriente de salida auxiliar en MNA. No se modelan rieles ni saturacion.
- Este dibujo documenta conectividad; no es una matriz Tableau ni sustituye la solucion MNA validada.
- Referencia MNA de la ejecucion original: `..\opamp_filter_20261105_2\mna_10hz.json`.
