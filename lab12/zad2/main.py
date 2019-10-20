import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt

def tomekzaw_quad_simpson(x, y):
    return (x[1]-x[0])/3 * (y[0] + 2*sum(y[::2]) + 4*sum(y[1::2]) + y[len(y)-1])

fns = {
    1: (lambda x: np.exp(-x**2)*(np.log(x))**2, 1e-9, 1),
    2: (lambda x: 1/(x**3-2*x-5), -6, 4),
    3: (lambda x: (x**5)*np.exp(-x)*np.sin(x), 0, 10),
}

fn, x0, xn = fns[2]
x = np.linspace(x0, xn, 100)
y = fn(x)

X = np.linspace(x0, xn, 10000)
Y = fn(X)

plt.plot(X, Y, color='green')
plt.scatter(x, y, s=3, color='red')
plt.show()

results = {
    "tomekzaw_quad_simpson": tomekzaw_quad_simpson(x, y),
    "scipy.integrate.quad": (scipy.integrate.quad(fn, x0, xn))[0]
}

for name, value in results.items():
    print("{}:\t{}".format(name, value))
