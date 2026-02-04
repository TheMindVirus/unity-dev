import ctypes
import struct

dll = ctypes.cdll.LoadLibrary("blaskernel.dll")

class complex_data(ctypes.Structure):
    _fields_ = \
    [
        ("n", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte))
    ]

def fft(x):
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
    dll.fft.argtypes = \
    [
        ctypes.POINTER(complex_data),
        ctypes.POINTER(complex_data)
    ]
    dll.fft.restype = ctypes.POINTER(complex_data)
    result2 = dll.fft(ctypes.byref(params), ctypes.byref(result))
    y = [0] * result2.contents.n
    for i in range(0, result2.contents.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.contents.data[j:j+8]))
        y[i] = complex(c[0], c[1])
    return y

def ifft(y):
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
    dll.ifft.argtypes = \
    [
        ctypes.POINTER(complex_data),
        ctypes.POINTER(complex_data)
    ]
    dll.ifft.restype = ctypes.POINTER(complex_data)
    result2 = dll.ifft(ctypes.byref(params), ctypes.byref(result))
    x = [0] * result2.contents.n
    for i in range(0, result2.contents.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.contents.data[j:j+8]))
        x[i] = complex(c[0], c[1])
    return x
