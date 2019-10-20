from __future__ import print_function
from PIL import Image
import matplotlib.pyplot as plt
import random
import math
import sys
import os

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def imgify(bitmap, scale=1.0):
    width, height = size(bitmap)
    img = Image.new('RGB', (width, height), 'white')
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            pixels[x,y] = (0, 0, 0) if bitmap[x][y] else (255, 255, 255)
    if scale != 1:
        img = img.resize((int(width * scale), int(height * scale)))
    return img

def show(bitmap, scale=1.0):
    imgify(bitmap, scale=scale).show()

def save(bitmap, path, scale=1.0):
    imgify(bitmap, scale=scale).save(path)

def generate(width, height, density):
    return [[random.random() < density for y in range(height)] for x in range(width)]

def size(bitmap):
    return len(bitmap), len(bitmap[0]) # width, height

def generate_arbitrary_swap(bitmap):
    width, height = size(bitmap)
    def random_point():
        return (random.randrange(width), random.randrange(height))
    while True:
        (x1, y1), (x2, y2) = random_point(), random_point()
        if bitmap[x1][y1] != bitmap[x2][y2]:
            return (x1, y1), (x2, y2)
    
def apply_swap(bitmap, swap):
    (x1, y1), (x2, y2) = swap
    bitmap[x1][y1], bitmap[x2][y2] = bitmap[x2][y2], bitmap[x1][y1]
    
def metropolis(delta, temp):
    try:
        return math.exp(delta / temp)
    except OverflowError:
        return 0.0

def calculate_bitmap_energy(bitmap, neighbourhood):
    width, height = size(bitmap)
    return sum([
        sum([
            weight if bitmap[(x+dx)%width][(y+dy)%height] else 0
            for (dx, dy), weight in neighbourhood.items()
        ]) if bitmap[x][y] else 0
        for x in range(width)
        for y in range(height)
    ])

def calculate_point_energy(bitmap, neighbourhood, point):
    x, y = point
    if bitmap[x][y] == 0:
        return 0
    width, height = size(bitmap)
    return sum([
        weight if bitmap[(x-dx)%width][(y-dy)%height] else 0
        for (dx, dy), weight in neighbourhood.items()
    ]) + sum([
        weight if bitmap[(x+dx)%width][(y+dy)%height] else 0
        for (dx, dy), weight in neighbourhood.items()
    ])

def modify(bitmap, neighbourhood, swap):
    delta = 0
    p1, p2 = swap
    delta -= calculate_point_energy(bitmap, neighbourhood, p1) + calculate_point_energy(bitmap, neighbourhood, p2)
    apply_swap(bitmap, swap)
    delta += calculate_point_energy(bitmap, neighbourhood, p1) + calculate_point_energy(bitmap, neighbourhood, p2)
    return delta

def save_plot(values, path, dpi=600, width=1):
    fig = plt.figure(figsize=(7,4))
    ax = fig.add_subplot(1, 1, 1)      
    ax.plot(values, linewidth=width, color='navy')
    plt.tight_layout()
    plt.savefig(path, dpi=dpi)

def run(
    name='example',
    width=100,
    height=100,
    density=0.4,    
    neighbourhood={
        (-1, -1): -1, (0, -1): -1, (1, -1): -1, (1, 0): -1,
        (1, 1): -1, (0, 1): -1, (-1, 1): -1, (-1, 0): -1
    },
    max_iterations=int(5e4),
    temperature=lambda i: 0.9995**i,
    probability=metropolis,
    scale=5.0,
    report_every=int(1e4),
    verify_every=int(5e5),
):
    if not os.path.exists('results'):
        os.makedirs('results')

    bitmap = generate(width, height, density)
    save(bitmap, 'results/{}_before.png'.format(name), scale=scale)

    energy = calculate_bitmap_energy(bitmap, neighbourhood)
    energies = list()
    temperatures = list()
    try:
        for iteration in range(max_iterations):
            temp = temperature(iteration)
            temperatures.append(temp)
            energies.append(energy)

            if iteration % report_every == 0:
                eprint('{:.0f}% ({}/{})'.format(iteration * 100.0 / max_iterations, iteration, max_iterations))
            if iteration % verify_every == 0:
                if energy != calculate_bitmap_energy(bitmap, neighbourhood):
                    print('Error in local energy function')
                    raise SystemExit

            swap = generate_arbitrary_swap(bitmap)
            delta = modify(bitmap, neighbourhood, swap)
            if delta < 0:  
                energy += delta
            else:
                prob = probability(delta, temp)
                rand = random.random()            
                if rand < prob:
                    energy += delta
                else:
                    apply_swap(bitmap, swap) # reverse swap
        print('100%')
    finally:
        save(bitmap, 'results/{}_after.png'.format(name), scale=scale)
        save_plot(energies, 'results/{}_energy.png'.format(name))
        save_plot(temperatures, 'results/{}_temperature.png'.format(name))