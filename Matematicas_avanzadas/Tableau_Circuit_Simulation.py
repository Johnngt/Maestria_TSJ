import numpy as np
import matplotlib.pyplot as plt


# Simulation Methods for Electronic Circuits
# Systematic Analysis of Linear and non-Linear Circuits
# Problem #1

# Sinusoidal Input
VL = 10e-3

# Circuit Component Values
R1 = 1e3
R5 = R1
R2 = 3.3e3
R3 = R2
C4 = 1e-6

# Frequency Analysis
points = 100
F_start = 10
F_stop = 1e3
freq = np.linspace(F_start, F_stop, points)

# INCIDENCE MATRIX
A = np.array([
    [1,  0,  0,  0,  1,  0,  0,  0,  0,  1],
    [0,  0,  0,  1, -1,  1,  0,  0,  0,  0],
    [-1, 0,  1,  0,  0, -1,  1,  0,  0,  0],
    [0,  1,  0,  0,  0,  0, -1,  1,  0,  0],
    [0,  0, -1,  0,  0,  0,  0, -1,  1,  0],
], dtype=float)

# IMPEDANCE MATRIX
Z = np.array([
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [1,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   0,   1,   0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,  -R1,  0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,  -R2,  0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,  -R3,  0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,  -1,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,  -R5,  0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
], dtype=float)

# SOURCE VECTOR
W = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, VL], dtype=float)

# Number of circuit nodes and branches
nodes, branches = A.shape

# Tableau equation: T*X = Wp
Wp = np.concatenate([np.zeros(branches), W, np.zeros(nodes)])

# Variable initialization (complex to match MATLAB's frequency-domain solution)
V_input = np.zeros(points, dtype=complex)
V_output = np.zeros(points, dtype=complex)
IL = np.zeros(points, dtype=complex)
ZL = np.zeros(points, dtype=complex)
ZL2 = np.zeros(points, dtype=complex)
j = 1j

for k in range(points):
    w = 2 * np.pi * freq[k]
    Y = np.zeros((branches, branches), dtype=complex)
    np.fill_diagonal(Y, [1, 0, 1, 0, 1, 1, 1, 1j * w * C4, 1, 1])

    # Assemble matrix T
    T = np.block([
        [np.eye(branches), np.zeros((branches, branches)), -A.T],
        [Y, Z, np.zeros((branches, nodes))],
        [np.zeros((nodes, branches)), A, np.zeros((nodes, nodes))],
    ])

    # Tableau equation: T*X = Wp
    X = np.linalg.solve(T, Wp)

    Vb = X[:branches]
    I = X[branches:2 * branches]
    Vn = X[2 * branches:]

    # Voltage at Node 1
    V_input[k] = Vn[0]
    IL[k] = I[4] + I[0]
    ZL[k] = V_input[k] / IL[k]

    # Circuit Analysis Equation
    ZL2[k] = 1j * w * C4 * R1 * R3 * R5 / R2
    Leq2 = C4 * R1 * R3 * R5 / R2

# Plots
plt.figure()
plt.plot(freq / 1000, np.abs(ZL) / 1000)
plt.grid(True)
plt.xlabel('Frecuency (KHz)')
plt.ylabel('ZL Tableau (KOhms)')

plt.figure()
plt.plot(freq / 1000, np.abs(ZL2) / 1000)
plt.grid(True)
plt.xlabel('Frecuency (KHz)')
plt.ylabel('ZL Circuit Analysis (KOhms)')

plt.figure()
plt.plot(freq, np.abs(IL))
plt.grid(True)
plt.xlabel('Frecuency (Hz)')
plt.ylabel('Ii (Amp)')

plt.show()
