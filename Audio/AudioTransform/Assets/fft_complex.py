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

print("BEGIN PYFZT")

def fzt(x):
    N = len(x)
    y = [0] * N
    for i in range(0, N):
        y[i] = x[i]
        for j in range(0, N):
            y[i] += ((j * i) / N)
    return y

def ifzt(y):
    N = len(y)
    x = [0] * N
    for i in range(0, N):
        x[i] = y[i]
        for j in range(0, N):
            x[i] -= ((j * i) / N)
    for i in range(0, N):
        x[i] = round(x[i])
    return x

Z = fzt(X)
print(Z)

Y = ifzt(Z)
print(Y)

print("BEGIN PYDMF")

import math

def cadd(x, y):
    return [x[0] + y[0], x[1] + y[1]]

def cmul(x, y):
    return [(x[0] * y[0]) - (x[1] * y[1]), ((x[0] * y[1]) + (x[1] * y[0]))]

def cpow(x):
    return [math.cos(x), math.sin(x)]

def cneg(x):
    return [x[0], -x[1]]

def dmf(x):
    N = len(x)
    y = [[0, 0]] * N
    for i in range(0, N):
        for j in range(0, N):
            y[i] = cadd(y[i], cmul([x[j], 0], cneg(cpow((2 * math.pi * j * i) / N))))
    return y

def idmf(y):
    N = len(y)
    x = [[0, 0]] * N
    for i in range(0, N):
        for j in range(0, N):
            x[i] = cadd(x[i], cmul([(1 / N), 0], cmul(y[j], cpow((2 * math.pi * j * i) / N))))
    for i in range(0, N):
        x[i] = round(x[i][0])
    return x

Z = dmf(X)
print(Z)

Y = idmf(Z)
print(Y)
