import matplotlib.pyplot as plt
import numpy as np
import math

def compand(a):
    if (a >= 0.0):
        return 1.0 - (0.5 * a)
    else:
        return 1.0 - (-0.5 * a)

def mix(a, b):
    return (a * compand(b)) + (b * compand(a))

def soften(a, b, n = 100):
    return ((1.0 / (1.0 + pow(n, (-mix(a, b))))) - 0.5) * 2.0

def sharpen(a, b, n = 100):
    c = (mix(a, b) / 2.0) + 0.5
    if c == 0:
        return -1
    d = -math.log((1.0 / c) - 1.0) / math.log(n)
    if d < -1:
        d = -1
    if d > 1:
        d = 1
    return d

plt.style.use("dark_background")
fig = plt.figure()

X = []
Y = []
Z1 = []
Z2 = []
for ix in range(0, 100):
    for iy in range(0, 100):
        x = ((float(ix) / 100.0) * 2.0) - 1.0
        y = ((float(iy) / 100.0) * 2.0) - 1.0
        z1 = soften(x, y)
        z2 = sharpen(x, y)
        X.append(x)
        Y.append(y)
        Z1.append(z1)
        Z2.append(z2)

axes = fig.add_subplot(2, 1, 1, projection = "3d")
axes.set_title("Soften")
axes.set_xlim(-1.0, 1.0)
axes.set_ylim(-1.0, 1.0)
axes.set_zlim(-1.0, 1.0)
axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.scatter(X, Y, Z1, marker = ".", c = "yellow")

axes = fig.add_subplot(2, 1, 2, projection = "3d")
axes.set_title("Sharpen")
axes.set_xlim(-1.0, 1.0)
axes.set_ylim(-1.0, 1.0)
axes.set_zlim(-1.0, 1.0)
axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.scatter(X, Y, Z2, marker = ".", c = "cyan")

plt.show()

