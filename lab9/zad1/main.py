from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import itertools
import copy

def run(
    original_filename='chopin.jpg',
    image_transform=lambda img: PIL.ImageOps.invert(img.convert('L')),
    patterns=[
        ('chopin1.jpg', 0.9, (-200, 0, -200)),
    ],
    result_filename=None,
    highlight_rectangle=True
):
    img = Image.open(original_filename)
    pixels = img.load()
    pixels2 = img.copy().load()
    w, h = img.size
    original = np.swapaxes(np.array(image_transform(img)), 0, 1)

    original_dft = np.fft.fft2(original)

    x = np.linspace(0, w-1, w)
    y = np.linspace(0, h-1, h)
    X, Y = np.meshgrid(x, y)
    Z = np.swapaxes(np.angle(original_dft), 0, 1)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    #ax.set_zlim(0, 3000000) # only for np.abs    
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    plt.savefig('angle.png', dpi=300)

    for pattern_filename, with_rotations, threshold, (dr, dg, db) in patterns:
        imp = Image.open(pattern_filename)
        for i in range(4 if with_rotations else 1):
            pw, ph = imp.size
            pattern = np.swapaxes(np.array(image_transform(imp)), 0, 1)

            C = np.real(
                np.fft.ifft2(
                    np.multiply(
                        original_dft,
                        np.fft.fft2(np.rot90(pattern, 2), s=(w, h))
                    )
                )
            )
            C_min, C_max = np.min(C), np.max(C)
            C_threshold = threshold * (C_max - C_min) + C_min

            for x, y in np.argwhere(C >= C_threshold):
                x, y = int(x), int(y)
                if highlight_rectangle:
                    for dx in range(pw):
                        for dy in range(ph):
                            r, g, b = pixels2[x-dx,y-dy]
                            pixels[x-dx,y-dy] = (r+dr, g+dg, b+db)
                else:
                    x0,y0 = x-pw//2, y-ph//2
                    r, g, b = pixels2[x0,y0]
                    pixels[x0,y0] = (r+dr, g+dg, b+db)

            imp = imp.transpose(Image.ROTATE_90)

    if result_filename is None:
        img.show()
    else:
        img.save(result_filename)

if __name__ == "__main__":
    """
    run(
        original_filename='galia.png',
        image_transform=lambda img: ImageOps.invert(img.convert('L')),
        patterns=[
            ('galia1.png', False, 0.9, (-100, -50, +100)),
        ],
        result_filename='results/galia.png',
        highlight_rectangle=True
    )
    """
    run(
        original_filename='chopin.jpg',
        image_transform=lambda img: ImageOps.invert(img.convert('L')),
        patterns=[
            ('chopin1.jpg', False, 0.91, (-200, 0, -200)),
        ],
        result_filename='results/chopin.jpg',
        highlight_rectangle=True
    )
    """
    run(
        original_filename='circuit.jpg',
        image_transform=lambda img: img.convert('L'),
        patterns=[('circuit{}.jpg'.format(i+1), True, 0.94, (-100, -50, 0)) for i in range(7)],
        result_filename='results/circuit.jpg',
        highlight_rectangle=True
    )
    """
    run(
        original_filename='fish.jpg',
        image_transform=lambda img: np.array(img)[:,:,0],
        patterns=[
            ('fish1.png', False, 0.14, (+255, -100, -100))
        ],
        result_filename='results/fish.jpg',
        highlight_rectangle=False
    )
    """
    run(
        original_filename='fish.jpg',
        image_transform=lambda img: np.abs(np.array(ImageOps.invert(img.convert('L')))-120),
        patterns=[
            ('fish1.png', False, 0.6, (+255, -100, -100))
        ],
        result_filename='results/fish_L.png',
        highlight_rectangle=False
    )
    
    for threshold in itertools.chain(range(5, 20), range(20, 50, 5), range(50, 100, 10)):
        run(
            original_filename='fish.jpg',
            image_transform=lambda img: np.array(img)[:,:,0],
            patterns=[
                ('fish1.png', False, threshold / 100.0, (+255, -100, -100))
            ],
            result_filename='results/fish_R_{}%.png'.format(threshold),
            highlight_rectangle=False
        )
    """