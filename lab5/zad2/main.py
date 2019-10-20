import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys

fname = 'lenna.bmp'
image = Image.open(fname).convert('L')
A = np.asarray(image)
u, s, v = np.linalg.svd(A)
B = np.zeros(A.shape)
fig = plt.figure()
for k in range(min(A.shape[0], A.shape[1])):
    B += s[k] * np.outer(u.T[k], v[k])
    print(np.linalg.norm(B-A))
    for i, kk in enumerate(range(24), 1):
        if k == kk:
            sys.stderr.write('{}\n'.format(k))
            ax = fig.add_subplot(4, 6, i)
            ax.set_title(k, fontsize=8)
            ax.axis('off')
            ax.imshow(B, cmap='gray', vmin=0, vmax=255)
plt.savefig('lennas.png', dpi=600)
