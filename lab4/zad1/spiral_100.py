from zad1 import *

run(
    name='spiral_100',
    nodes=generate_nodes_spiral(100, 3),
    temperature=lambda i: 0.99995**i,
    max_iterations=int(3e5),
    report=True
)
