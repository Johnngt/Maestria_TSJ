# Matriz Tableau parcial con bloques sustituidos

La imagen se renderiza desde `tableau_partial_10hz.json`, producido por `build_tableau_system.py`. Dimensiones: T 19x19; RHS 19.

El circuito original incluye U1 ideal. Para visualizar los bloques de sus siete ramas de dos terminales, el modelo de entrada del ensamblador excluyo explicitamente U1 en una copia de artefacto. El resultado no es Tableau del circuito completo ni tiene validacion/solucion para el op-amp. U1 se resuelve por MNA en el proyecto.
