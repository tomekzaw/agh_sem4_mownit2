import numpy as np
import zad2

"""
n = 100
A = np.random.random(size=(n, n))
"""
A = np.matrix([[5, 3, 2], [1, 2, 0], [3, 0, 4]], dtype=np.double)
L, U = zad2.lu(A)

b = np.matrix([[1], [2], [3]]) # Ax=b => x=solve(A,b)
x1 = np.linalg.solve(A, b)

# LUx=b => L(Ux)=b => Lz=b, Ux=z => z=solve(L,b), x=solve(U,z)
z = np.linalg.solve(L, b)
x2 = np.linalg.solve(U, z)

print("A = {}".format(A))
print("L = {}".format(L))
print("U = {}".format(U))

print("x1 = {}".format(x1.transpose()))
print("x2 = {}".format(x2.transpose()))