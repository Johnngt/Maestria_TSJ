# Aprendizajes de la sesión — 2026-11-07

## Presentación de nodos en reportes

En etiquetas generadas para presentación, quitar la `N` auxiliar de prefijos como `V(NIN)` y `KCL(NN1)`, mostrando `V(IN)` y `KCL(N1)`. Conservar sin cambios los nombres reales de nodos en el netlist y los datos de cálculo; esto es solo una regla de presentación.

## Tableau cuando hay elementos no compatibles

- El op-amp ideal `.OPAMP ... IDEAL` es una extensión del proyecto que debe resolverse mediante MNA; no tratarlo como una rama pasiva Tableau.
- Si un circuito contiene un elemento que impide ensamblar Tableau completa, construir la Tableau parcial de las ramas compatibles con las herramientas deterministas del proyecto, si sus entradas lo permiten.
- Mostrar la matriz `T` con sus bloques numéricos sustituidos y las regiones coloreadas, preservando el orden de ramas/nodos y los valores de los artefactos.
- Identificar claramente el elemento excluido y explicar que la matriz parcial no representa el circuito completo ni es su solución. No inventar ecuaciones para completar los bloques.
- Diferenciar la validación del netlist, el resultado del ensamblador y la validación de cualquier solución. No declarar PASS si una etapa falló.

## Carpetas de ejecución

Para cada nuevo análisis de circuito, crear una carpeta nueva dentro de `artifacts` con la fecha en su nombre. No sobrescribir ni borrar ejecuciones anteriores.

## Ejemplo de esta sesión

En `opamp_filter_20261105_2`, el validador del netlist dio PASS. El ensamblador de Tableau rechazó el circuito completo porque contiene U1 ideal. Se generó una matriz Tableau de 19×19 para las siete ramas de dos terminales, a 10 Hz, excluyendo U1 explícitamente en una copia de artefacto; posteriormente se creó una imagen coloreada por regiones. Esa representación es parcial y no sustituye la MNA del circuito completo.

Artefacto de referencia de la imagen coloreada: `tableau_T_visualization_partial_20261107_173800_v4\tableau_T_colored_blocks_10hz.png`.

## Alcance del registro

Este archivo guarda las preferencias y aprendizajes solicitados en esta sesión. No modifica la bitácora metodológica del proyecto ni cambia automáticamente la implementación de las herramientas.