import cmath
import math

x = [0,1,2,3,4,5,6]
n = len(x)
n2 = n * n
D = 1.0 / n
k = [0] * n2
k2 = [0] * n2
tau = math.pi * 2

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        jin = -(j * i) / n
        jin *= (0+1j * tau)
        k[idx] = cmath.exp(jin)
print(k, end = "\n\n")

y = [0] * n
for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        K = k[idx]
        y[i] += x[j] * K
print(y, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        jin = ((j * i) / n) / (0+1j * tau)
        jin *= (0+1j * tau)
        jin *= (0+1j * tau)
        k[idx] = cmath.exp(jin)
print(k, end = "\n\n")

z = [0] * n
for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        K = k[idx]
        z[i] += y[j] * K * D
print(z, end = "\n\n")
