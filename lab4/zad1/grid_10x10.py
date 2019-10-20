from zad1 import *

run(
    name='grid_10x10',
    nodes=generate_nodes_grid(10),
    temperature=lambda i: 0.999997**i,
    max_iterations=int(3e6),
    report=True
)
