#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from cython.parallel cimport prange, parallel
from cython.cimports.libc.math cimport sin, cos, M_PI
from cython.cimports.libc.stdlib cimport malloc
from cython.cimports.libc.string cimport memcpy
cimport openmp

cdef float tau = 2.0 * M_PI
cdef float complex k = 0
cdef int sz = sizeof(k)
cdef int num_threads
openmp.omp_set_dynamic(1)
with nogil, parallel():
    num_threads = openmp.omp_get_num_threads()

def blas_fft(x):
    cdef int N = len(x)
    cdef int N2 = N * N
    y = [0] * N
    cdef float complex K = 0
    cdef float complex A = 0
    cdef float complex B = 0
    cdef int nsz = sz * N
    cdef float complex[:] X = <float complex[:N]>malloc(nsz)
    cdef float complex[:] Y = <float complex[:N]>malloc(nsz)
    cdef float jin = 0.0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    for i in range(0, N):
        X[i] = x[i]
    for i in prange(0, N, nogil = True):
        Y[i] = 0.0
    for a in prange(0, N2, nogil = True):
        i = int(a / N)
        j = a - (i * N)
        jin = (tau * j * i) / N
        K.real = cos(jin)
        K.imag = -sin(jin)
        memcpy(&A, &Y[i], sz)
        memcpy(&B, &X[j], sz)
        B = B * K
        A = A + B
        memcpy(&Y[i], &A, sz)
    for i in range(0, N):
        y[i] = Y[i]
    return y

def blas_ifft(y):
    cdef int N = len(y)
    cdef int N2 = N * N
    cdef float D = 1.0 / N
    x = [0] * N
    cdef float complex K = 0
    cdef float complex A = 0
    cdef float complex B = 0
    cdef int nsz = sz * N
    cdef float complex[:] Y = <float complex[:N]>malloc(nsz)
    cdef float complex[:] X = <float complex[:N]>malloc(nsz)
    cdef float jin = 0.0
    cdef int i = 0
    cdef int j = 0
    cdef int a = 0
    for i in range(0, N):
        Y[i] = y[i]
    for i in prange(0, N, nogil = True):
        X[i] = 0.0
    for a in prange(0, N2, nogil = True):
        i = int(a / N)
        j = a - (i * N)
        jin = (tau * j * i) / N
        K.real = cos(jin)
        K.imag = sin(jin)
        memcpy(&A, &X[i], sz)
        memcpy(&B, &Y[j], sz)
        B = B * K * D
        A = A + B
        memcpy(&X[i], &A, sz)
    for i in range(0, N):
        x[i] = X[i]
    return x