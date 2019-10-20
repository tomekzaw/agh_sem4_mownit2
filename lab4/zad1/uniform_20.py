from zad1 import *

for n, modification, name, temp_base, max_iterations in [
    #(20, arbitrary_swap, 'arbitrary', 0.9995, 3e4),
    #(20, consecutive_swap, 'consecutive', 0.99995, 3e5),
    #(50, arbitrary_swap, 'arbitrary', 0.99998, 6e5),
    (100, arbitrary_swap, 'arbitrary', 0.999995, 2e6),
]:
    run(
        name='uniform_{}_{}'.format(n, name),
        nodes=generate_nodes_uniform(n),
        modification=modification,
        temperature=lambda i: temp_base**i,
        max_iterations=int(max_iterations),
        report=True
    )