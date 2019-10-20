import numpy as np
import zad1
import math
import sys
from timeit import default_timer as timer
from random import shuffle

def measure_time(func):
    start = timer()
    result = func()
    end = timer()
    return result, end-start

ns = [int(pow(2, i/20.)) for i in range(20*2, 20*12+1)]
#shuffle(ns)
for n in ns:
    print('{}'.format(n), file=sys.stderr)

    # generate random matrix
    Ab = np.random.random(size=(n, n+1))

    # solve linear system using implemented algorithm
    x1, t1 = measure_time(lambda: zad1.solve_gauss_jordan(Ab))

    # solve linear system using library function
    x2, t2 = measure_time(lambda: np.linalg.solve(*zad1.split(Ab)))

    # calculate error
    err = math.sqrt(sum(map(lambda x: x**2, x1-x2))) # or: err = max(abs(x1-x2))

    # print results
    """
    print("n = {}".format(n))
    print("zad1.solve_gauss_jordan: {0:.2f} s".format(t1))
    print("np.linalg.solve: {0:.2f} s".format(t2))
    print("err = {0:.3g}".format(err))
    """
    print(' '.join(map(str, (n, t1, t2, err))))