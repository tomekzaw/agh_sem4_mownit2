import zad3
import networkx as nx
import matplotlib.pyplot as plt

edges = [
    (1, 10, 1),
    (2, 20, 1),
    (3, 30, 1),
    (4, 40, 1),
    (5, 50, 1),
    (10, 20, 1),
    (20, 30, 1),
    (30, 40, 1),
    (40, 50, 1),
    (50, 10, 1),
    (1, 3, 1),
    (3, 5, 1),
    (5, 2, 1),
    (2, 4, 1),
    (4, 1, 1)
]
pos = {
    1: [0, 1],
    2: [3, -2],
    3: [2, -6],
    4: [-2, -6],
    5: [-3, -2],
    10: [0, 5],
    20: [6, 0],
    30: [4, -10],
    40: [-4, -10],
    50: [-6, 0]
}    
s, t = 10, 2
E = 80

# construct graph representing electric circuit
G = nx.DiGraph()
for (u, v, R) in edges:
    G.add_edge(u, v, R=R)

zad3.solve(G, pos, s, t, E,
    edge_colormap=plt.cm.Reds,
    draw_nodes=True,
    draw_node_labels=True,
    node_size=400,
    node_label_font_size=13,
    draw_edge_labels=True,
    edge_arrow_size=20,
    edge_label_font_size=10,
    plot_filename='petersen.png',
)