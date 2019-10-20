from zad1 import *

run(
    name='groups_3x3_50',
    nodes=generate_nodes_groups(50, 3),
    temperature=lambda i: 0.999995**i,
    max_iterations=int(3e6),
    report=True
)
