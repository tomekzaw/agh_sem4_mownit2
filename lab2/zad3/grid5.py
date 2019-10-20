import zad3
import networkx as nx
import matplotlib.pyplot as plt

n = 5
G = nx.DiGraph()
for u, v in nx.grid_2d_graph(n, n).edges():
    G.add_edge(u, v, R=1)

# pos = nx.shell_layout(G)
pos = {
    (i, j): [i, -j]
    for i in range(n)
    for j in range(n)
}

s, t = (0, 0), (n-1, n-1)
E = 10

zad3.solve(G, pos, s, t, E,
    edge_colormap=plt.cm.Blues,
    edge_arrow_size=12,
    draw_nodes=True,
    edge_width=1.5,
    node_size=20,
    draw_edge_labels=True,
    plot_filename='grid5.png'
)