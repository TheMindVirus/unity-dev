#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

from cython.parallel cimport prange, parallel
from cython.cimports.libc.math cimport sin, cos, pow, abs
#from cython.cimports.libc.complex cimport cexp, cpow
from cython.cimports.libc.stdlib cimport malloc, free
from cython.cimports.libc.string cimport memcpy
cimport openmp

#from cython.cimports.libc.time cimport clock, clock_t, CLOCKS_PER_SEC
import numpy as np
import cmath
"""
cdef extern from "complex.h" nogil:
   ctypedef struct _Dcomplex:
       float real
       float imag
   cdef _Dcomplex cexp(_Dcomplex)
   cdef _Dcomplex cpow(_Dcomplex, _Dcomplex)
"""
cdef int num_threads
cdef float complex k = 0
cdef size_t sz = sizeof(k)
openmp.omp_set_dynamic(1)
with nogil, parallel():
    num_threads = openmp.omp_get_num_threads()

modes = \
{
    "GAUSS": 0,
    "FFT": 1,
    "FOURIER": 2,
    "LAPLACE": 3,
}

def gauss_filter(x, eq):
    cdef int N = len(x)
    eq["f"] *= N
    for i in range(1, N):
        p = i
        if (i > N / 2):
            p = N - i
        factor = (pow(eq["c"], -abs(pow(p - eq["f"], eq["b"])) / eq["q"]) * eq["g"]) + eq["l"];
        x[i] = complex(x[i].real * factor, x[i].imag * factor)
        #x[i].real = (x[i].real * factor) - (x[i].imag * 0);
        #x[i].imag = (x[i].real * 0) + (x[i].imag * factor);
        x[i] = complex(x[i].real, x[i].imag)
    return x

cdef struct _fourier_forward_struct:
    float* kr
    float* ki
cdef _fourier_forward_struct fourier_forward_struct

def fourier_forward_setup(n = 2048):
    cdef int N = n
    cdef int N2 = N * N
    cdef size_t sz = sizeof(float)
    cdef size_t nsz = sz * N2
    cdef float* kr = <float*>malloc(nsz)
    cdef float* ki = <float*>malloc(nsz)
    cdef float tau = <float>6.283185307179586
    cdef float complex jin = 0.0
    cdef int idx = 0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    for a in range(0, N2):
        i = a / N
        j = a - (i * N)
        idx = (i * N) + j
        jin = (0-1j * tau * j * i) / N
        kr[idx] = cmath.exp(jin).real
        ki[idx] = cmath.exp(jin).imag
    fourier_forward_struct.kr = kr
    fourier_forward_struct.ki = ki
fourier_forward_setup()

def fourier_forward(x):
    cdef int N = len(x)
    cdef int N2 = N * N
    y = [0] * N
    cdef size_t sz = sizeof(float)
    cdef size_t nsz = sz * N
    cdef float* Xr = <float*>malloc(nsz)
    cdef float* Xi = <float*>malloc(nsz)
    cdef float* Yr = <float*>malloc(nsz)
    cdef float* Yi = <float*>malloc(nsz)
    cdef float* kr = fourier_forward_struct.kr
    cdef float* ki = fourier_forward_struct.ki
    cdef float Kr = 0.0
    cdef float Ki = 0.0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    cdef int idx = 0
    for i in range(0, N):
        Xr[i] = x[i].real
        Xi[i] = x[i].imag
    for i in prange(0, N, nogil = True):
        Yr[i] = 0.0
        Yi[i] = 0.0
    for a in prange(0, N2, nogil = True):
        i = a / N
        j = a - (i * N)
        idx = (i * N) + j #!!! BUG: runs slower when swapping i with j!
        Kr = kr[idx]
        Ki = ki[idx]
        Yr[i] += ((Xr[j] * Kr) - (Xi[j] * Ki))
        Yi[i] += ((Xr[j] * Ki) + (Xi[j] * Kr))
    for i in range(0, N):
        y[i] = complex(Yr[i], Yi[i])
    free(Xr)
    free(Xi)
    free(Yr)
    free(Yi)
    return y

cdef struct _fourier_backward_struct:
    float* kr
    float* ki
cdef _fourier_backward_struct fourier_backward_struct

def fourier_backward_setup(n = 2048):
    cdef int N = n
    cdef int N2 = N * N
    cdef size_t sz = sizeof(float)
    cdef size_t nsz = sz * N2
    cdef float* kr = <float*>malloc(nsz)
    cdef float* ki = <float*>malloc(nsz)
    cdef float tau = <float>6.283185307179586
    cdef float complex jin = 0.0
    cdef int idx = 0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    for a in range(0, N2):
        i = a / N
        j = a - (i * N)
        idx = (i * N) + j
        jin = (0+1j * tau * j * i) / N
        kr[idx] = cmath.exp(jin).real
        ki[idx] = cmath.exp(jin).imag
    fourier_backward_struct.kr = kr
    fourier_backward_struct.ki = ki
fourier_backward_setup()

def fourier_backward(y):
    cdef int N = len(y)
    cdef int N2 = N * N
    x = [0] * N
    cdef float D = 1.0 / N
    cdef size_t sz = sizeof(float)
    cdef size_t nsz = sz * N
    cdef float* Yr = <float*>malloc(nsz)
    cdef float* Yi = <float*>malloc(nsz)
    cdef float* Xr = <float*>malloc(nsz)
    cdef float* Xi = <float*>malloc(nsz)
    cdef float* kr = fourier_backward_struct.kr
    cdef float* ki = fourier_backward_struct.ki
    cdef float Kr = 0.0
    cdef float Ki = 0.0
    cdef int idx = 0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    for i in range(0, N):
        Yr[i] = y[i].real
        Yi[i] = y[i].imag
    for i in prange(0, N, nogil = True):
        Xr[i] = 0.0
        Xi[i] = 0.0
    for a in prange(0, N2, nogil = True):
        i = a / N
        j = a - (i * N)
        idx = (i * N) + j
        Kr = kr[idx]
        Ki = ki[idx]
        Xr[i] += (((Yr[j] * Kr) - (Yi[j] * Ki)) * D)
        Xi[i] += (((Yr[j] * Ki) + (Yi[j] * Kr)) * D)
    for i in range(0, N):
        x[i] = complex(Xr[i], Xi[i])
    free(Xr)
    free(Xi)
    free(Yr)
    free(Yi)
    return x

cdef struct _laplace_forward_struct:
    float* kr
    float* ki
cdef _laplace_forward_struct laplace_forward_struct

def laplace_forward_setup(n = 2048):
    cdef int N = n
    cdef int N2 = N * N
    cdef size_t sz = sizeof(float)
    cdef size_t nsz = sz * N2
    cdef float* kr = <float*>malloc(nsz)
    cdef float* ki = <float*>malloc(nsz)
    cdef float tau = <float>6.283185307179586
    cdef float complex jin = 0.0
    cdef float complex tmp = 0.0
    cdef float complex pmt = 0.0
    cdef int idx = 0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    for a in range(0, N2):
        i = a / N
        j = a - (i * N)
        idx = (i * N) + j
        jin = -(j * i) / N
        tmp.real = 0.0
        tmp.imag = tau
        #jin *= tmp #!!! BUG: incorrect values received
        pmt.real = (jin.real * tmp.real) - (jin.imag * tmp.imag)
        pmt.imag = (jin.real * tmp.imag) + (jin.imag * tmp.real)
        jin.real = pmt.real
        jin.imag = pmt.imag
        #jin = -(0+1j * tau * j * i) / N
        kr[idx] = cmath.exp(jin).real
        ki[idx] = cmath.exp(jin).imag
    laplace_forward_struct.kr = kr
    laplace_forward_struct.ki = ki
laplace_forward_setup()

def laplace_forward(x):
    cdef int N = len(x)
    cdef int N2 = N * N
    y = [0] * N
    cdef size_t sz = sizeof(float)
    cdef size_t nsz = sz * N
    cdef float* Xr = <float*>malloc(nsz)
    cdef float* Xi = <float*>malloc(nsz)
    cdef float* Yr = <float*>malloc(nsz)
    cdef float* Yi = <float*>malloc(nsz)
    cdef float* kr = laplace_forward_struct.kr
    cdef float* ki = laplace_forward_struct.ki
    cdef float Kr = 0.0
    cdef float Ki = 0.0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    cdef int idx = 0
    for i in range(0, N):
        Xr[i] = x[i].real
        Xi[i] = x[i].imag
    for i in prange(0, N, nogil = True):
        Yr[i] = 0.0
        Yi[i] = 0.0
    for a in prange(0, N2, nogil = True):
        i = a / N
        j = a - (i * N)
        idx = (i * N) + j
        Kr = kr[idx]
        Ki = ki[idx]
        Yr[i] += ((Xr[j] * Kr) - (Xi[j] * Ki))
        Yi[i] += ((Xr[j] * Ki) + (Xi[j] * Kr))
    for i in range(0, N):
        y[i] = complex(Yr[i], Yi[i])
    free(Xr)
    free(Xi)
    free(Yr)
    free(Yi)
    return y

cdef struct _laplace_backward_struct:
    float* kr
    float* ki
cdef _laplace_backward_struct laplace_backward_struct

def laplace_backward_setup(n = 2048):
    cdef int N = n
    cdef int N2 = N * N
    cdef size_t sz = sizeof(float)
    cdef size_t nsz = sz * N2
    cdef float* kr = <float*>malloc(nsz)
    cdef float* ki = <float*>malloc(nsz)
    cdef float tau = <float>6.283185307179586
    cdef float complex jin = 0.0
    cdef int idx = 0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    for a in range(0, N2):
        i = a / N
        j = a - (i * N)
        idx = (i * N) + j
        jin = ((j * i) / N) / (0+1j * tau) #!!! BUG: not the same as (tau * 0+1j)!
        jin *= (0+1j * tau)
        jin *= (0+1j * tau)
        kr[idx] = cmath.exp(jin).real
        ki[idx] = cmath.exp(jin).imag
    laplace_backward_struct.kr = kr
    laplace_backward_struct.ki = ki
laplace_backward_setup()

def laplace_backward(y):
    cdef int N = len(y)
    cdef int N2 = N * N
    x = [0] * N
    cdef float D = 1.0 / N
    cdef size_t sz = sizeof(float)
    cdef size_t nsz = sz * N
    cdef float* Yr = <float*>malloc(nsz)
    cdef float* Yi = <float*>malloc(nsz)
    cdef float* Xr = <float*>malloc(nsz)
    cdef float* Xi = <float*>malloc(nsz)
    cdef float* kr = laplace_backward_struct.kr
    cdef float* ki = laplace_backward_struct.ki
    cdef float Kr = 0.0
    cdef float Ki = 0.0
    cdef int idx = 0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    for i in range(0, N):
        Yr[i] = y[i].real
        Yi[i] = y[i].imag
    for i in prange(0, N, nogil = True):
        Xr[i] = 0.0
        Xi[i] = 0.0
    for a in prange(0, N2, nogil = True):
        i = a / N
        j = a - (i * N)
        idx = (i * N) + j
        Kr = kr[idx]
        Ki = ki[idx]
        Xr[i] += (((Yr[j] * Kr) - (Yi[j] * Ki)) * D)
        Xi[i] += (((Yr[j] * Ki) + (Yi[j] * Kr)) * D)
    for i in range(0, N):
        x[i] = complex(Xr[i], Xi[i])
    free(Xr)
    free(Xi)
    free(Yr)
    free(Yi)
    return x