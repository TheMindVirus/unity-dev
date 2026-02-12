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
        try:
            jin = 1.0 / (j * i)
        except:
            jin = 0.0
        k[idx] = jin / tau
print(k, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        y[idx] = x[j] * k[idx]
print(y, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        try:
            jin = 1.0 / (j * i)
        except:
            jin = 0.0
        try:
            k[idx] = pow(jin / tau, -1)
        except:
            k[idx] = float("nan")
print(k, end = "\n\n")

for i in range(0, n):
    for j in range(0, n):
        idx = (i * n) + j
        z[idx] = y[idx] * k[idx]
for i in range(0, n):
    c = n
    for j in range(0, n):
        jdx = (j * n) + i
        if math.isnan(z[jdx]):
            a[i] += 0.0
            c -= 1
        else:
            a[i] += z[jdx]
    try:
        a[i] /= c
    except:
        a[i] = 0.0
print(z, end = "\n\n")

print(a, end = "\n\n")
