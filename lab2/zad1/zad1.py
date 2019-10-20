import numpy as np

def split(AB):
    A = AB[:,:-1]
    B = AB[:,-1] # last column
    return A, B

def solve_gauss_jordan(AB):
    if AB.ndim != 2:
        raise Exception("Matrix is not 2-dimensional")

    n, m = AB.shape
    if n != m-1:
        raise Exception("Matrix has incorrect size")

    AB = AB.copy()
    colswaps = []
    for i in range(0, n):
        # full pivoting

        # find maximum
        mi = mj = i
        for ti in range(i, n):
            for tj in range(i, n):
                if abs(AB[ti,tj]) > abs(AB[mi,mj]):
                    mi, mj = ti, tj

        # swap rows
        if i != mi:
            AB[mi], AB[i] = AB[i], AB[mi].copy()

        # swap columns
        if i != mj:
            AB[:,mj], AB[:,i] = AB[:,i], AB[:,mj].copy()
            colswaps.append((mj, i))

        """
        # partial pivoting

        # find maximum
        mi = i
        for ti in range(i, n):
            if abs(AB[ti,i]) > abs(AB[mi,i]):
                mi = ti

        # swap rows
        if i != mi:
            AB[mi], AB[i] = AB[i], AB[mi].copy()
        """

        # Gauss-Jordan
        for j in range(0, n):
            if i != j:
                AB[j] -= (AB[j,i] / AB[i,i]) * AB[i]
                # AB[j] = AB[j] - AB[i] * (AB[j,i] / AB[i,i])

    # obtain a solution
    A, B = split(AB)
    X = np.divide(B, np.diag(A))
    
    # undo column swaps
    for i, j in reversed(colswaps):
        X[i], X[j] = X[j], X[i]

    return X
