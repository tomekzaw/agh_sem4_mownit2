import numpy as np

def lu(A):
    if A.ndim != 2:
        raise Exception("Matrix is not 2-dimensional")
    m, n = A.shape
    if m != n:
        raise Exception("Matrix is not square")
    A = A.copy()

    """
    # scaling
    for i in range(n):
        div = abs(A[i]).max()
        if div != 0:
            A[i] /= div
    """

    # LU factorization
    L = np.identity(n) # Doolittle's method
    U = np.zeros((n, n))
    for k in range(n):
        for j in range(k, n):
            U[k,j] = A[k,j] - sum([L[k,s]*U[s,j] for s in range(k)])
        for i in range(k+1, n):
            L[i,k] = (A[i,k] - sum([L[i,s]*U[s,k] for s in range(k)])) / U[k,k]
    return L, U
