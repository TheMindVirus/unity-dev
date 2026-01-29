import math

X = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
N = len(X)

Yr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
Yi = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

Y = [[0, 0]] * N
Z = [[0, 0]] * N

#def cadd(x, y):
#    return [x[0] + y[0], x[1] + y[1]]

#def cmul(x, y):
#    return [(x[0] * y[0]) - (x[1] * y[1]), ((x[0] * y[1]) + (x[1] * y[0]))]

#def cpow(x):
#    return [math.cos(x), math.sin(x)]

#def cneg(x):
#    return [x[0], -x[1]]

for i in range(0, N):
    for j in range(0, N):
        Yr[i] += X[j] * math.cos((2.0 * math.pi * j * i) / N)
        Yi[i] += X[j] * -math.sin((2.0 * math.pi * j * i) / N)
        #Y[i] = cadd(Y[i], cmul([X[j], 0], cneg(cpow((2.0 * math.pi * j * i) / N))))

#for i in range(0, len(Y)):
#    Yr[i] = Y[i][0]
#    Yi[i] = Y[i][1]

#for i in range(0, len(Y)):
#    Y[i][0] = Yr[i]
#    Y[i][1] = Yi[i]

for i in range(0, N):
    for j in range(0, N):
        t = Yr[j] * math.cos((2.0 * math.pi * j * i) / N)
        t -= Yi[j] * math.sin((2.0 * math.pi * j * i) / N)
        #x: [1/N, 0], y: t, ?
        #Z[i][0] += (1 / N) * t # - (0 * ?)
        #Z[i][0] = Z[i][0] + ((1 / N) * t) #???
        Z[i] = [Z[i][0] + ((1 / N) * t), Z[i][1] + 0]
        #Z[i] = cadd(Z[i], [(1 / N) * t, 0])
        #Z[i] = cadd(Z[i], cmul([(1 / N), 0], [t, 0]))
        #Z[i] = cadd(Z[i], cmul([(1 / N), 0], cmul([Yr[j], Yi[j]], cpow((2.0 * math.pi * j * i) / N))))
        #Z[i] = cadd(Z[i], cmul([(1 / N), 0], cmul([Yr[j], -Yi[j]], cneg(cpow((2.0 * math.pi * j * i) / N)))))
        #Z[i] = cadd(Z[i], cmul([(1 / N), 0], cmul(Y[j], cpow((2.0 * math.pi * j * i) / N))))

for i in range(0, len(Z)):
    Z[i] = round(Z[i][0])

print(X)
print(Y)
print(Yr)
print(Yi)
print(Z)

"""
import numpy as np

print(np.fft.fft(X))
print(np.fft.ifft(np.fft.fft(X)))
"""
