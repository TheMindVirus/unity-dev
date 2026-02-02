import math #, cmath
#import numpy as np
import time

def integrate(x):
    N = len(x)
    y = [0] * N
    y[0] = x[0]
    for i in range(1, N):
        y[i] = x[i - 1] + (0.5 * (x[i] - x[i - 1]))
    return y

def differentiate(y):
    N = len(y)
    x = [0] * N
    x[0] = y[0]
    for i in range(1, N):
        x[i] = (2.0 * y[i]) - x[i - 1]
    return x

def convolute(x):
    N = len(x)
    y = [0] * N
    tau = 2.0 * math.pi
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            #K = cmath.exp((0-1j * 2.0 * math.pi * j * i) / N)
            K = complex(math.cos(jin), math.sin(jin))
            y[i] += x[j] * K
    return y

def unwind(y):
    N = len(y)
    x = [0] * N
    D = (1.0 / N)
    tau = 2.0 * math.pi
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            #K = cmath.exp((0+1j * 2.0 * math.pi * j * i) / N)
            K = complex(math.cos(jin), -math.sin(jin))
            x[i] += y[j] * K * D
    return x

def main():
    T = []
    X = []
    Y = []
    
    N = 2047 #7 #2048
    for i in range(0, N + 1):
        X.append(complex(i, 0))

    T.append(time.monotonic())

    Y.append(X)
    #Y.append([])
    #Y.append(integrate(Y[0]))
    #Y.append(differentiate(Y[-1]))
    #Y.append([])
    #Y.append(differentiate(Y[0]))
    #Y.append(integrate(Y[-1]))
    #Y.append([])
    Y.append(convolute(Y[0]))
    Y.append(unwind(Y[-1]))
    #Y.append([])
    #Y.append(unwind(Y[0]))
    #Y.append(convolute(Y[-1]))
    #Y.append([])

    T[-1] = time.monotonic() - T[-1]

    if N < 10:
        for i in range(0, len(Y)):
            print(Y[i])
    else:
        for i in range(0, len(T)):
            print(T[i], "seconds")

if __name__ == "__main__":
    main()
