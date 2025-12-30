import matplotlib.pyplot as plt
import numpy as np
import math

def avg(a, b):
    return (a + b) / 2.0

def soften(a, b):
    return math.sin(avg(a, b) * 0.5 * math.pi)

def sharpen(a, b):
    return math.asin(avg(a, b)) / (0.5 * math.pi)

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

