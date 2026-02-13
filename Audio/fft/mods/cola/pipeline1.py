import cmath, math

x = [0,1,2,3,4,5,6]
n = len(x)
n2 = n * n
y = [0] * n2
z = [0] * n2
k1 = [0] * n2
k2 = [0] * n2
xx = [0] * n

for a in range(0, n2):
    i = int(a / n)
    j = int(a - (i * n))
    idx = int((i * n) + j)
    k1[idx] = cmath.exp((0-1j * math.pi * 2 * j * i) / n)
    k2[idx] = pow(k1[idx], -1)

for a in range(0, n2):
    i = int(a / n)
    j = int(a - (i * n))
    idx = int((i * n) + j)
    y[idx] = x[j] * k1[idx]
print(y)

for a in range(0, n2):
    i = int(a / n)
    j = int(a - (i * n))
    idx = int((i * n) + j)
    z[i] += y[idx]
print(z)

for a in range(0, n2):
    i = int(a / n)
    j = int(a - (i * n))
    idx = int((i * n) + j)
    xx[i] += z[j] * k2[idx] * (1.0 / n)
print(xx)
