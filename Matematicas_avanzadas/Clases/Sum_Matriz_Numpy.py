import numpy as np

# Define matrix A
A = np.array([[1, -2, 4],
              [2, -1, 3]])

# Define matrix B
B = np.array([[0, 2, -4],
              [1, 3, 1]])

# Calculate the sum of matrices A and B
result = A + B

print("Matrix A:")
print(A)
print("\nMatrix B:")
print(B)
print("\nSum A + B:")
print(result)