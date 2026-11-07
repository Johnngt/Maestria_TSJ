# Alcance de la matriz visualizada

La matriz Tableau se ensamblara con la herramienta del proyecto a partir de las matrices de incidencia y constitutivas reportadas para las siete ramas de dos terminales. Se usa una copia derivada del modelo de circuito donde U1 se excluye expresamente; no se modifica el modelo de la ejecucion original ni el netlist fuente.

U1 ideal no es una rama pasiva y el ensamblador oficial lo rechaza para el circuito completo. Por tanto, la matriz generada es Tableau del subcircuito de ramas representables, no una formulacion completa ni una solucion del filtro con op-amp.
