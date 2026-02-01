import scipy.integrate as integrate
import numpy as np
import math, cmath
import sympy

print("BEGIN_SCIPY")

X = [0, 1, 2, 3, 4, 5, 6]
Y = [0, 0, 0, 0, 0, 0, 0]
Z = [0, 0, 0, 0, 0, 0, 0]
N = len(X)

def f_real_fwd(t, u, n, e):
    t = int(t) % n
    return e[t] * cmath.exp((0+1j * -2.0 * math.pi * u * t)).real

def f_imag_fwd(t, u, n, e):
    t = int(t) % n
    return e[t] * cmath.exp((0+1j * -2.0 * math.pi * u * t)).imag

def f_real_inv(t, u, n, e):
    t = int(t) % n
    return e[t] * cmath.exp((0+1j * 2.0 * math.pi * u * t)).real

def f_imag_inv(t, u, n, e):
    t = int(t) % n
    return e[t] * cmath.exp((0+1j * 2.0 * math.pi * u * t)).imag

for i in range(0, N):
    real = integrate.quad(f_real_fwd, -np.inf, np.inf, args = (i, N, X))[0]
    imag = integrate.quad(f_imag_fwd, -np.inf, np.inf, args = (i, N, X))[0]
    Y[i] = complex(real, imag)

#for i in range(0, N):
#    real = integrate.quad(f_real_inv, -np.inf, np.inf, args = (i, N, Y))[0]
#    imag = integrate.quad(f_imag_inv, -np.inf, np.inf, args = (i, N, Y))[0]
#    Z[i] = complex(real, imag)

print(X)
print(Y)
print(Z)

print("BEGIN_SYMPY")

X = [0, 1, 2, 3, 4, 5, 6]
Y = [0, 0, 0, 0, 0, 0, 0]
Z = [0, 0, 0, 0, 0, 0, 0]
N = len(X)

oo = np.inf

for i in range(0, N):
    x, i, u, t = sympy.symbols("x i u t")
    expr = sympy.Integral(sympy.exp(-2 * sympy.pi * i * u * t), (t, -oo, oo))
    print(expr)
    print(expr.doit())

print(X)
print(Y)
print(Z)
