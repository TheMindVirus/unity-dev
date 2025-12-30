import matplotlib.pyplot as plt
import numpy as np
import math

def add(a, b):
    return a + b

def compand(a):
    if (a >= 0.0):
        return 1.0 - (0.5 * a)
    else:
        return 1.0 - (-0.5 * a)

def mix(a, b):
    return (a * compand(b)) + (b * compand(a))

def soften(a, b):
    return math.sin(add(a, b) * 0.25 * math.pi)
    #return math.sin(mix(a, b) * 0.5 * math.pi)

plt.style.use("dark_background")
fig = plt.figure()

axes = fig.add_subplot(2, 2, 1, projection = "3d")
axes.set_title("Add")
X = []
Y = []
Z = []
for ix in range(0, 100):
    for iy in range(0, 100):
        x = ((float(ix) / 100.0) * 2.0) - 1.0
        y = ((float(iy) / 100.0) * 2.0) - 1.0
        z = add(x, y)
        X.append(x)
        Y.append(y)
        Z.append(z)
axes.set_xlim(-1.0, 1.0)
axes.set_ylim(-1.0, 1.0)
axes.set_zlim(-1.0, 1.0)
axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.scatter(X, Y, Z, marker = ".", c = "red")

axes = fig.add_subplot(2, 2, 2, projection = "3d")
axes.set_title("Compand")
X = []
Y = []
Z = []
for ix in range(0, 100):
    for iy in range(0, 100):
        x = ((float(ix) / 100.0) * 2.0) - 1.0
        y = ((float(iy) / 100.0) * 2.0) - 1.0
        z = (x * compand(y)) + (y * compand(x))
        X.append(x)
        Y.append(y)
        Z.append(z)
axes.set_xlim(-1.0, 1.0)
axes.set_ylim(-1.0, 1.0)
axes.set_zlim(-1.0, 1.0)
axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.scatter(X, Y, Z, marker = ".", c = "cyan")

axes = fig.add_subplot(2, 2, 3, projection = "3d")
axes.set_title("Mix")
X = []
Y = []
Z = []
for ix in range(0, 100):
    for iy in range(0, 100):
        x = ((float(ix) / 100.0) * 2.0) - 1.0
        y = ((float(iy) / 100.0) * 2.0) - 1.0
        z = mix(x, y)
        X.append(x)
        Y.append(y)
        Z.append(z)
axes.set_xlim(-1.0, 1.0)
axes.set_ylim(-1.0, 1.0)
axes.set_zlim(-1.0, 1.0)
axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.scatter(X, Y, Z, marker = ".", c = "blue")

axes = fig.add_subplot(2, 2, 4, projection = "3d")
axes.set_title("Soften")
X = []
Y = []
Z = []
for ix in range(0, 100):
    for iy in range(0, 100):
        x = ((float(ix) / 100.0) * 2.0) - 1.0
        y = ((float(iy) / 100.0) * 2.0) - 1.0
        z = soften(x, y)
        X.append(x)
        Y.append(y)
        Z.append(z)
axes.set_xlim(-1.0, 1.0)
axes.set_ylim(-1.0, 1.0)
axes.set_zlim(-1.0, 1.0)
axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
axes.scatter(X, Y, Z, marker = ".", c = "yellow")

plt.show()

