from zad1 import *

run(
    name='circle_20',
    nodes=generate_nodes_circle(20),
    temperature=lambda i: 0.999**i,
    max_iterations=int(1e4),
    report=True
)
