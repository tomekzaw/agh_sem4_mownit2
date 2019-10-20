import zad3
import networkx as nx
import matplotlib.pyplot as plt

n = 20
G = nx.DiGraph()
for u, v in nx.grid_2d_graph(n, n).edges():
    G.add_edge(u, v, R=1)

# pos = nx.shell_layout(G)
pos = {
    (i, j): [i, -j]
    for i in range(n)
    for j in range(n)
}

s, t = (5, 5), (15, 15)
E = 10

zad3.solve(G, pos, s, t, E,
    edge_colormap=plt.cm.Blues,
    edge_arrow_size=10,
    draw_nodes=True,
    edge_width=1,
    node_size=2,
    draw_edge_labels=False,
    plot_filename='grid20.png'
)