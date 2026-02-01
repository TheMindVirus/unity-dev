import concurrent.futures
import time
import math

print("loading")

N = 100 #2048
T = N * N
F = [0] * T
R = [0] * N

X = []
for i in range(0, N):
    X.append([])
    for j in range(0, N):
        X[i].append(0.0)
for i in range(0, N):
    for j in range(0, N):
        p = 2.0 * math.pi * j * i
        X[j][i] = complex(math.cos(p / N),
                         -math.sin(p / N))
x = X[0].copy()

print("start")

t = time.monotonic()

def worker(i, j, x, X):
    return x[j] * X[j][i]

with concurrent.futures.ThreadPoolExecutor(max_workers = N) as executor:
    for i in range(0, N):
        for j in range(0, N):
            F[j] = executor.submit(worker, i, j, x, X)
    for i in range(0, N):
        for j in range(0, N):
            R[i] += F[j].result()

t = time.monotonic() - t

print(t)

R = [0] * N

t = time.monotonic()

for i in range(0, N):
    for j in range(0, N):
        R[i] += x[j] * X[j][i]

t = time.monotonic() - t

print(t)
