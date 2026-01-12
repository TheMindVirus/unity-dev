X = [ -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6 ]

print("BEGIN PYFFT")

pi = 3.141592653589793
e = 2.718281828459045

def pft(x):
    N = len(x)
    y = [0] * N
    for i in range(0, N):
        for k in range(0, N):
            y[i] += x[k] * pow(e, (0-1j * 2 * pi * k * i) / N)
    return y

def ipft(y):
    N = len(y)
    x = [0] * N
    for i in range(0, N):
        for k in range(0, N):
            x[i] += y[k] * pow(e, (0+1j * 2 * pi * k * i) / N) * (1 / N)
    for i in range(0, N):
        x[i] = round(x[i].real)
    return x

Z = pft(X)
print(Z)

Y = ipft(Z)
print(Y)

print("BEGIN CMATH")

import math, cmath

def cft(x):
    N = len(x)
    y = [0] * N
    for i in range(0, N):
        for j in range(0, N):
            y[i] += x[j] * cmath.exp((-cmath.sqrt(-1) * 2 * math.pi * j * i) / N)
    return y

def icft(y):
    N = len(y)
    x = [0] * N
    for i in range(0, N):
        for j in range(0, N):
            x[i] += y[j] * cmath.exp((cmath.sqrt(-1) * 2 * math.pi * j * i) / N) * (1 / N)
    for i in range(0, N):
        x[i] = round(x[i].real)
    return x
        
Z = cft(X)
print(Z)

Y = icft(Z)
print(Y)

print("BEGIN NUMPY")

import numpy as np

Z = np.fft.fft(X)
print(Z)

Y = np.fft.ifft(Z)
Y = [round(i.real) for i in Y]
print(Y)
