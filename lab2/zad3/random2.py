import zad3
import random
import networkx as nx
import matplotlib.pyplot as plt

n = 10
G1 = nx.DiGraph()
G2 = nx.DiGraph()
for u in range(n):
    for v in range(u, n):
        R = random.randint(0, 10)
        if random.random() < 0.4:
            G1.add_edge(u, v, R=R)
        if random.random() < 0.4:
            G2.add_edge(u+n, v+n, R=R)

pos1 = nx.shell_layout(G1)
pos2 = nx.shell_layout(G2)

G = nx.compose(G1, G2)
G.add_edge(0, n, R=1)

pos2_new = {k: [xy[0]+2, xy[1]+2] for k, xy in pos2.items()}
pos = {**pos1, **pos2_new} # join dicts

s, t = 1, n+1
E = 100

zad3.solve(G, pos, s, t, E,
    edge_colormap=plt.cm.Greens,
    draw_nodes=True,
    draw_node_labels=False,
    node_size=16,
    edge_width=1.5,
    edge_arrow_size=16,
    draw_edge_labels=True,
    edge_label_font_size=6,
    plot_filename='random2.png',
)