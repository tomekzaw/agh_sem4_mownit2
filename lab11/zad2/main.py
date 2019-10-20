import numpy
import matplotlib.pyplot as plt

def tomekzaw_lstsq(A, b):
    Q, R = numpy.linalg.qr(A)
    return numpy.linalg.solve(R, Q.T @ b)

points = [
    (-5, 2),
    (-4, 7),
    (-3, 9),
    (-2, 12),
    (-1, 13),
    (0, 14),
    (1, 14),
    (2, 13),
    (3, 10),
    (4, 8),
    (5, 4),
]

A = numpy.array([[1, x, x*x] for x, _ in points])
b = numpy.array([y for _, y in points])

# x, _, _, _ = numpy.linalg.lstsq(A, b, rcond=None)
x = tomekzaw_lstsq(A, b)

a0, a1, a2 = x
print('f(x) = {:.2f} + {:.2f}x + {:.2f}x²'.format(a0, a1, a2))
f = lambda x: a0 + a1*x + a2*x*x

xs, ys = zip(*points)
plt.scatter(xs, ys)
linspace = numpy.linspace(min(xs), max(xs), 100)
plt.plot(linspace, f(linspace))
plt.show()
