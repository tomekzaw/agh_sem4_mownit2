import zad3
import random
import networkx as nx
import matplotlib.pyplot as plt

n = 10
G = nx.DiGraph()
for u in range(n):
    for v in range(u, n):
        if random.random() < 0.2:
            R = random.randint(0, 10)
            G.add_edge(u, v, R=R)
pos = nx.shell_layout(G)
s, t = 0, 1
E = 100

zad3.solve(G, pos, s, t, E,
    edge_colormap=plt.cm.Wistia,
    draw_nodes=True,
    draw_node_labels=True,
    node_size=400,
    node_label_font_size=12,
    draw_edge_labels=True,
    edge_arrow_size=20,
    edge_label_font_size=10,
    plot_filename='random1.png',
)