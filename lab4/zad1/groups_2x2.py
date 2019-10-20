from zad1 import *

run(
    name='groups_2x2_50',
    nodes=generate_nodes_groups(50, 2),
    temperature=lambda i: 0.99998**i,
    max_iterations=int(7e5),
    report=True
)

"""
run(
    name='groups_2x2_100',
    nodes=generate_nodes_groups(100, 2),
    temperature=lambda i: 0.99999**i,
    max_iterations=int(2e6),
    report=True
)
"""
