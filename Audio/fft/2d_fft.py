import numpy as np
import math, cmath

print("BEGIN NP-2D")

X = [[ 0,  1,  2,  3,  4,  5,  6],
     [-1,  0,  1,  2,  3,  4,  5],
     [-2, -1,  0,  1,  2,  3,  4],
     [-3, -2, -1,  0,  1,  2,  3],
     [-4, -3, -2, -1,  0,  1,  2],
     [-5, -4, -3, -2, -1,  0,  1],
     [-6, -5, -4, -3, -2, -1,  0]]

Y = np.fft.fft2(X)
Y = np.round(Y)
Z = np.fft.ifft2(Y)
Z = np.round(Z.real)

N = len(X)
M = len(X[0])

for i in range(0, N):
    print(X[i])
print(Y)
print(Z)

print("BEGIN NP-1D")

Y = np.zeros_like(Y)
Z = np.zeros_like(Z, dtype = complex)

for i in range(0, len(X)):
    Y[i] = np.fft.fft(X[i])
    #Y[i] = np.round(Y[i])
for i in range(0, len(Y[0])):
    D = [Y[j][i] for j in range(0, len(Y[i]))]
    YY = np.fft.fft(D)
    YY = np.round(YY)
    for j in range(0, len(YY)):
        Y[j][i] = YY[j]

for i in range(0, len(Y[0])):
    D = [Y[j][i] for j in range(0, len(Y[i]))]
    ZZ = np.fft.ifft(D)
    #ZZ = np.round(ZZ)
    for j in range(0, len(ZZ)):
        Z[j][i] = ZZ[j]
for i in range(0, len(Z)):
    Z[i] = np.fft.ifft(Z[i])
    Z[i] = np.round(Z[i].real)
Z = Z.real

for i in range(0, N):
    print(X[i])
print(Y)
print(Z)

print("BEGIN 2D-NP")

x = X
y = []
yi = []
zii = []
zi = []
z = []
for j in range(0, M):
    y.append([])
    yi.append([])
    zii.append([])
    zi.append([])
    z.append([])
    for i in range(0, N):
        y[j].append([0.0, 0.0])
        yi[j].append([0.0, 0.0])
        zii[j].append([0.0, 0.0])
        zi[j].append([0.0, 0.0])
        z[j].append(0.0)

for k in range(0, M):
    for i in range(0, N):
        for j in range(0, N):
            yi[k][i][0] += x[k][j] * math.cos((2.0 * math.pi * j * i) / N)
            yi[k][i][1] += x[k][j] * -math.sin((2.0 * math.pi * j * i) / N)
    #for i in range(0, N):
    #    for j in range(0, N):
    #        yi[k][i][0] = round(yi[k][i][0])
    #        yi[k][i][1] = round(yi[k][i][1])
for k in range(0, N):
    for i in range(0, M):
        for j in range(0, M):
            y[i][k][0] += (yi[j][k][0] * math.cos((2.0 * math.pi * j * i) / M))
            y[i][k][0] += (yi[j][k][1] * -math.sin((2.0 * math.pi * j * i) / M))
            y[i][k][1] += (yi[j][k][0] * -math.sin((2.0 * math.pi * j * i) / M))
            y[i][k][1] += (yi[j][k][1] * math.cos((2.0 * math.pi * j * i) / M))
    for i in range(0, M):
        for j in range(0, M):
            y[i][k][0] = round(y[i][k][0])
            y[i][k][1] = round(y[i][k][1])

#y[0][1][0] = -24
#y[0][2][0] = -24
#y[1][0][0] = 24
#y[2][0][0] = 24

for k in range(0, N):
    for i in range(0, M):
        for j in range(0, M):
            t = math.cos((2.0 * math.pi * j * i) / M)
            t += math.sin((2.0 * math.pi * j * i) / M)
            zii[i][k][0] += y[j][k][0] * t * (1 / M)
            zii[i][k][0] -= y[j][k][1] * t * (1 / M)
            #u = math.cos((2.0 * math.pi * j * i) / M)
            #u += math.sin((2.0 * math.pi * j * i) / M)
            #zii[i][k][1] -= y[j][k][0] * u * (1 / M)
            #zii[i][k][1] += y[j][k][1] * u * (1 / M)
for k in range(0, M):
    for i in range(0, N):
        for j in range(0, N):
            t = math.cos((2.0 * math.pi * j * i) / N)
            t += math.sin((2.0 * math.pi * j * i) / N)
            zi[k][i][0] += zii[k][j][0] * t * (1 / N)
            #zi[k][i][0] -= zii[k][j][1] * t * (1 / N)

for j in range(0, M):
    for i in range(0, N):
        z[j][i] = round(zi[j][i][0])

for i in range(0, N):
    print(x[i])
for i in range(0, N):
    for j in range(0, M):
        print(y[i][j], end = ", ")
    print()
for i in range(0, N):
    for j in range(0, M):
        print(z[i][j], end = ", ")
    print()
