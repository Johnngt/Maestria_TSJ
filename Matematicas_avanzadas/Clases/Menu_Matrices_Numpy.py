import ast
import re

import numpy as np


def leer_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Entrada inválida. Debes ingresar un número entero.")


def parsear_matriz(entrada, filas, columnas):
    """Recibe la matriz como filas separadas por espacios o en formato de lista."""
    texto = entrada.strip()
    if not texto:
        raise ValueError("La entrada está vacía.")

    if "[" in texto:
        texto_limpio = texto.replace(";", ",")
        texto_limpio = re.sub(r"\]\s*\[", "], [", texto_limpio)
        texto_limpio = re.sub(r"(?<=\d)\s+(?=[-+\d.])", ",", texto_limpio)
        texto_limpio = re.sub(r"\s+", "", texto_limpio)

        try:
            datos = ast.literal_eval(texto_limpio)
        except (SyntaxError, ValueError):
            raise ValueError("El formato de la matriz no es válido.")

        if isinstance(datos, (int, float)):
            datos = [datos]

        if not isinstance(datos, (list, tuple)) or not datos:
            raise ValueError("La matriz debe contener al menos un valor.")

        if isinstance(datos[0], (int, float)):
            matriz = [list(datos)]
        else:
            matriz = [list(fila) for fila in datos]

    else:
        filas_texto = [fila.strip() for fila in re.split(r"[\n;]+", texto) if fila.strip()]
        if not filas_texto:
            raise ValueError("No se detectaron filas válidas.")

        matriz = []
        for fila in filas_texto:
            valores = [valor for valor in re.split(r"[\s,]+", fila) if valor]
            if not valores:
                continue
            try:
                matriz.append([float(valor) for valor in valores])
            except ValueError as exc:
                raise ValueError("Solo se permiten números reales.") from exc

    if len(matriz) != filas:
        raise ValueError(f"Se esperaban {filas} filas, pero se recibieron {len(matriz)}.")

    for fila in matriz:
        if len(fila) != columnas:
            raise ValueError(f"Cada fila debe tener exactamente {columnas} valores.")

    return matriz


def leer_matriz(nombre, filas, columnas):
    matriz = []
    print(f"\nIngrese la matriz {nombre} ({filas}x{columnas})")
    print("Formatos aceptados:")
    print("  - Filas separadas por espacios: 1 2 3")
    print("  - Matriz completa: [[1, 2, 3], [4, 5, 6]]")
    print("  - También acepta: [[1 2 3] [4 5 6]]")

    while True:
        entrada = input(
            f"Ingrese los valores de {nombre} (o presione Enter para fila por fila): "
        ).strip()

        if entrada == "":
            for i in range(filas):
                while True:
                    fila_input = input(f"Fila {i + 1} ({columnas} valores separados por espacio): ").strip()
                    valores = fila_input.split()

                    if len(valores) != columnas:
                        print(f"Debes ingresar exactamente {columnas} valores en la fila {i + 1}.")
                        continue

                    try:
                        fila = [float(valor) for valor in valores]
                        matriz.append(fila)
                        break
                    except ValueError:
                        print("Solo se permiten números reales.")
            break

        try:
            matriz = parsear_matriz(entrada, filas, columnas)
            break
        except ValueError as exc:
            print(f"{exc} Intenta nuevamente.")

    return np.array(matriz, dtype=float)


def leer_dimensiones_matriz(nombre):
    """Pide filas y columnas para una matriz; pueden ser distintas en cada matriz."""
    filas = leer_entero(f"Número de filas de {nombre}: ")
    columnas = leer_entero(f"Número de columnas de {nombre}: ")
    return filas, columnas


def suma_matrices():
    """Suma dos matrices ingresadas por el usuario."""
    print("\n=== Suma de matrices ===")
    print("Nota: para sumar, ambas matrices deben tener exactamente la misma dimensión.")
    filas_A, columnas_A = leer_dimensiones_matriz("A")
    filas_B, columnas_B = leer_dimensiones_matriz("B")

    if filas_A != filas_B or columnas_A != columnas_B:
        print("\nLas matrices deben tener la misma dimensión para sumarse.")
        return

    A = leer_matriz("A", filas_A, columnas_A)
    B = leer_matriz("B", filas_B, columnas_B)

    result = A + B
    print("\nMatriz A:")
    print(A)
    print("\nMatriz B:")
    print(B)
    print("\nResultado A + B:")
    print(result)


def multiplicacion_matrices():
    """Multiplica dos matrices ingresadas por el usuario."""
    print("\n=== Multiplicación de matrices ===")
    print("Nota: las matrices pueden tener dimensiones distintas; solo debe cumplirse que columnas de A = filas de B.")
    filas_A, columnas_A = leer_dimensiones_matriz("A")
    filas_B, columnas_B = leer_dimensiones_matriz("B")

    if columnas_A != filas_B:
        print("\nNo se puede multiplicar. Debe cumplirse: columnas de A = filas de B.")
        return

    A = leer_matriz("A", filas_A, columnas_A)
    B = leer_matriz("B", filas_B, columnas_B)

    result = A @ B
    print("\nMatriz A:")
    print(A)
    print("\nMatriz B:")
    print(B)
    print(f"\nResultado A @ B ({result.shape}):")
    print(result)


def inversa_matriz():
    """Calcula la inversa de una matriz cuadrada ingresada por el usuario."""
    print("\n=== Inversa de una matriz ===")
    n = leer_entero("Ingrese el tamaño de la matriz cuadrada n: ")
    A = leer_matriz("A", n, n)

    if A.shape[0] != A.shape[1]:
        print("\nLa matriz no es cuadrada, no se puede invertir.")
        return

    det_A = np.linalg.det(A)
    print("\nMatriz A:")
    print(A)
    print(f"\nDeterminante: {det_A}")

    if abs(det_A) <= 1e-10:
        print("\nLa matriz es singular y no tiene inversa.")
        return

    A_inv = np.linalg.inv(A)
    print("\nInversa de A:")
    print(A_inv)

    print("\nVerificación (A @ A_inv):")
    print(A @ A_inv)


def mostrar_menu():
    while True:
        print("\n===== MENÚ DE OPERACIONES CON MATRICES =====")
        print("1. Suma de matrices (misma dimensión)")
        print("2. Multiplicación de matrices (pueden variar las dimensiones)")
        print("3. Inversa de una matriz")
        print("4. Salir")

        opcion = input("\nElige una opción (1-4): ")

        if opcion == "1":
            suma_matrices()
        elif opcion == "2":
            multiplicacion_matrices()
        elif opcion == "3":
            inversa_matriz()
        elif opcion == "4":
            print("\nSaliendo del programa...")
            break
        else:
            print("\nOpción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    mostrar_menu()
