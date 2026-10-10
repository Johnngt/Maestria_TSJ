import numpy as np

# Define matrix A
A = np.array([[4, 0, 0],
              [0, 1, 0],
              [-1, 1, 0]])

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