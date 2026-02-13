import filters

x = [0,1,2,3,4,5,6,7]
bsz = len(x)

eq = \
{
    "c": 5.0,
    "b": 2.0,
    "f": 0.0,
    "q": bsz,
    "g": 0.0,
    "l": 1.0,
}

filters.fourier_setup(bsz)
a = filters.fourier(x, eq)
filters.laplace_setup(bsz)
b = filters.laplace(x, eq)
filters.hilbert_setup(bsz)
c = filters.hilbert(x, eq)
filters.hartley_setup(bsz)
d = filters.hartley(x, eq)

print("fourier:\n", a, end = "\n\n")
print("laplace:\n", b, end = "\n\n")
print("hilbert:\n", c, end = "\n\n")
print("hartley:\n", d, end = "\n\n")

"""
import numpy as np
x = np.linspace(0, 1023, 1024)
filters.laplace_setup(1024)
c = filters.laplace(list(x), eq, mode = 1)
print(c[85:95])
"""

print("hadamard:", filters.hadamard(x, eq), end = "\n\n")
print("gauss:", filters.gauss(bsz, eq), end = "\n\n")
