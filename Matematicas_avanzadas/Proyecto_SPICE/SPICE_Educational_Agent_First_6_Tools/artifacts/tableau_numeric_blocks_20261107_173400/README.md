# Composicion Tableau con matrices reportadas

La imagen inserta las matrices numericas directamente desde los artefactos generados de la ejecucion `opamp_filter_20261105_2`: `incidence.json` (A reducida) y `constitutive_10hz.json` (Y, Z y W). El punto constitutivo es AC a 10 Hz. Se conserva el orden de ramas `B1..B7` y nodos reducidos `IN, N1, NM, NP, OUT`.

**Alcance:** el netlist valida PASS, pero incluye `.OPAMP U1 NP NM OUT IDEAL`. El ensamblador de Tableau fallo explicitamente indicando que el op-amp ideal requiere MNA. Por eso esta figura muestra la composicion por bloques y sus matrices fuente para las siete ramas de dos terminales; no afirma que exista una matriz Tableau completa del circuito, no incorpora U1 como rama pasiva y no es una solucion validada.

Los coeficientes complejos se muestran redondeados a 6 cifras significativas para legibilidad; los valores completos se conservan en `..\opamp_filter_20261105_2\constitutive_10hz.json`.
