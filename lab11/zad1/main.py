import numpy
import matplotlib.pyplot as plt
from scipy.stats import ortho_group

def normalize(v):
    return -v / numpy.linalg.norm(v)

def tomekzaw_qr(A):
    n = A.shape[0]
    Q = numpy.zeros((n, n))
    R = numpy.zeros((n, n))
    """
    # k = 1
    Q[:,0] = normalize(A[:,0])
    # k > 1
    """
    for k in range(0, n):
        Q[:,k] = A[:,k]
        for i in range(0, k):
            Q[:,k] -= numpy.dot(Q[:,i], A[:,k]) * Q[:,i]
        Q[:,k] = normalize(Q[:,k])

    for i in range(0, n):
        for j in range(i, n):
            R[i,j] = numpy.dot(Q[:,i], A[:,j])

    return Q, R

"""
A = numpy.random.rand(5, 5)

tQ, tR = tomekzaw_qr(A)
print(tQ)
print(tR)

print(' ')

nQ, nR = numpy.linalg.qr(A)
print(nQ)
print(nR)
"""

n = 8

A = numpy.random.rand(n, n)
U, S, V_T = numpy.linalg.svd(A)
S = numpy.diag(S)

results = []
for i in range(100):
    S[0,0] *= 1.5
    A = U @ S @ V_T
    # cond = numpy.linalg.cond(A)
    cond = S[0,0] / S[n-1,n-1]
    Q, _ = tomekzaw_qr(A)
    norm = numpy.linalg.norm(numpy.identity(n) - Q.T @ Q)
    results.append((cond, norm))

x, y = zip(*results)
plt.scatter(x, y)
plt.plot()
plt.show()

"""
U = ortho_group.rvs(dim=n)
V_T = ortho_group.rvs(dim=n)
Sigma = numpy.diag([(1/(i+1))**j for j in range(n)])
A = U @ Sigma @ V_T
#A = numpy.random.rand(n, n)
results = [(cond, norm) for (cond, norm) in results if cond != 0]
"""