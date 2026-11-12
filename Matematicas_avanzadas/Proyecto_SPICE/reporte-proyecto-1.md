# Proyecto de la Unidad I: Desarrollo de un Custom Agent para Simulación Explicable de Circuitos

**Programa:** Matemáticas Avanzadas (Programa 2026)[cite: 1]  
**Institución:** Tecnológico Superior de Jalisco | Maestría en Ingeniería Electrónica[cite: 1]  
**Profesor:** Dr. Francisco E. Rangel-Patiño[cite: 1]  
**Temas Clave:** Netlist, Grafo, Matrices, Análisis AC, Ganancia, Validación[cite: 1]

---

## 1. Reto Central y Propósito del Proyecto

El reto central consiste en completar las herramientas faltantes, integrar 10 *skills* especializados y construir un agente de GitHub Copilot capaz de analizar un filtro activo, obtener su respuesta en frecuencia y comparar la magnitud y la fase frente a un simulador SPICE[cite: 1].

### Propósito del proyecto
Integrar el álgebra lineal, la teoría de grafos, la formulación nodal, Tableau, el análisis fasorial y el desarrollo de agentes[cite: 2]. El resultado final es un **agente educativo** que recibe un *netlist*, construye los artefactos matemáticos del circuito, resuelve el análisis AC y explica paso a paso la obtención de cada resultado[cite: 2].

> **Nota importante sobre el resultado esperado:** El agente no debe funcionar como una caja negra. Cada voltaje, corriente, matriz, gráfica y métrica de validación conservará completa trazabilidad hasta el *netlist* y sus ecuaciones constitutivas[cite: 2].

---

## 2. Circuito Objetivo y Especificaciones

El circuito objetivo es un **filtro activo** compuesto por:
* Dos capacitores de entrada ($C_1$, $C_2$)[cite: 2].
* Una red de realimentación mediante una conductancia $G_1$[cite: 2].
* Una conductancia $G_2$ conectada a tierra[cite: 2].
* Un amplificador operacional no inversor con resistores $R_A$ y $R_B$[cite: 2]. 
  *(Nota: El agente modelará el amplificador operacional ideal mediante la formulación aprobada en el curso)[cite: 2].*

### Parámetros de simulación y valores nominales
* **Rango de frecuencia:** 300 puntos de frecuencia desde $10\text{ Hz}$ hasta $100\text{ kHz}$[cite: 2].
* **Componentes:** 
  * $R_A = 1.27\text{ k}\Omega$[cite: 2]
  * $R_B = 2.3\text{ k}\Omega$[cite: 2]
  * $G_1 = 1 / R_A$[cite: 2]
  * $G_2 = 1 / R_B$[cite: 2]
  * $C_1 = C_2 = 0.1\text{ }\mu\text{F}$[cite: 2]
* **Excitación:** $|V_i| = 1\text{ mV}$ para todas las frecuencias[cite: 2]. Condiciones iniciales iguales a cero[cite: 2].
* **Ecuación a resolver:** Análisis Nodal Modificado (MNA) para determinar $V_{ni}$ (vector de voltajes nodales) e $I_z$[cite: 2].

---

## 3. Objetivos de Aprendizaje

* Aplicar teoría de grafos y matrices a un circuito electrónico real[cite: 3].
* Convertir un *netlist* en un modelo computacional reproducible[cite: 3].
* Construir matrices de incidencia y formulaciones de circuitos[cite: 3].
* Implementar análisis nodal, Tableau y análisis AC utilizando `NumPy`[cite: 3].
* Diseñar herramientas (*tools*) deterministas para un Custom Agent de GitHub Copilot[cite: 3].
* Aplicar validación matemática, eléctrica y numérica[cite: 3].
* Comparar resultados contra un simulador SPICE y comunicar las diferencias de manera técnica[cite: 3].

---

## 4. Requerimientos Funcionales del Agente

1. Recibir como entrada un *netlist* compatible con el subconjunto documentado[cite: 3].
2. Validar sintaxis, unidades, nodo de referencia y componentes soportados[cite: 3].
3. Identificar componentes, nodos, ramas y su orientación[cite: 3].
4. Generar y mostrar el grafo orientado[cite: 3].
5. Generar la matriz de incidencia completa y reducida con sus respectivos encabezados[cite: 3].
6. Construir las matrices constitutivas requeridas por el método seleccionado[cite: 4].
7. Modelar las ramas especiales asociadas con la fuente de entrada y el amplificador operacional ideal[cite: 4].
8. Ensamblar y resolver el sistema lineal para cada frecuencia de la red[cite: 4].
9. Calcular la función de transferencia $H(j\omega) = V_o / V_i$[cite: 4].
10. Calcular la ganancia en decibeles ($\text{dB}$) y la fase en grados[cite: 4].
11. Generar gráficas comparables con los resultados de SPICE[cite: 4].
12. Validar residuos, leyes de corrientes de Kirchhoff (KCL), leyes de tensiones de Kirchhoff (KVL) y ecuaciones constitutivas[cite: 4].
13. Generar un reporte explicable y reproducible[cite: 4].

---

## 5. Cálculos Obligatorios

* **Función de transferencia:** 
  $$H(j\omega) = \frac{V_o(j\omega)}{V_i(j\omega)}$$
* **Ganancia en decibeles:** 
  $$\text{Ganancia\_dB} = 20 \log_{10}(|H(j\omega)|)$$
* **Fase en grados:** 
  $$\text{Fase\_deg} = \text{angle}(H(j\omega)) \cdot \frac{180}{\pi}$$

> *Nota:* La fase deberá desenvolverse (*unwrap*) cuando sea necesario para evitar saltos artificiales de $\pm 180^{\circ}$[cite: 4]. Las gráficas deben emplear escala logarítmica en la frecuencia e incluir unidades, títulos, leyendas y etiquetas claras[cite: 4].

---

## 6. Arquitectura de Trabajo (Materiales Proporcionados vs. Por Desarrollar)

### 6.1 Materiales Proporcionados por el Profesor
* **Guía Metodológica (`Guia_Metodologica_Custom_Agent_SPICE_Educativo.md`):** Arquitectura general, responsabilidades, convenciones, flujo determinista, validación y pruebas[cite: 5].
* **Planes de desarrollo (`PLAN_01` y `PLAN_02`):** Guías de planeación para auditar e integrar herramientas y *skills* mediante GitHub Copilot (Plan Mode)[cite: 5].
* **Skills del Agente:** 10 carpetas/archivos con conocimiento especializado[cite: 5].
* **Scripts iniciales (`SPICE_Educational_Agent_First_6_Python_Tools.zip`):** Seis herramientas base en Python[cite: 5].

### 6.2 Inventario de Herramientas (Scripts de Python)

| # | Script Inicial (Proporcionado) | Responsabilidad |
|---|---|---|
| 1 | `parse_netlist.py` | Interpretar el subconjunto educativo del *netlist*[cite: 5]. |
| 2 | `build_circuit_model.py` | Crear nodos, ramas y objetos del dominio[cite: 5]. |
| 3 | `build_oriented_graph.py` | Construir y exportar el grafo dirigido[cite: 5]. |
| 4 | `build_incidence_matrix.py` | Generar la matriz de incidencia completa y reducida[cite: 5]. |
| 5 | `build_nodal_system.py` | Ensamblar el sistema nodal compatible[cite: 5]. |
| 6 | `solve_linear_system.py` | Resolver, recuperar variables y validar KCL[cite: 5]. |

| # | Script Requerido (Por Desarrollar) | Responsabilidad Principal |
|---|---|---|
| 1 | `validate_netlist.py` | Validación detallada, control de errores y alcance soportado[cite: 6]. |
| 2 | `stamp_elements.py` | *Stamps* deterministas de elementos lineales y ramas especiales[cite: 6]. |
| 3 | `build_constitutive_matrices.py` | Construcción trazable de matrices $Y$, $Z$ y $W$[cite: 6]. |
| 4 | `build_tableau_system.py` | Ensamble del sistema Tableau ($T$, $W'$) y mapas de índices[cite: 6]. |
| 5 | `solve_ac_sweep.py` | Barrido de frecuencia y extracción de $H(j\omega)$[cite: 6]. |
| 6 | `validate_solution.py` | Validación matemática, eléctrica y numérica[cite: 6]. |
| 7 | `compare_reference.py` | Comparación cuantitativa frente a los resultados de SPICE[cite: 6]. |
| 8 | `generate_report.py` | Generación de reportes explicables en formatos Markdown/JSON[cite: 6]. |
| 9 | `plot_results.py` | Trazado de gráficas de ganancia en $\text{dB}$ y fase en grados[cite: 6]. |

---

## 7. Skills que debe Integrar el Agente

El agente debe integrar formalmente los siguientes 10 *skills* que contienen la metodología teórica, los cuales interactúan de forma directa con los *tools* ejecutables[cite: 6]:

1. `spice-netlist-fundamentals`[cite: 6]
2. `circuit-graph-theory`[cite: 6]
3. `incidence-matrix-method`[cite: 6]
4. `component-constitutive-models`[cite: 6]
5. `classical-nodal-analysis`[cite: 6]
6. `tableau-formulation`[cite: 6]
7. `ac-frequency-analysis`[cite: 6]
8. `engineering-units-and-conventions`[cite: 6]
9. `solver-validation`[cite: 6]
10. `explainable-circuit-reporting`[cite: 6]

---

## 8. Procedimiento de Desarrollo Paso a Paso

* **Paso 1. Preparar el repositorio:** Organizar la estructura separando agentes, *prompts*, *skills*, código fuente, pruebas y artefactos conforme a la guía metodológica[cite: 7].
* **Paso 2. Estudiar el material:** Revisar exhaustivamente la guía, los archivos de *skills* y los 6 scripts iniciales para comprender la representación de nodos, ramas y unidades[cite: 7].
* **Paso 3. Utilizar PLAN_01:** Ejecutar el plan inicial con GitHub Copilot para definir dependencias, interfaces, algoritmos y pruebas de los 9 scripts restantes[cite: 7].
* **Paso 4. Desarrollar los 9 scripts Python restantes:** Implementar cada uno de los módulos de soporte algorítmico y matemático[cite: 8].
* **Paso 5. Utilizar PLAN_02:** Auditar la integración de los 15 *tools* y los 10 *skills* mediante el segundo plan de trabajo[cite: 8].
* **Paso 6. Corregir discrepancias (*gaps*):** Resolver incompatibilidades de interfaces, orden de nodos, inversión de signos o problemas con el OpAmp ideal[cite: 8].
* **Paso 7. Construir el Custom Agent:** Crear la definición del agente en `.github/agents/basic-spice-agent.agent.md` garantizando que delegue los cálculos numéricos a las herramientas deterministas[cite: 8, 9].
* **Paso 8. Calificar el agente:** Alimentar al agente con el *netlist* oficial del circuito de la Unidad I para generar el reporte técnico completo[cite: 10].
* **Paso 9. Comparar contra SPICE:** Contrastar cuantitativamente las curvas de magnitud y fase bajo condiciones equivalentes[cite: 10].

---

## 9. Validación y Criterios frente a SPICE

La validación se realiza utilizando un entorno equivalente en SPICE (topología, fuentes, componentes, amplitud de entrada y barrido)[cite: 10]:

| Métrica de Validación | Requisito de Evaluación |
|---|---|
| **Magnitud** | Control de error absoluto y relativo en puntos de frecuencia seleccionados. |
| **Fase** | Diferencia angular en grados con un tratamiento consistente de *wrapping*. |
| **Frecuencia característica** | Comparación del punto de transición/corte identificado por ambos métodos. |
| **Ganancia de banda** | Comparación del valor estable dentro de la región de operación. |
| **Residuos** | Comprobación de que el sistema matemático cumple con las tolerancias establecidas. |

---

## 10. Entregables del Proyecto

1. **Repositorio Git:** Código fuente, definición del agente, 10 *skills*, *prompts*, pruebas unitarias y documentación.
2. **Nueve scripts desarrollados:** Implementaciones completas con encabezados, autor, *docstrings* y interfaz de línea de comandos (CLI).
3. **Netlist final:** Archivo que describe el circuito objetivo y la configuración del barrido AC.
4. **Reporte técnico:** Documento con bases matemáticas, arquitectura, resultados, validación y limitaciones.
5. **Demo del agente:** Demostración de ejecución desde la lectura del *netlist* hasta la emisión del reporte final.
6. **Comparación SPICE:** Datos tabulados, gráficas comparativas y métricas de diferencia.
7. **Presentación final:** Resumen ejecutivo y defensa técnica del proyecto.