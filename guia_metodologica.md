# Guía metodológica — Custom Agent educativo para simulación de circuitos tipo SPICE
Netlist → Grafo orientado → Matrices → Solución → Validación
Profesor: Dr. Francisco E. Rangel-Patiño
Matemáticas Avanzadas · Programa 2026
Maestría en Ingeniería Electrónica
Tecnológico Superior de Jalisco
Versión metodológica para uso académico

## Propósito del documento
Orientar a los estudiantes en la construcción gradual, verificable y explicable de un agente basado en GitHub Copilot que analice netlists y ejecute un motor determinista de simulación desarrollado en Python.

## Cómo utilizar esta guía
La guía organiza el proyecto como una experiencia de ingeniería basada en evidencia. El objetivo no es pedirle a un modelo de lenguaje que calcule matrices, sino construir un agente que orqueste herramientas deterministas, explique el procedimiento y entregue resultados verificables.

### Principio rector
El agente interpreta, coordina y explica. Los scripts de Python procesan, ensamblan, resuelven y validan. Ningún resultado matricial debe depender únicamente de generación de texto.
