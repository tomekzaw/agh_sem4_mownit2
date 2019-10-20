import random
import itertools
import numpy
import scipy
import networkx as nx
import matplotlib.pyplot as plt

N = 10
"""
G = nx.DiGraph()
for u in range(n):
    for v in range(u+1, n):
        if random.random() < 0.8*u/n:
            G.add_edge(u, v)
"""
G = nx.gnc_graph(N)
A = nx.to_scipy_sparse_matrix(G, dtype=float)

Nu = scipy.sparse.linalg.norm(A, ord=0, axis=1)
Nu = (1 / Nu)
Nu[numpy.isinf(Nu)] = 0
A = A.T.multiply(Nu).T

print(A.todense())
eigvals, eigvecs = numpy.linalg.eig(A.todense())
print(eigvals)

plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G)
nx.draw_networkx_labels(G, pos)
nx.draw(G, pos)
plt.savefig('graph.png', bbox_inches='tight', dpi=300)
