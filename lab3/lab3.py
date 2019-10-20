#from mpmath import *
from decimal import *
from math import sin, sinh, cos, cosh, tan, pow, exp, log, pi
from numpy import sign

def bisection(f, a, b, eps):
    i = 0
    while True:
        i += 1
        c = a + (b-a)/2
        (fa, fb, fc) = (f(a), f(b), f(c))
        if abs(fc) < eps or sign(fa) == sign(fb):
            return (c, i)
        if sign(fc) == sign(fa):
            a = c
        else: 
            b = c

def newton(f, df_dx, x, eps, imax):
    i = 0
    while True:
        fx = f(x)
        dfx = df_dx(x)
        if (abs(fx) < eps or i > imax or dfx == 0):
            return (x, i)
        i += 1
        x = x - fx / dfx

def secant(f, a, b, eps, imax):
    i = 0
    while True:
        c = (f(b)*a - f(a)*b) / (f(b)-f(a))
        if (abs(f(c)) < eps or i > imax):
            return (c, i)            
        (a, b) = (b, c)
        i += 1

if __name__ == '__main__':
    getcontext().prec = 100
    fs = [
        (lambda x: cos(x)*cosh(x)-1, lambda x: -cosh(x)*sin(x) + cos(x)*sinh(x)),
        #(lambda x: 1/x-tan(x), lambda x: -1/pow(x, 2) - 1/pow(cos(x), 2)),
        #(lambda x: pow(2,-x)+exp(x)+2*cos(x)-6, lambda x: exp(x) - pow(2, -x)*log(2) - 2*sin(x)),
    ]
    ranges = [
        (3*pi/2, 2*pi),
        (0, pi/2),
        (1, 3),
    ]

    for ((f, _), (a, b)) in zip(fs, ranges):
        print(bisection(f, a, b, 1e-13))

    for ((f, dfdx), (a, _)) in zip(fs, ranges):
        print(newton(f, dfdx, b, 1e-13, 1e10))

    for ((f, _), (a, b)) in zip(fs, ranges):
        print(secant(f, a, b, 1e-13, 1e10))