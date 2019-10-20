from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def visualize_svd(A, fig, pos=111, show_axes=True):    
    ax = fig.add_subplot(pos, projection='3d')
    ax.view_init(elev=30, azim=30)
    ax.set_aspect('equal')

    s = np.linspace(0, 2*np.pi, 50)
    t = np.linspace(0, np.pi, 50)

    X = np.outer(np.cos(s), np.sin(t))
    Y = np.outer(np.sin(s), np.sin(t))
    Z = np.outer(np.ones(np.size(s)), np.cos(t))

    for i in range(len(s)):
        for j in range(len(t)):
            X[i,j], Y[i,j], Z[i,j] = A @ np.array([X[i,j], Y[i,j], Z[i,j]])

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='plasma', edgecolor=None, alpha=0.7)
    #ax.plot_wireframe(X, Y, Z, edgecolor='black', linewidth=0.2)

    if show_axes:
        u, s, vh = np.linalg.svd(A)
        for s1 in np.diag(s):
            b = np.dot(u, s1) # było v
            ax.plot([0, b[0]], [0, b[1]], [0, b[2]], linewidth=2)

    # aspect ratio 1:1
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0
    mid_x = (X.max()+X.min()) * 0.5
    mid_y = (Y.max()+Y.min()) * 0.5
    mid_z = (Z.max()+Z.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

if __name__ == "__main__":

    #A = np.random.rand(3, 3)
    A = np.array([[7,0,0],[2,3,0],[0,0,4]])
    # print(A)
    u, sd, vh = np.linalg.svd(A)
    s = np.diag(sd)
    v = vh.T
    I = np.identity(3)
    
    for i, T in enumerate((I, v, s @ v, A), 1):
        fig = plt.figure()
        visualize_svd(T, fig, 111, i == 4)
        plt.show()
    #plt.savefig('main.png', dpi=1200)
