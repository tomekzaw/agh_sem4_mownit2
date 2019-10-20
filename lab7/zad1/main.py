import numpy as np
import scipy.linalg
import itertools

A = np.array([
    [1,2,3],
    [2,2,4],
    [3,4,1]
])

print('np.linalg.eig:')
eigvals, eigvecs = np.linalg.eig(A)
print(eigvals)
print(eigvecs)

def tomekzaw_maxeig_v1(A, eps=1e-9):
    v0 = np.identity(A.shape[0])[0] # [1,0,0,...]
    for i in itertools.count(1):
        v = v0
        v = A @ v
        v /= np.linalg.norm(v)
        if np.linalg.norm(v-v0) < eps:
            return l, v, i
        l = v.T @ A @ v
        v0 = v

def tomekzaw_maxeig_v2(A, eps=1e-9):
    v0 = np.identity(A.shape[0])[0]
    u = 8
    AuI = A-u*np.identity(A.shape[0])
    for i in itertools.count(1):
        v = v0
        w = np.linalg.solve(AuI, v)
        v = w / np.linalg.norm(w)
        if np.linalg.norm(v-v0) < eps or np.linalg.norm(v+v0) < eps:
            return l, v, i
        l = v.T @ A @ v
        v0 = v

def tomekzaw_maxeig_v2_2(A, eps=1e-9):
    v0 = np.identity(A.shape[0])[0]
    u = 8
    AuI = A-u*np.identity(A.shape[0])
    lupiv = scipy.linalg.lu_factor(AuI)
    for i in itertools.count(1):
        v = v0
        w = scipy.linalg.lu_solve(lupiv, v)
        v = w / np.linalg.norm(w)
        if np.linalg.norm(v-v0) < eps or np.linalg.norm(v+v0) < eps:
            return l, v, i
        l = v.T @ A @ v
        v0 = v

def tomekzaw_maxeig_v3(A, eps=1e-9):
    v0 = np.identity(A.shape[0])[0]
    l = 8
    for i in itertools.count(1):
        v = v0
        AuI = A-l*np.identity(A.shape[0])
        w = scipy.linalg.solve(AuI, v)
        v = w / np.linalg.norm(w)
        if np.linalg.norm(v-v0) < eps or np.linalg.norm(v+v0) < eps:
            return l, v, i
        l = v.T @ A @ v
        v0 = v

for name, func in {
    'tomekzaw_maxeig_v1': tomekzaw_maxeig_v1,
    'tomekzaw_maxeig_v2': tomekzaw_maxeig_v2,
    'tomekzaw_maxeig_v2_2': tomekzaw_maxeig_v2_2,
    'tomekzaw_maxeig_v3': tomekzaw_maxeig_v3
}.items():
    print('\n{}:'.format(name))
    maxeigval, maxeigvec, iters = func(A)
    print(maxeigval)
    print(maxeigvec)
    print('Number of iterations: {}'.format(iters))

"""
for n in range(2, 20):
    A = np.random.rand(n, n)
    _, _, iters = tomekzaw_maxeig_v3(A)
    print(iters)
"""