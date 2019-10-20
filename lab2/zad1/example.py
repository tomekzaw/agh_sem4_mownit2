import numpy as np
import zad1

# generate random matrix
n = 8
AB = np.random.uniform(low=-1, high=1, size=(n, n+1))

# solve linear system using implemented algorithm
X1 = zad1.solve_gauss_jordan(AB)

# solve linear system using library function
"""
A, B = split(AB)
X2 = np.linalg.solve(A, B)
"""
X2 = np.linalg.solve(*zad1.split(AB))

# print linear system and solution
print(AB)
print(X1)
print(X2)
