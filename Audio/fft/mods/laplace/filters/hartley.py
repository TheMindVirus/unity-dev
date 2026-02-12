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
        jin = (math.cos(j * i) + math.sin(j * i))
        k[idx] = jin / math.sqrt(tau)
print(k, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        y[idx] = x[j] * k[idx]
print(y, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        jin = (math.cos(j * i) + math.sin(j * i))
        k[idx] = pow(jin / math.sqrt(tau), -1)
print(k, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        z[idx] = y[j] * k[idx]
a = z[:n]
print(z, end = "\n\n")

print(a, end = "\n\n")
