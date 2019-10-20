import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
import itertools
import random
import math
import os
from copy import deepcopy   

def import_sudoku(path):
    with open(path) as file:  
        data = file.read()
    sudoku = [[None] * 9 for i in range(9)] 
    free = [[list() for i in range(3)] for j in range(3)]
    for i in range(9):
        for j in range(9):
            if not data:
                break
            while True:
                char, data = data[0], data[1:]
                if char in ['0', 'x', '.', '_']:
                    free[i//3][j//3].append((i, j))
                    break
                if char in map(str, range(1, 10)):
                    sudoku[i][j] = int(char)
                    break
    return sudoku, free

def print_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            print((str(sudoku[i][j]) if sudoku[i][j] else 'x') + ' ', end='')
            if j % 3 == 2:
                print('  ', end='')
        print('\n\n' if i % 3 == 2 else '\n', end='')
        
def draw_sudoku(sudoku, ax):
    ax.axis('off')
    ax.set_aspect('equal')
    ax.set_xlim([-1, 9])
    ax.set_ylim([1, -9])
    for i in range(9):
        for j in range(9):
            ax.text(j, i-8+0.05, sudoku[i][j], fontname='Helvetica', fontsize=5, horizontalalignment='center', verticalalignment='center')
    for i in range(10):
        linewidth = 0.5 if i % 3 == 0 else 0.2
        for (xs, ys) in [([-0.5, 8.5], [-i+0.5] * 2), ([i-0.5] * 2, [0.5, -8.5])]:
            ax.add_line(lines.Line2D(xs, ys, linewidth=linewidth, color='black', axes=ax))

def save_sudoku(*sudokus, path=None, dpi=600):
    fig = plt.figure(figsize=(len(sudokus), 1), dpi=dpi)
    for i, sudoku in enumerate(sudokus, 1):
        draw_sudoku(sudoku, fig.add_subplot(1, len(sudokus), i))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    if path is None:
        plt.show()
    else:
        plt.savefig(path)

def save_plot(values, path, dpi=600):
    fig = plt.figure(figsize=(6, 2))
    ax = fig.add_subplot(1, 1, 1)        
    ax.plot(values, linewidth=0.5, color='navy')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    plt.tight_layout()
    plt.savefig(path, dpi=dpi)

def fill_sudoku(sudoku, free):
    for iii in range(3):
        for jjj in range(3):
            found = list()
            for ii in range(3):
                for jj in range(3):
                    i, j = iii*3+ii, jjj*3+jj
                    if (i, j) not in free[iii][jjj]:
                        found.append(sudoku[i][j])
            not_found = [n for n in range(1, 9+1) if n not in found]
            random.shuffle(not_found)
            for (i, j), n in zip(free[iii][jjj], not_found):
                sudoku[i][j] = n
            if len(free[iii][jjj]) == 1:
                free[iii][jjj] = list()

def count_repetitions(list):
    occurrences = [-1] * 9
    for n in list:
        occurrences[n-1] += 1 # if n is not None:
    return sum(map(lambda r: 0 if r <= 0 else r, occurrences))

def sudoku_energy(sudoku):
    energy = 0
    for i in range(9):
        energy += count_repetitions([sudoku[i][j] for j in range(9)])
        energy += count_repetitions([sudoku[j][i] for j in range(9)])
    return energy

def generate_random_swap(free):
    while True:
        iii, jjj = random.randint(0, 2), random.randint(0, 2)
        if len(free[iii][jjj]) >= 2:
            return random.sample(free[iii][jjj], 2)

def sudoku_swap(sudoku, i1, j1, i2, j2):
    sudoku[i1][j1], sudoku[i2][j2] = sudoku[i2][j2], sudoku[i1][j1]
    
def metropolis(old_energy, new_energy, temp):
    try:
        return math.exp(-(new_energy - old_energy) / temp)
    except OverflowError:
        return 0.0

def solve(
    filename,
    temperature=lambda i: 0.9999**i,
    probability=metropolis
):
    name = os.path.basename(filename).split('.')[0]
    original, free = import_sudoku(filename)
    sudoku = deepcopy(original)
    fill_sudoku(sudoku, free)

    if not os.path.exists('results'):
        os.makedirs('results')

    old_energy = sudoku_energy(sudoku)
    energies = [old_energy]
    try:
        for iteration in itertools.count():
            temp = temperature(iteration)

            (i1, j1), (i2, j2) = generate_random_swap(free)
            sudoku_swap(sudoku, i1, j1, i2, j2)

            new_energy = sudoku_energy(sudoku)
            energies.append(new_energy)
            if new_energy == 0:
                print('Number of iterations: {}'.format(iteration))
                save_sudoku(original, sudoku, path='results/{}_sudoku.png'.format(name), dpi=1200)
                raise SystemExit

            prob = probability(old_energy, new_energy, temp)
            rand = random.uniform(0, 1)

            if new_energy < old_energy or rand < prob:
                old_energy = new_energy
            else:
                sudoku_swap(sudoku, i1, j1, i2, j2) # reverse swap

            print('{}\t{}\t{}\t{}'.format(iteration, new_energy, temp, prob))

    except KeyboardInterrupt:
        print('Interrupted')

    finally:
        save_plot(energies, path='results/{}_energy.png'.format(name))