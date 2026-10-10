import numpy as np

# Define matrix A
#A = np.array([[1, 2, 3],
#              [0, 1, 4]])
A = np.array([[ 0.375,   0.125,   0.625 ],
                [-0.3125,  0.0625,  0.3125],
                [ 0.0625,  0.1875, -0.0625]])

# Define matrix B
#B = np.array([[-1, 2],
#              [2, 3],
#              [5, 0]])
B = np.array([[-16],[20],[0]])

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