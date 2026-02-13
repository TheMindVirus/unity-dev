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
    p = float(i)
    if (i > n / 2):
        p = (n - i)
    y[idx] = x[j] * k1[idx]
    #y[idx] *= (pow(5.0, (-abs(pow(p - 0, 2.0)) / n)) * 1.0) + 0.0;
    z[idx] = y[idx] * k2[idx] * (1.0 / n)
print(z)

#for a in range(0, n2):
#    i = int(a / n)
#    j = int(a - (i * n))
#    idx = int((i * n) + j)
#    jdx = int((j * n) + i)
#    z[idx] = y[jdx] * k2[idx]
#print(z)

for a in range(0, n2):
    i = int(a / n)
    j = int(a - (i * n))
    idx = int((i * n) + j)
    jdx = int((j * n) + i)
    xx[i] += z[jdx]
print(xx)
#for a in range(0, n):
#    xx[a] /= n
print(xx)

