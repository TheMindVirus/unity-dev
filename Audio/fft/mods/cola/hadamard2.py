import math
import numpy as np

x = [0,1,2,3,4,5,6,7]
x = np.linspace(0, 1023, 1024)
n = len(x)

y = x.copy()
h = 1
while h < n:
    for i in range(0, n, h * 2):
        for j in range(i, i + h):
            a = y[j]
            b = y[j + h]
            y[j] = a + b
            y[j + h] = a - b
    for i in range(0, n):
        x[i] /= math.sqrt(2)
    h *= 2

print(y)

x = y.copy()
h = 1
while h < n:
    for i in range(0, n, h * 2):
        for j in range(i, i + h):
            a = x[j]
            b = x[j + h]
            x[j] = a + b
            x[j + h] = a - b
    for i in range(0, n):
        y[i] /= math.sqrt(2)
    h *= 2
for i in range(0, n):
    x[i] /= n

print(x)
