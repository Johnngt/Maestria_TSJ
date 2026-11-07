# Especificacion tecnica propuesta: modelado de transistores

- **Fecha:** 2026-11-02
- **Estado:** propuesta de aprendizaje; pendiente de aprobacion docente y de implementacion
- **Alcance actual:** este documento no habilita el parser ni autoriza a presentar resultados de transistores. El MVP vigente no soporta semiconductores ni analisis no lineal general.

## 1. Objetivo

Definir los contratos de modelo, datos, ensamblaje, solucion, validacion y pruebas necesarios para una extension educativa del simulador que incluya transistores. Los calculos deberan ejecutarse mediante herramientas deterministas del proyecto. No se deben aproximar dispositivos con redes de componentes pasivos ni asumir que aceptar una linea en el parser significa que el modelo esta implementado.

## 2. Alcance candidato por fases

La eleccion de modelos y supuestos es una decision pendiente del curso. Como alcance didactico inicial se propone:

1. **BJT:** modelo estatico Ebers-Moll, con polaridades NPN y PNP, incluyendo las corrientes de ambas junturas y acoplamiento de transporte directo/inverso. No presentarlo como Gummel-Poon ni como modelo de transistor moderno de precision.
2. **MOSFET:** modelo de canal largo Shichman-Hodges de nivel 1, con modos NMOS y PMOS y regiones de corte, lineal/triodo y saturacion. Definir explicitamente si el primer alcance incluye modulacion de longitud de canal (`lambda`) y efecto de cuerpo; no asumirlos por defecto.
3. **Analisis inicial:** punto de operacion DC no lineal mediante MNA y Newton amortiguado. AC de pequena senal solo despues de converger un punto DC y solo con la matriz Jacobiana del modelo aprobado.
4. **Fuera de alcance inicial:** JFET, IGBT, modelos Gummel-Poon completos, BSIM, subcircuitos de fabricante, ruido, temperatura variable, auto calentamiento, avalancha, ruptura, carga/descarga dinamica y analisis transitorio. Extenderlos requiere especificacion y pruebas separadas.

La lista anterior es una propuesta para acotar una primera fase, no una seleccion aprobada. El curso debe aprobar las familias y variantes exactas antes de codificar.

## 3. Convenciones y contrato de dispositivo

- Mantener la referencia `0`/`GND`, el orden estable de nodos y la orientacion existente de ramas.
- Preservar cada transistor como dispositivo multipuerto tipado, separado de las ramas pasivas: BJT `Qname C B E [S]`; MOSFET `Mname D G S B`. La presencia de terminales repetidos y terminales omitidos debe seguir reglas explicitas del modelo, no una normalizacion silenciosa.
- Crear un esquema comun con: identificador, familia, polaridad/tipo, orden de pines, nombre del modelo, parametros con unidades, linea original, numero de linea y procedencia de parametros.
- Cada modelo debera exponer una funcion de corrientes terminales no lineales y su Jacobiana local respecto de voltajes terminales; conservar convencion de signo y orden en ambos contratos. La suma algebraica de corrientes terminales debe ser cero dentro de tolerancia.
- El stamp local debe ensamblarse en los nodos globales con KCL y derivadas coherentes. No convertir un dispositivo de tres/cuatro terminales en una rama diagonal Y/Z/W.
- Parametros obligatorios y opcionales, unidades, rangos, temperatura y valores por defecto deben quedar enumerados para cada modelo. No inventar defaults ni mezclar parametros de modelos distintos.

## 4. Modelos y datos

### BJT Ebers-Moll (candidato)

La definicion aprobada debe fijar las ecuaciones de corrientes de colector/base/emisor, orientaciones de las junturas base-emisor y base-colector, polaridad NPN/PNP, corrientes de saturacion, factores de transporte y convencion de signos. Debe especificar el rango de validez y como se trata numericamente la dependencia exponencial para evitar overflow sin cambiar el modelo de forma no documentada. Ebers-Moll estatico no implica automaticamente capacitancias de juntura, carga almacenada ni efectos de alta frecuencia.

### MOSFET Shichman-Hodges nivel 1 (candidato)

La definicion aprobada debe fijar las ecuaciones por region, convenciones D/S, conversion para NMOS/PMOS, polaridad del cuerpo, comportamiento de diodo de cuerpo y tratamiento de operaciones inversas. Debe acordar si `lambda`, efecto de cuerpo, conductancias de juntura y capacitancias entran en la primera version. Documentar la suavidad/discontinuidad entre regiones y las consecuencias para la convergencia de Newton.

### Tarjetas de modelo / netlist

Antes de implementar, aprobar una gramatica para instancias y definiciones de modelo. Debe decidir si se aceptara un subconjunto propio tipo `.MODEL` o una sintaxis SPICE concreta, especificando dialecto y compatibilidad real. Validar nombres unicos, pines, tipo de dispositivo, parametros desconocidos, unidades, finitud y rangos; producir diagnosticos con linea, codigo y sugerencia. Una instancia sin modelo o con modelo de polaridad incompatible debe fallar antes de construir el sistema.

## 5. Ensamblaje y algoritmo no lineal

- Formular DC como `F(x)=0`, donde `x` incluye voltajes nodales y corrientes auxiliares de fuentes ideales segun la MNA vigente.
- Cada iteracion evaluara el residuo y Jacobiano globales, resolvera el sistema lineal `J(x_k) * delta_x = -F(x_k)` y actualizara el estado usando una politica de amortiguamiento aprobada.
- Evitar invertir la matriz explicitamente. Reportar iteraciones, norma de residuo, norma de paso, rango/condicion cuando se puedan calcular y estado final.
- Definir criterios separados y con unidades/tolerancias documentadas para convergencia absoluta y relativa de voltajes, corrientes y residuos KCL/constitutivos. Definir limites de iteracion, estrategia de inicializacion, damping/line-search y que diagnosticos se emiten ante singularidad, falta de convergencia u overflow.
- Evaluar source stepping, conductance stepping o inicializacion heuristica solo como tecnicas seleccionadas y verificadas; no ocultar que alteran el camino de solucion. La falta de convergencia no debe transformarse en un `PASS` ni en una solucion de aspecto valido.
- Los stamps no lineales deben conservar la trazabilidad a dispositivo, modelo, parametros, terminales y linea fuente.

## 6. AC de pequena senal y transitorio

- AC requiere un punto DC convergido y validado. Linealizar cada dispositivo con la Jacobiana en ese punto y combinarla con los elementos lineales AC.
- Declarar si se incluyen capacitancias internas de juntura/difusion del BJT, capacitancias de compuerta del MOSFET y dependencias con frecuencia. Si no se incluyen, etiquetar el modelo como estatico de pequena senal, no usarlo para afirmar ancho de banda/transitorios del transistor.
- Analisis transitorio debe ser una fase independiente: requiere modelos de carga/estado, integracion numerica (por ejemplo, metodo y orden aprobados), control de paso temporal, inicializacion, eventos, tolerancias y pruebas de estabilidad. No inferir un transitorio a partir del modelo DC/AC.

## 7. Arquitectura prevista

1. Ampliar validador/parser y modelo normalizado sin perder lineas fuente ni orden de pines.
2. Implementar cada modelo semiconductor en un modulo importable con evaluacion de corrientes y Jacobiana local.
3. Integrar stamps en el ensamblador MNA no lineal; conservar inalterados los caminos nodal/Tableau lineales existentes.
4. Introducir un solver Newton no lineal independiente de la solucion lineal existente, con resultado estructurado y diagnosticos explicitos.
5. Actualizar validacion para KCL, ecuaciones de dispositivo, residuos, convergencia, valores finitos y restricciones de fuentes.
6. Soportar AC solo tras DC PASS; bloquear AC si no existe punto de operacion valido.
7. Actualizar grafo/reporte para representar terminales multipuerto y mostrar modelo, parametros, supuestos, convergencia y limitaciones.
8. Cada cambio requiere README/skills/agente consistentes, solo despues de aprobacion. No modificar herramientas actuales para simular una funcionalidad todavia no aprobada.

## 8. Plan de pruebas y aceptacion

- **Validacion de netlist:** terminales faltantes, nombres duplicados, modelo ausente, tipo/polaridad incompatibles, parametro desconocido, unidad/rango invalido, NaN/Inf y directivas no soportadas; deben fallar antes de ensamblar.
- **Dispositivo aislado:** barridos de terminales en cada region de funcionamiento, signos de corrientes, conservacion de carga/corriente terminal y consistencia de Jacobiana contra diferencias finitas en puntos de prueba aprobados.
- **Puntos de operacion:** corte, conduccion y regiones de frontera para cada polaridad; validar residuos de KCL y del modelo. Probar circuitos singulares, flotantes e incompatibles y exigir error explicito o diagnostico `WARN` segun criterio aprobado.
- **No linealidad:** convergencia desde varias inicializaciones, amortiguamiento, parametros extremos permitidos, overflow, numero maximo de iteraciones y problemas mal condicionados.
- **AC:** comprobar linealizacion alrededor de un DC validado, frecuencias positivas, unidades, respuesta de cada dispositivo segun las dinamicas incluidas y bloqueo cuando falla DC.
- **Regresion:** repetir todos los tests lineales existentes (nodal, Tableau, op-amp MNA y AC lineal) y verificar que resultados/esquemas previos no cambian.
- **Referencias independientes:** usar resultados analiticos solo dentro de la validez del modelo; para SPICE externo, registrar motor/version, modelo exacto, temperatura, opciones, parametros, condiciones, unidades y puntos comparados. No generar referencias artificiales ni comparar una ejecucion consigo misma.
- **Reporte:** incluir variante exacta del modelo, parametros efectivos y su procedencia, metodo/tolerancias del solver, estado por punto, warning/limitaciones y referencia externa si se proporciono.

## 9. Aprobaciones previas requeridas

Antes de implementar deben aprobarse: familias y variantes exactas (BJT/MOSFET); ecuaciones y convenciones de pines/signos; parametros y defaults; sintaxis/dialecto del netlist; condiciones de temperatura; estrategia/tolerancias de Newton; alcance de AC interno; exclusiones de transitorio; fixtures de referencia y criterios de aceptacion. Hasta esa aprobacion, la herramienta debe rechazar transistores como no soportados y el agente debe explicitar la limitacion.

## 10. Aprendizajes registrados

- Un transistor es un dispositivo multipuerto no lineal; no se puede incorporar como una admitancia constante ni como una rama pasiva Tableau sin linearizacion en un punto de operacion.
- MNA lineal por si sola no resuelve el problema: DC requiere residuos y Jacobianos no lineales, un metodo iterativo y puertas explicitas de convergencia.
- AC de pequena senal depende de un punto DC valido y solo representa dinamicas incluidas por el modelo; un modelo estatico no autoriza conclusiones de ancho de banda ni transitorio.
- El nombre de una familia de modelos no basta para reproducibilidad: version/variante, parametros, convenciones, temperatura y defaults tambien forman parte del contrato.
- Aceptar sintaxis en el parser no significa que el dispositivo ni su solver esten implementados. Sin implementacion aprobada, diagnosticar y detener en lugar de aproximar o inventar resultados.
