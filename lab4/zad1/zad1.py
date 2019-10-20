from __future__ import print_function
import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import random
import math
import sys
import os
import warnings
warnings.filterwarnings('ignore', category=mpl.cbook.mplDeprecation)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def generate_nodes_uniform(n):
    return [(random.random(), random.random()) for i in range(n)]

def generate_nodes_groups(n, groups):
    def random_pos():
        return random.randint(1, groups) + random.random() / 3
    return [(random_pos(), random_pos()) for i in range(n)]

def generate_nodes_grid(n):
    nodes = [(i, j) for i in range(n) for j in range(n)]
    random.shuffle(nodes)
    return nodes

def generate_nodes_circle(n):
    nodes = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]
    random.shuffle(nodes)
    return nodes

def generate_nodes_spiral(n, k):
    rot = float(n) / k
    nodes = [(math.sqrt(i) * math.cos(2 * math.pi * i / rot), math.sqrt(i) * math.sin(2 * math.pi * i / rot)) for i in range(n)]
    random.shuffle(nodes)
    return nodes

def generate_path(nodes):    
    return list(map(lambda i: nodes[i], range(len(nodes))))

def pairs(list):
    return zip(list, list[1:])

def distance(a, b):
    ax, ay = a
    bx, by = b
    return math.sqrt((ax-bx)**2+(ay-by)**2)

def cost(path):
    return sum(map(lambda two: distance(*two), pairs(path)))

def arbitrary_swap(old):
    new = old.copy()
    i1, i2 = random.sample(range(len(new)), 2)
    new[i1], new[i2] = new[i2], new[i1]
    return new

def consecutive_swap(old):
    new = old.copy()
    i1 = random.randint(0, len(new)-1)    
    i2 = (i1+1) % len(new)
    new[i1], new[i2] = new[i2], new[i1]
    return new

def metropolis(old_energy, new_energy, temp):
    try:
        return math.exp(-(old_energy - new_energy) / temp)
    except OverflowError:
        return 0.0

def simulated_annealing(old_state, energy, modification, temperature, probability, max_iterations, report=False):
    temperatures = list()
    energies = list()
    if report:
        report_every = max_iterations / 100

    old_energy = energy(old_state)
    best_energy = old_energy
    for iteration in range(max_iterations):
        if report and iteration % report_every == 0:
            eprint('{:.0f}% ({}/{})'.format(iteration * 100.0 / max_iterations, iteration, max_iterations))

        temp = temperature(iteration)
        temperatures.append(temp)
        energies.append(old_energy)
        new_state = modification(old_state)
        new_energy = energy(new_state)
        prob = probability(old_energy, new_energy, temp)
        rand = random.uniform(0, 1)
        if (new_energy > best_energy and rand < prob) or (new_energy < old_energy and rand > prob):
            old_state = new_state
            best_energy = min(best_energy, new_energy)
            old_energy = new_energy

    return old_state, temperatures, energies

def draw_path(path, ax, cmap=plt.cm.winter, title=None):
    ax.set_title(title, fontsize=9)
    ax.axis('off')

    G = nx.Graph()
    for i, edge in enumerate(pairs(list(path))):
        G.add_edge(*edge, order=i)

    pos = {(x, y): [x, y] for (x, y) in path}
    edge_color = [order for _, _, order in G.edges(data='order')]

    nx.draw_networkx_nodes(G, pos, node_size=5, node_color='black', cmap=cmap)
    nx.draw_networkx_edges(G, pos, width=1, edge_color=edge_color, edge_cmap=cmap)

def draw_plot(values, ax, title=None, width=0.5, color='navy'):
    ax.set_title(title, fontsize=9)
    ax.tick_params(labelsize=7)
    ax.grid(color='lightgray')
    ax.plot(values, linewidth=width, color=color)

def run(
    name='example',
    nodes=generate_nodes_uniform(50),
    temperature=lambda i: 0.999**i,
    max_iterations=int(4e4),
    energy=cost,
    modification=arbitrary_swap,
    probability=metropolis,
    report=True,
):
    path_before = generate_path(nodes)
    path_after, temperatures, energies = simulated_annealing(
        path_before,
        energy=energy,
        modification=modification,
        temperature=temperature,
        probability=probability,
        max_iterations=max_iterations,
        report=report
    )
    energy_before, energy_after = energies[0], energies[-1]

    if report:
        print('Before: {:.3f}\nAfter: {:.3f}'.format(energy_before, energy_after))

    fig = plt.figure(figsize=(7, 6), dpi=300)
    fig.tight_layout()

    draw_path(path_before, fig.add_subplot(2, 2, 1), title='Before')
    draw_path(path_after, fig.add_subplot(2, 2, 2), title='After')
    draw_plot(temperatures, fig.add_subplot(2, 2, 3), title='Temperature', width=1, color='navy')
    draw_plot(energies, fig.add_subplot(2, 2, 4), title='Energy', width=0.5, color='navy')

    if not os.path.exists('results'):
        os.makedirs('results')
    plt.savefig('results/{}.png'.format(name), bbox_inches='tight')