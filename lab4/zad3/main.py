from zad3 import *
import sys

if len(sys.argv) < 2:
    print('Please specify path to sudoku file')
    raise SystemExit
solve(sys.argv[1])
