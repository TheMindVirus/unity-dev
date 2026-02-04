import math

def blas_fft(x):
    N = len(x)
    y = [0] * N
    tau = 2.0 * math.pi
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            K = complex(math.cos(jin), -math.sin(jin))
            y[i] += x[j] * K
    return y

def blas_ifft(y):
    N = len(y)
    x = [0] * N
    D = 1.0 / N
    tau = 2.0 * math.pi
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            K = complex(math.cos(jin), math.sin(jin))
            x[i] += y[j] * K * D
    return x