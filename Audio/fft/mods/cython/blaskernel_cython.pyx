from cython.operator import dereference
import struct

cdef extern from "blaskernel_cpp.cpp":
    cdef struct complex_data:
        int n
        unsigned char* data

cdef extern complex_data* fft(complex_data* params, complex_data* result)
cdef extern complex_data* ifft(complex_data* params, complex_data* result)

def wrap_fft(x):
    N = len(x)
    bstr = b''
    zstr = b''
    for i in range(0, N):
        bstr += struct.pack("<ff", x[i].real, x[i].imag)
        zstr += struct.pack("<ff", 0.0, 0.0)
    cdef complex_data params = complex_data()
    cdef complex_data result = complex_data()
    params.n = N;
    params.data = bstr
    result.n = N
    result.data = zstr
    cdef complex_data result2 = dereference(fft(&params, &result))
    y = [0] * result2.n
    for i in range(0, result2.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.data[j:j+8]))
        y[i] = complex(c[0], c[1])
    return y

def wrap_ifft(y):
    N = len(y)
    bstr = b''
    zstr = b''
    for i in range(0, N):
        bstr += struct.pack("<ff", y[i].real, y[i].imag)
        zstr += struct.pack("<ff", 0.0, 0.0)
    cdef complex_data params = complex_data()
    cdef complex_data result = complex_data()
    params.n = N;
    params.data = bstr
    result.n = N
    result.data = zstr
    cdef complex_data result2 = dereference(ifft(&params, &result))
    x = [0] * result2.n
    for i in range(0, result2.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.data[j:j+8]))
        x[i] = complex(c[0], c[1])
    return x