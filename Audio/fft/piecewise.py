X = [0.0+0.0j, 1.0+1.0j, 2.0+2.0j, 3.0+3.0j, 4.0+4.0j, 5.0+5.0j, 6.0+6.0j]
Y = [0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j]
Z = [0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j]
A = [0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j]
B = [0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j]
C = [0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j]
D = [0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j]
E = [0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j]
F = [0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j, 0.0+0.0j]
N = len(X)

#################################################

Y[0] = X[0]
for i in range(1, N):
    Y[i] = X[i - 1] + (0.5 * (X[i] - X[i - 1]))

Z[0] = Y[0]
for i in range(1, N):
    Z[i] = 0.5 * ((4.0 * Y[i]) - (2.0 * Z[i - 1]))

A[0] = X[0]
for i in range(1, N):
    A[i] = 0.5 * ((4.0 * X[i]) - (2.0 * A[i - 1]))

B[0] = A[0]
for i in range(1, N):
    B[i] = A[i - 1] + (0.5 * (A[i] - A[i - 1]))

#################################################

import math, cmath

x = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

for t in range(0, N):
    for u in range(0, N):
        x[t] = cmath.exp((0-1j * 2.0 * math.pi * u * t))

for t in range(0, N):
    for u in range(0, N):
        y[t] = cmath.exp((0+1j * 2.0 * math.pi * u * t))
"""
z = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
iz = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

for t in range(0, N):
    for u in range(0, N):
        ztr = math.cos((2.0 * math.pi * u * t) / N)
        zti = -math.sin((2.0 * math.pi * u * t) / N)
        z[t] = complex(ztr, zti)

for t in range(0, N):
    for u in range(0, N):
        ztr = math.cos((2.0 * math.pi * u * t) / N)
        zti = -math.sin((2.0 * math.pi * u * t) / N)
        iz[t] = complex((ztr - zti) * (1 / N), (ztr + zti) * (1 / N))
"""
#z = [0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j]
#___magic = 0.0-0.5j #pow(0.0+2.0j, -1)
#iz = [___magic, ___magic, ___magic, ___magic, ___magic, ___magic, ___magic]

#z = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
#iz = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

#z = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
#iz = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

#################################################

c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
d = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
e = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
f = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

cr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
ci = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
dr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
di = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
er = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
ei = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fi = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

for i in range(0, N):
    c[i] = X[i] * x[i]
C[0] = c[0]
for i in range(1, N):
    #C[i] = c[i - 1] + (0.5 * (c[i] - c[i - 1]))
    cr[i] = c[i - 1].real + (0.5 * (c[i].real - c[i - 1].real))
    ci[i] = c[i - 1].imag + (0.5 * (c[i].imag - c[i - 1].imag))
    C[i] = complex(cr[i], ci[i])

"""
for i in range(0, N):
    d[i] = C[i] * y[i]
D[0] = d[0]
for i in range(1, N):
    #D[i] = d[i - 1] + (0.5 * (d[i] - d[i - 1]))
    dr[i] = d[i - 1].real + (0.5 * (d[i].real - d[i - 1].real))
    di[i] = d[i - 1].imag + (0.5 * (d[i].imag - d[i - 1].imag))
    D[i] = complex(dr[i], di[i])
"""

#"""
for i in range(0, N):
    d[i] = C[i]
D[0] = d[0]
for i in range(1, N):
    #D[i] = 0.5 * ((4.0 * d[i]) - (2.0 * D[i - 1]))
    dr[i] = 0.5 * ((4.0 * d[i].real) - (2.0 * D[i - 1].real))
    di[i] = 0.5 * ((4.0 * d[i].imag) - (2.0 * D[i - 1].imag))
    D[i] = complex(dr[i], di[i])
for i in range(0, N):
    D[i] = D[i] * y[i]
#"""

"""
for i in range(0, N):
    e[i] = X[i] * y[i]
E[0] = e[0]
for i in range(1, N):
    #E[i] = e[i - 1] + (0.5 * (e[i] - e[i - 1]))
    er[i] = e[i - 1].real + (0.5 * (e[i].real - e[i - 1].real))
    ei[i] = e[i - 1].imag + (0.5 * (e[i].imag - e[i - 1].imag))
    E[i] = complex(er[i], ei[i])
"""

#"""
for i in range(0, N):
    e[i] = X[i]
E[0] = e[0]
for i in range(1, N):
    #E[i] = 0.5 * ((4.0 * e[i]) - (2.0 * E[i - 1]))
    er[i] = 0.5 * ((4.0 * e[i].real) - (2.0 * E[i - 1].real))
    ei[i] = 0.5 * ((4.0 * e[i].imag) - (2.0 * E[i - 1].imag))
    E[i] = complex(er[i], ei[i])
for i in range(0, N):
    E[i] = E[i] * y[i]
#"""

for i in range(0, N):
    f[i] = E[i] * x[i]
F[0] = f[0]
for i in range(1, N):
    #F[i] = f[i - 1] + (0.5 * (f[i] - f[i - 1]))
    fr[i] = f[i - 1].real + (0.5 * (f[i].real - f[i - 1].real))
    fi[i] = f[i - 1].imag + (0.5 * (f[i].imag - f[i - 1].imag))
    F[i] = complex(fr[i], fi[i])

#################################################

print(X)
print(Y)
print(Z)
print(A)
print(B)
print(C)
print(D)
print(E)
print(F)
