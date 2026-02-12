import cmath
import math

x = [0,1,2,3,4,5,6]
n = len(x)
n2 = n * n
k = [0] * n2
y = [0] * n2
z = [0] * n2
a = [0] * n
tau = math.pi * 2

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        jin = (0-1j * tau * j * i) / n
        k[idx] = cmath.exp(jin)
print(k, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        y[idx] = x[j] * k[idx]
print(y, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        jin = (0+1j * tau * j * i) / n
        k[idx] = cmath.exp(jin)
print(k, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        z[idx] = y[idx] * k[idx]
for i in range(0, n):
    for j in range(0, n):
        jdx = (j * n) + i
        a[i] += z[jdx]
    a[i] /= n
print(z, end = "\n\n")

print(a, end = "\n\n")


