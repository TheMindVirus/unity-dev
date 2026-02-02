import math #, cmath
#import numpy as np
import time

import ctypes
import struct

dll = ctypes.cdll.LoadLibrary("complicated_dll.dll")

class complex_data(ctypes.Structure):
    _fields_ = \
    [
        ("n", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte))
    ]

def dll_integrate(x):
    N = len(x)
    T = ctypes.c_ubyte * (N * 8)
    bstr = b''
    zstr = b''
    for i in range(0, N):
        bstr += struct.pack("<ff", x[i].real, x[i].imag)
        zstr += struct.pack("<ff", 0.0, 0.0)
    params = complex_data()
    result = complex_data()
    params.n = N
    params.data = T(*bstr)
    result.n = N
    result.data = T(*zstr)
    dll.integrate.argtypes = \
    [
        ctypes.POINTER(complex_data),
        ctypes.POINTER(complex_data)
    ]
    dll.integrate.restype = ctypes.POINTER(complex_data)
    result2 = dll.integrate(ctypes.byref(params), ctypes.byref(result))
    y = [0] * result2.contents.n
    for i in range(0, result2.contents.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.contents.data[j:j+8]))
        y[i] = complex(c[0], c[1])
    return y

def dll_differentiate(y):
    N = len(y)
    T = ctypes.c_ubyte * (N * 8)
    bstr = b''
    zstr = b''
    for i in range(0, N):
        bstr += struct.pack("<ff", y[i].real, y[i].imag)
        zstr += struct.pack("<ff", 0.0, 0.0)
    params = complex_data()
    result = complex_data()
    params.n = N
    params.data = T(*bstr)
    result.n = N
    result.data = T(*zstr)
    dll.differentiate.argtypes = \
    [
        ctypes.POINTER(complex_data),
        ctypes.POINTER(complex_data)
    ]
    dll.differentiate.restype = ctypes.POINTER(complex_data)
    result2 = dll.differentiate(ctypes.byref(params), ctypes.byref(result))
    x = [0] * result2.contents.n
    for i in range(0, result2.contents.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.contents.data[j:j+8]))
        x[i] = complex(c[0], c[1])
    return x

def dll_convolute(x):
    N = len(x)
    T = ctypes.c_ubyte * (N * 8)
    bstr = b''
    zstr = b''
    for i in range(0, N):
        bstr += struct.pack("<ff", x[i].real, x[i].imag)
        zstr += struct.pack("<ff", 0.0, 0.0)
    params = complex_data()
    result = complex_data()
    params.n = N
    params.data = T(*bstr)
    result.n = N
    result.data = T(*zstr)
    dll.convolute.argtypes = \
    [
        ctypes.POINTER(complex_data),
        ctypes.POINTER(complex_data)
    ]
    dll.convolute.restype = ctypes.POINTER(complex_data)
    result2 = dll.convolute(ctypes.byref(params), ctypes.byref(result))
    y = [0] * result2.contents.n
    for i in range(0, result2.contents.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.contents.data[j:j+8]))
        y[i] = complex(c[0], c[1])
    return y

def dll_unwind(y):
    N = len(y)
    T = ctypes.c_ubyte * (N * 8)
    bstr = b''
    zstr = b''
    for i in range(0, N):
        bstr += struct.pack("<ff", y[i].real, y[i].imag)
        zstr += struct.pack("<ff", 0.0, 0.0)
    params = complex_data()
    result = complex_data()
    params.n = N
    params.data = T(*bstr)
    result.n = N
    result.data = T(*zstr)
    dll.unwind.argtypes = \
    [
        ctypes.POINTER(complex_data),
        ctypes.POINTER(complex_data)
    ]
    dll.unwind.restype = ctypes.POINTER(complex_data)
    result2 = dll.unwind(ctypes.byref(params), ctypes.byref(result))
    x = [0] * result2.contents.n
    for i in range(0, result2.contents.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.contents.data[j:j+8]))
        x[i] = complex(c[0], c[1])
    return x

def integrate(x):
    N = len(x)
    y = [0] * N
    y[0] = x[0]
    for i in range(1, N):
        y[i] = x[i - 1] + (0.5 * (x[i] - x[i - 1]))
    return y

def differentiate(y):
    N = len(y)
    x = [0] * N
    x[0] = y[0]
    for i in range(1, N):
        x[i] = (2.0 * y[i]) - x[i - 1]
    return x

def convolute(x):
    N = len(x)
    y = [0] * N
    tau = 2.0 * math.pi
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            #K = cmath.exp((0-1j * 2.0 * math.pi * j * i) / N)
            K = complex(math.cos(jin), math.sin(jin))
            y[i] += x[j] * K
    return y

def unwind(y):
    N = len(y)
    x = [0] * N
    D = (1.0 / N)
    tau = 2.0 * math.pi
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            #K = cmath.exp((0+1j * 2.0 * math.pi * j * i) / N)
            K = complex(math.cos(jin), -math.sin(jin))
            x[i] += y[j] * K * D
    return x

def main():
    T = []
    X = []
    Y = []
    
    N = 2047 #6 #2047 #7 #2048
    for i in range(0, N + 1):
        X.append(complex(i, 0))

    T.append(time.monotonic())

    Y.append(X)
    Y.append([])
    Y.append(integrate(Y[0]))
    Y.append(differentiate(Y[-1]))
    Y.append([])
    Y.append(differentiate(Y[0]))
    Y.append(integrate(Y[-1]))
    Y.append([])
    Y.append(convolute(Y[0]))
    Y.append(unwind(Y[-1]))
    Y.append([])
    Y.append(unwind(Y[0]))
    Y.append(convolute(Y[-1]))
    Y.append([])

    T[-1] = time.monotonic() - T[-1]
    
    T.append(time.monotonic())

    Y.append(X)
    Y.append([])
    Y.append(dll_integrate(Y[0]))
    Y.append(dll_differentiate(Y[-1]))
    Y.append([])
    Y.append(dll_differentiate(Y[0]))
    Y.append(dll_integrate(Y[-1]))
    Y.append([])
    Y.append(dll_convolute(Y[0]))
    Y.append(dll_unwind(Y[-1]))
    Y.append([])
    Y.append(dll_unwind(Y[0]))
    Y.append(dll_convolute(Y[-1]))
    Y.append([])
    
    T[-1] = time.monotonic() - T[-1]

    if N < 10:
        for i in range(0, len(Y)):
            print(Y[i])
    else:
        for i in range(0, len(T)):
            print(T[i], "seconds")

if __name__ == "__main__":
    main()

ctypes.windll.kernel32.FreeLibrary(dll._handle)

"""
13.75 seconds
0.9220000000204891 seconds
"""
