def compand(a):
    if (a >= 0.0):
        return 1.0 - (0.5 * a)
    else:
        return 1.0 - (-0.5 * a)

def mix(a, b):
    return (a * compand(b)) + (b * compand(a))

a = 1.0
b = 1.0
c = 1.0
print(a, b, mix(a, b), c)

a = -1.0
b = -1.0
c = -1.0
print(a, b, mix(a, b), c)

a = 1.0
b = -1.0
c = 0.0
print(a, b, mix(a, b), c)

a = -1.0
b = 1.0
c = 0.0
print(a, b, mix(a, b), c)

#import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("dark_background")
fig = plt.figure()
axes = fig.add_subplot(projection = "3d")
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
axes.scatter(X, Y, Z)
plt.show()
