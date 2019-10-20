import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import warnings
warnings.filterwarnings("ignore", category=mpl.cbook.mplDeprecation)

def solve(G, pos, s, t, E,
    draw_nodes=False,
    node_color='black',
    node_size=100,
    draw_node_labels=False,
    node_label_color='white',
    node_label_font_size=16,
    draw_edges=True,
    edge_width=2,
    edge_colormap=plt.cm.Wistia,
    edge_arrow_size=32,
    draw_edge_labels=False,
    edge_label_font_size=6,
    draw_colorbar=True,
    plot_filename=None,
    plot_dpi=600,
    I_eps=1e-8,
    U_eps=1e-8
):
    # define helper functions
    def pairs(cycle):
        return zip(cycle, cycle[1:] + [cycle[0]])

    # validate circuit
    if not nx.is_weakly_connected(G): # nx.is_connected(G.to_undirected())
        raise Exception('Circuit is not connected')

    # validate input data
    for x in s, t:
        if x not in G.nodes():
            raise Exception('Node {} does not exist'.format(x))

    if s == t:
        raise Exception('Cannot apply electromotive force to single node')

    # apply the electromotive force
    G.add_edge(s, t, R=0)

    # create matrix
    e = G.number_of_edges()
    M = np.zeros((e, e)) # todo: sparse matrix
    B = np.zeros(e)
    edgelist = list(G.edges()) # for column indexing

    # apply the Kirchhoff's second law for cycle basis
    cycles = nx.cycle_basis(G.to_undirected())
    for i, cycle in enumerate(cycles):
        for pair in pairs(cycle):
            if pair == (s, t):
                B[i] = E
            elif pair == (t, s):
                B[i] = -E
            else:
                (u, v) = pair
                if (u, v) in edgelist:
                    j = edgelist.index((u, v))
                    M[i][j] = G[u][v]['R']
                else: # (v, u) in edgelist
                    j = edgelist.index((v, u))
                    M[i][j] = -G[v][u]['R']

    # apply the Kirchhoff's first law for each node
    C = len(cycles)
    for i, x in enumerate(G.nodes()):
        if C+i == len(edgelist):
            break
        for (u, x) in G.in_edges(x):
            j = edgelist.index((u, x))
            M[C+i,j] = 1
        for (x, v) in G.out_edges(x):
            j = edgelist.index((x, v))
            M[C+i,j] = -1

    # check matrix
    if np.linalg.matrix_rank(M) != G.number_of_edges():
        raise Exception("Singular matrix")

    # solve linear system
    I = np.linalg.solve(M, B)
    I_max = max(I)

    # add currents to graph
    for i, (u, v) in enumerate(G.copy().edges()):
        if I[i] < 0:
            # reverse edge if current is negative
            R = G.edges[u, v]['R']
            G.remove_edge(u, v)
            G.add_edge(v, u, R=R)
            (u, v), I[i] = (v, u), -I[i]
        G.edges[u, v]['I'] = I[i]

    # verify the solution

    # verify the Kirchhoff's second law for cycle basis
    for x in G.nodes():
        I = 0
        for e in G.in_edges(x):
            I += G.edges[e]['I']
        for e in G.out_edges(x):
            I -= G.edges[e]['I']
        if I > I_eps * I_max:
            raise Exception("Verification failed for Kirchhoff's second law")
    
    # verify the Kirchhoff's first law for each node
    for i, cycle in enumerate(cycles):
        U = 0
        for pair in pairs(cycle):
            if pair == (s, t):
                U += E
            elif pair == (t, s):
                U -= E
            else:
                (u, v) = pair
                if (u, v) in G.edges():
                    U -= G.edges[u, v]['R'] * G.edges[u, v]['I']
                else: # (v, u) in G.edges()
                    U += G.edges[v, u]['R'] * G.edges[v, u]['I']
        if U > U_eps * E:
            raise Exception("Verification failed for Kirchhoff's first law")
    
    # draw graph
    if draw_nodes:
        nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=node_size)

    if draw_node_labels:
        nx.draw_networkx_labels(G, pos, font_color=node_label_color, font_size=node_label_font_size, font_weight='bold')

    if draw_edges:
        tmp = list(G.nodes)[0]
        colors = currents = [I for _, _, I in G.edges(data='I')]
        widths = [edge_width*I/I_max+edge_width for I in currents]
        nx.draw_networkx_edges(G, pos, width=widths, edge_color=colors, edge_cmap=edge_colormap, edge_vmin=-I_max/10, edge_vmax=I_max, arrowsize=edge_arrow_size, node_size=node_size)
    
    if draw_edge_labels:
        edge_labels = {e: '%.3g' % (i) if i > I_eps * I_max else '0' for e, i in nx.get_edge_attributes(G, 'I').items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=edge_label_font_size)
    
    if draw_colorbar:
        sm = plt.cm.ScalarMappable(cmap=edge_colormap, norm=plt.Normalize(vmin=0, vmax=I_max))
        sm._A = []
        plt.colorbar(sm, shrink=0.5, fraction=0.1)

    # generate plot
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    if plot_filename is None:
        plt.show()
    else:
        plt.savefig(plot_filename, dpi=plot_dpi)
