import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt

"""
f4 = lambda x, y: 1 / (np.sqrt(x + y) * (1 + x + y))
result, _ = scipy.integrate.dblquad(f4, 0, 1, lambda x: 0, lambda x: 1-x)
print(result)
"""

def tomekzaw_quad_trapezoid_2d(f, a, b, c, d, xs=100000, ys=100000):
    x = np.linspace(a, b, xs)
    y = np.linspace(c, d, ys)
    h, k = (b-a)/xs, (d-c)/ys
    return h*k/4 * (
        f(a,c) + f(b,c) + f(a,d) + f(b,d)
        + 2*sum(f(x[1:-1],c)) + 2*sum(f(x[1:-1],d))
        + 2*sum(f(a,y[1:-1])) + 2*sum(f(b,y[1:-1]))
        + 4*sum(sum(f(xx,y[1:-1])) for xx in x[1:-1])
    ) # http://mathfaculty.fullerton.edu/mathews/n2003/simpsons2Drule/SimpsonsRule2DMod/Images/SimpsonsRule2DMod_gr_16.gif

f5 = lambda x, y: x**2+y**2
for name, func in {
    "tomekzaw_quad_trapezoid_2d": tomekzaw_quad_trapezoid_2d,
    "scipy.integrate.dblquad": scipy.integrate.dblquad,
}.items():
    result = func(f5, -3, 3, -5, 5)
    print("{}:\t{}".format(name, result))

