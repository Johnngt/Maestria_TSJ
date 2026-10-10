# Define matrix A
A = [[1, -2, 4],
     [2, -1, 3]]

# Define matrix B
B = [[0, 2, -4],
     [1, 3, 1]]

# Calculate the sum of matrices A and B
result = []
for i in range(len(A)):
    row = []
    for j in range(len(A[i])):
        row.append(A[i][j] + B[i][j])
    result.append(row)

print("Matrix A:")
for row in A:
    print(row)

print("\nMatrix B:")
for row in B:
    print(row)

print("\nSum A + B:")
for row in result:
    print(row)