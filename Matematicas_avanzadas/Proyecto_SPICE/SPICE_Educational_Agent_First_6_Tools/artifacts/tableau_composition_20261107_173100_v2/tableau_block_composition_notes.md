# Composicion estructural Tableau

- Circuito: `opamp_active_filter.cir`; validacion del netlist: **PASS**.
- Punto constitutivo: AC, 10 Hz.
- La imagen presenta los bloques estructurales usando `A_reduced` de dimensiones 5 x 7 y `Y`, `Z`, `W` de las siete ramas.
- Orden de ramas: `B1(V1), B2(C1), B3(C2), B4(G1), B5(G2), B6(RA), B7(RB)`.
- Orden nodal reducido: `IN, N1, NM, NP, OUT`. La dimension estructural es 19 x 19 para esas ramas.
- El ensamblador rechazo la matriz del circuito completo porque `U1` ideal requiere MNA. Esta visualizacion no es una matriz Tableau completa del filtro ni una solucion.
- Fuentes: `..\tableau_check_20261107_172500\incidence.json`, `..\tableau_check_20261107_172500\constitutive_10hz.json`, `..\tableau_check_20261107_172500\netlist_validation.json`.
