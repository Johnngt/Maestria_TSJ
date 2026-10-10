import numpy as np


def suma_matrices():
    """Ejemplo de suma de matrices."""
    # Define matrix A
    A = np.array([[1, -2, 4],
                  [2, -1, 3]])

    # Define matrix B
    B = np.array([[0, 2, -4],
                  [1, 3, 1]])

    # Calculate the sum of matrices A and B
    result = A + B

    print("=== Suma de matrices A + B ===")
    print("Matrix A:")
    print(A)
    print("\nMatrix B:")
    print(B)
    print("\nSum A + B:")
    print(result)


def multiplicacion_matrices():
    """Ejemplo de multiplicación de matrices."""
    # Define matrix A
    A = np.array([[0.375, 0.125, 0.625],
                  [-0.3125, 0.0625, 0.3125],
                  [0.0625, 0.1875, -0.0625]])

    # Define matrix B
    B = np.array([[-16],
                  [20],
                  [0]])

    print("\n=== Multiplicación de matrices A @ B ===")
    print("Matrix A:")
    print(A)
    print(f"Shape of A: {A.shape}")

    print("\nMatrix B:")
    print(B)
    print(f"Shape of B: {B.shape}")

    # Check if matrix multiplication is possible
    print(f"\nFor matrix multiplication A @ B:")
    print(f"A is {A.shape[0]}x{A.shape[1]} and B is {B.shape[0]}x{B.shape[1]}")
    print(f"Number of columns in A ({A.shape[1]}) equals number of rows in B ({B.shape[0]}) ✓")

    # Matrix multiplication A @ B
    result_AB = A @ B
    print(f"\nMatrix multiplication A @ B:")
    print(f"Result shape: {result_AB.shape}")
    print("A @ B =")
    print(result_AB)


def inversa_matriz():
    """Ejemplo de cálculo de la inversa de una matriz."""
    # Define matrix A
    A = np.array([[4, 0, 0],
                  [0, 1, 0],
                  [-1, 1, 0]])

    print("\n=== Inversa de la matriz A ===")
    print("Matrix A:")
    print(A)
    print(f"Shape of A: {A.shape}")

    # Check if the matrix is square
    if A.shape[0] == A.shape[1]:
        print(f"\nMatrix A is square ({A.shape[0]}x{A.shape[1]})")

        # Calculate the determinant
        det_A = np.linalg.det(A)
        print(f"Determinant of A: {det_A}")

        # Check if matrix is invertible (determinant != 0)
        if abs(det_A) > 1e-10:  # Using small threshold for floating point comparison
            # Calculate the inverse
            A_inverse = np.linalg.inv(A)
            print(f"\nInverse of A:")
            print(A_inverse)

            # Verify the inverse by multiplying A * A_inverse
            verification = A @ A_inverse
            print(f"\nVerification (A @ A_inverse should be identity matrix):")
            print(verification)

        else:
            print("\nMatrix A is singular (determinant = 0) and cannot be inverted.")

    else:
        print(f"\nMatrix A is not square and cannot be inverted.")


if __name__ == "__main__":
    suma_matrices()
    multiplicacion_matrices()
    inversa_matriz()
