#include <complex.h>
#include <Python.h>
#include <omp.h>

static PyObject* modes_get()
{
    PyObject* modes = PyDict_New();
    PyDict_SetItem(modes, PyUnicode_FromString("NULL"), PyLong_FromLong(0));
    PyDict_SetItem(modes, PyUnicode_FromString("FOURIER"), PyLong_FromLong(1));
    PyDict_SetItem(modes, PyUnicode_FromString("LAPLACE"), PyLong_FromLong(2));
    PyDict_SetItem(modes, PyUnicode_FromString("HILBERT"), PyLong_FromLong(3));
    PyDict_SetItem(modes, PyUnicode_FromString("HARTLEY"), PyLong_FromLong(4));
    return modes;
}

PyDoc_STRVAR(gauss_filter_doc, "gauss filter transform");
static PyObject* gauss_filter(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    PyObject* eq = NULL;
    static char* keywords[] = { "n", "eq", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &n, &eq)) { return NULL; }
    Py_ssize_t N = PyLong_AsLong(n);
    PyObject* z = PyList_New(N);
    float x = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("x")));
    float c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    x *= N;
    float X = 0.0;
    float factor = 0.0;
    int idx = 0;
    for (Py_ssize_t i = 0; i < N; ++i)
    {
        X = ((float)i);
        if (i > N / 2) { X = (N - i); }
        factor = (pow(c, (-abs(pow(X - x, b)) / q)) * g) + l;
        PyList_SetItem(z, i, PyFloat_FromDouble(factor));
    }
    return z;
}

PyDoc_STRVAR(gauss_filter_2d_doc, "gauss filter 2d transform");
static PyObject* gauss_filter_2d(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    PyObject* eq = NULL;
    static char* keywords[] = { "n", "eq", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &n, &eq)) { return NULL; }
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    PyObject* z = PyList_New(N2);
    float x = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("x")));
    float y = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("y")));
    float c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    x *= N;
    y *= N;
    float X = 0.0;
    float Y = 0.0;
    float factor = 0.0;
    int idx = 0;
    for (Py_ssize_t i = 0; i < N; ++i)
    {
        X = ((float)i);
        if (i > N / 2) { X = (N - i); }
        for (Py_ssize_t j = 0; j < N; ++j)
        {
            Y = ((float)j);
            if (i > N / 2) { Y = (N - i); }
            factor = (pow(c, (-abs(pow(X - x, b)) / q) + (-abs(pow(Y - y, b)) / q)) * g) + l;
            idx = (j * N) + i;
            PyList_SetItem(z, idx, PyFloat_FromDouble(factor));
        }
    }
    return z;
}

struct _fourier_forward_struct
{
    float complex* k;
};
static struct _fourier_forward_struct fourier_forward_struct;

PyDoc_STRVAR(fourier_forward_setup_doc, "setup for forward fourier transform");
static PyObject* fourier_forward_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    size_t nsz = sz * N2;
    float complex* k = (float complex*)malloc(nsz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = (-I * tau * j * i) / N;
        k[idx] = cexp(jin);
    }
    fourier_forward_struct.k = k;
    return Py_None;
}

PyDoc_STRVAR(fourier_forward_doc, "forward fourier transform");
static PyObject* fourier_forward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N2);
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float complex);
    float complex* k = fourier_forward_struct.k;
    float complex* X = (float complex*)malloc(N * sz);
    float complex* Y = (float complex*)malloc(N2 * sz);
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        Y[a] = 0.0;
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Y[idx] = X[j] * k[idx];
    }
    for (a = 0; a < N2; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(creal(Y[a]), cimag(Y[a])));
    }
    free(X);
    free(Y);
    return y;
}

struct _fourier_backward_struct
{
    float complex* k;
};
static struct _fourier_backward_struct fourier_backward_struct;

PyDoc_STRVAR(fourier_backward_setup_doc, "setup for backward fourier transform");
static PyObject* fourier_backward_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    size_t nsz = sz * N2;
    float complex* k = (float complex*)malloc(nsz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = (-I * tau * j * i) / N;
        k[idx] = pow(cexp(jin), -1);
    }
    fourier_backward_struct.k = k;
    return Py_None;
}

PyDoc_STRVAR(fourier_backward_doc, "backward fourier transform");
static PyObject* fourier_backward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* y = NULL;
    static char* keywords[] = { "y", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &y)) { return NULL; }
    Py_ssize_t N2 = PyList_Size(y);
    Py_ssize_t N = sqrt(N2);
    PyObject* x = PyList_New(N);
    int idx = 0;
    int jdx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float complex);
    float complex* k = fourier_backward_struct.k;
    float complex* Y = (float complex*)malloc(N2 * sz);
    float complex* Z = (float complex*)malloc(N2 * sz);
    float complex* X = (float complex*)malloc(N * sz);
    for (a = 0; a < N; ++a)
    {
        X[a] = 0.0;
    }
    for (a = 0; a < N2; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(y, a));
        Y[a] = data.real + (I * data.imag);
        Z[a] = 0.0;
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Z[idx] = Y[idx] * k[idx];
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        jdx = (j * N) + i;
        X[i] += Z[jdx];
    }
    #pragma omp parallel for
    for (a = 0; a < N; ++a)
    {
        X[a] /= N;
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(x, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    free(Y);
    free(Z);
    free(X);
    return x;
}

struct _laplace_forward_struct
{
    float complex* k;
};
static struct _laplace_forward_struct laplace_forward_struct;

PyDoc_STRVAR(laplace_forward_setup_doc, "setup for forward laplace transform");
static PyObject* laplace_forward_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    size_t nsz = sz * N2;
    float complex* k = (float complex*)malloc(nsz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = -(j * i) / N;
        k[idx] = cexp(jin);
    }
    laplace_forward_struct.k = k;
    return Py_None;
}

PyDoc_STRVAR(laplace_forward_doc, "forward laplace transform");
static PyObject* laplace_forward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N2);
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float complex);
    float complex* k = laplace_forward_struct.k;
    float complex* X = (float complex*)malloc(N * sz);
    float complex* Y = (float complex*)malloc(N2 * sz);
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        Y[a] = 0.0;
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Y[idx] = X[j] * k[idx];
    }
    for (a = 0; a < N2; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(creal(Y[a]), cimag(Y[a])));
    }
    free(X);
    free(Y);
    return y;
}

struct _laplace_backward_struct
{
    float complex* k;
};
static struct _laplace_backward_struct laplace_backward_struct;

PyDoc_STRVAR(laplace_backward_setup_doc, "setup for backward laplace transform");
static PyObject* laplace_backward_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    size_t nsz = sz * N2;
    float complex* k = (float complex*)malloc(nsz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = -(j * i) / N;
        k[idx] = pow(cexp(jin), -1);
    }
    laplace_backward_struct.k = k;
    return Py_None;
}

PyDoc_STRVAR(laplace_backward_doc, "backward laplace transform");
static PyObject* laplace_backward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* y = NULL;
    static char* keywords[] = { "y", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &y)) { return NULL; }
    Py_ssize_t N2 = PyList_Size(y);
    Py_ssize_t N = sqrt(N2);
    PyObject* x = PyList_New(N);
    int idx = 0;
    int jdx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float complex);
    float complex* k = laplace_backward_struct.k;
    float complex* Y = (float complex*)malloc(N2 * sz);
    float complex* Z = (float complex*)malloc(N2 * sz);
    float complex* X = (float complex*)malloc(N * sz);
    for (a = 0; a < N; ++a)
    {
        X[a] = 0.0;
    }
    for (a = 0; a < N2; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(y, a));
        Y[a] = data.real + (I * data.imag);
        Z[a] = 0.0;
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Z[idx] = Y[idx] * k[idx];
    }
    #pragma omp parallel for
    for (a = 0; a < N; ++a)
    {
        X[a] = Z[a];
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(x, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    free(Y);
    free(Z);
    free(X);
    return x;
}

struct _hilbert_forward_struct
{
    float complex* k;
};
static struct _hilbert_forward_struct hilbert_forward_struct;

PyDoc_STRVAR(hilbert_forward_setup_doc, "setup for forward hilbert transform");
static PyObject* hilbert_forward_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    size_t nsz = sz * N2;
    float complex* k = (float complex*)malloc(nsz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        if ((j == 0) || (i == 0)) { jin = 0.0; }
        else { jin = 1.0 / (j * i); }
        k[idx] = jin / tau;
    }
    hilbert_forward_struct.k = k;
    return Py_None;
}

PyDoc_STRVAR(hilbert_forward_doc, "forward hilbert transform");
static PyObject* hilbert_forward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N2);
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float complex);
    float complex* k = hilbert_forward_struct.k;
    float complex* X = (float complex*)malloc(N * sz);
    float complex* Y = (float complex*)malloc(N2 * sz);
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        Y[a] = 0.0;
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Y[idx] = X[j] * k[idx];
    }
    for (a = 0; a < N2; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(creal(Y[a]), cimag(Y[a])));
    }
    free(X);
    free(Y);
    return y;
}

struct _hilbert_backward_struct
{
    float complex* k;
};
static struct _hilbert_backward_struct hilbert_backward_struct;

PyDoc_STRVAR(hilbert_backward_setup_doc, "setup for backward hilbert transform");
static PyObject* hilbert_backward_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    size_t nsz = sz * N2;
    float complex* k = (float complex*)malloc(nsz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        if ((j == 0) || (i == 0)) { jin = 0.0; }
        else { jin = 1.0 / (j * i); }
        k[idx] = -pow(jin / tau, -1);
    }
    hilbert_backward_struct.k = k;
    return Py_None;
}

PyDoc_STRVAR(hilbert_backward_doc, "backward hilbert transform");
static PyObject* hilbert_backward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* y = NULL;
    static char* keywords[] = { "y", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &y)) { return NULL; }
    Py_ssize_t N2 = PyList_Size(y);
    Py_ssize_t N = sqrt(N2);
    PyObject* x = PyList_New(N);
    int idx = 0;
    int jdx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    int c = N;
    Py_complex data;
    size_t sz = sizeof(float complex);
    float complex* k = hilbert_backward_struct.k;
    float complex* Y = (float complex*)malloc(N2 * sz);
    float complex* Z = (float complex*)malloc(N2 * sz);
    float complex* X = (float complex*)malloc(N * sz);
    for (a = 0; a < N; ++a)
    {
        X[a] = 0.0;
    }
    for (a = 0; a < N2; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(y, a));
        Y[a] = data.real + (I * data.imag);
        Z[a] = 0.0;
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Z[idx] = Y[idx] * k[idx];
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        jdx = (j * N) + i;
        if (isnan(creal(Z[jdx]))) { c -= 1; }
        else { X[i] += Z[jdx]; }
    }
    #pragma omp parallel for
    for (a = 0; a < N; ++a)
    {
        X[a] /= c;
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(x, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    free(Y);
    free(Z);
    free(X);
    return x;
}

struct _hartley_forward_struct
{
    float complex* k;
};
static struct _hartley_forward_struct hartley_forward_struct;

PyDoc_STRVAR(hartley_forward_setup_doc, "setup for forward hartley transform");
static PyObject* hartley_forward_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    size_t nsz = sz * N2;
    float complex* k = (float complex*)malloc(nsz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = (cos(j * i) + sin(j * i));
        k[idx] = jin / sqrt(tau);
    }
    hartley_forward_struct.k = k;
    return Py_None;
}

PyDoc_STRVAR(hartley_forward_doc, "forward hartley transform");
static PyObject* hartley_forward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N2);
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float complex);
    float complex* k = hartley_forward_struct.k;
    float complex* X = (float complex*)malloc(N * sz);
    float complex* Y = (float complex*)malloc(N2 * sz);
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        Y[a] = 0.0;
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Y[idx] = X[j] * k[idx];
    }
    for (a = 0; a < N2; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(creal(Y[a]), cimag(Y[a])));
    }
    free(X);
    free(Y);
    return y;
}

struct _hartley_backward_struct
{
    float complex* k;
};
static struct _hartley_backward_struct hartley_backward_struct;

PyDoc_STRVAR(hartley_backward_setup_doc, "setup for backward hartley transform");
static PyObject* hartley_backward_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    size_t nsz = sz * N2;
    float complex* k = (float complex*)malloc(nsz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = (cos(j * i) + sin(j * i));
        k[idx] = pow(jin / sqrt(tau), -1);
    }
    hartley_backward_struct.k = k;
    return Py_None;
}

PyDoc_STRVAR(hartley_backward_doc, "backward hartley transform");
static PyObject* hartley_backward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* y = NULL;
    static char* keywords[] = { "y", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &y)) { return NULL; }
    Py_ssize_t N2 = PyList_Size(y);
    Py_ssize_t N = sqrt(N2);
    PyObject* x = PyList_New(N);
    int idx = 0;
    int jdx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float complex);
    float complex* k = hartley_backward_struct.k;
    float complex* Y = (float complex*)malloc(N2 * sz);
    float complex* Z = (float complex*)malloc(N2 * sz);
    float complex* X = (float complex*)malloc(N * sz);
    for (a = 0; a < N; ++a)
    {
        X[a] = 0.0;
    }
    for (a = 0; a < N2; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(y, a));
        Y[a] = data.real + (I * data.imag);
        Z[a] = 0.0;
    }
    #pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Z[idx] = Y[idx] * k[idx];
    }
    #pragma omp parallel for
    for (a = 0; a < N; ++a)
    {
        X[a] = Z[a];
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(x, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    free(Y);
    free(Z);
    free(X);
    return x;
}

static PyMethodDef custom_methods[] = 
{
    { "gauss_filter", (PyCFunction)gauss_filter, METH_VARARGS | METH_KEYWORDS, gauss_filter_doc },
    { "gauss_filter_2d", (PyCFunction)gauss_filter_2d, METH_VARARGS | METH_KEYWORDS, gauss_filter_2d_doc },
    { "fourier_forward_setup", (PyCFunction)fourier_forward_setup, METH_VARARGS | METH_KEYWORDS, fourier_forward_setup_doc },
    { "fourier_forward", (PyCFunction)fourier_forward, METH_VARARGS | METH_KEYWORDS, fourier_forward_doc },
    { "fourier_backward_setup", (PyCFunction)fourier_backward_setup, METH_VARARGS | METH_KEYWORDS, fourier_backward_setup_doc },
    { "fourier_backward", (PyCFunction)fourier_backward, METH_VARARGS | METH_KEYWORDS, fourier_backward_doc },
    { "laplace_forward_setup", (PyCFunction)laplace_forward_setup, METH_VARARGS | METH_KEYWORDS, laplace_forward_setup_doc },
    { "laplace_forward", (PyCFunction)laplace_forward, METH_VARARGS | METH_KEYWORDS, laplace_forward_doc },
    { "laplace_backward_setup", (PyCFunction)laplace_backward_setup, METH_VARARGS | METH_KEYWORDS, laplace_backward_setup_doc },
    { "laplace_backward", (PyCFunction)laplace_backward, METH_VARARGS | METH_KEYWORDS, laplace_backward_doc },
    { "hilbert_forward_setup", (PyCFunction)hilbert_forward_setup, METH_VARARGS | METH_KEYWORDS, hilbert_forward_setup_doc },
    { "hilbert_forward", (PyCFunction)hilbert_forward, METH_VARARGS | METH_KEYWORDS, hilbert_forward_doc },
    { "hilbert_backward_setup", (PyCFunction)hilbert_backward_setup, METH_VARARGS | METH_KEYWORDS, hilbert_backward_setup_doc },
    { "hilbert_backward", (PyCFunction)hilbert_backward, METH_VARARGS | METH_KEYWORDS, hilbert_backward_doc },
    { "hartley_forward_setup", (PyCFunction)hartley_forward_setup, METH_VARARGS | METH_KEYWORDS, hartley_forward_setup_doc },
    { "hartley_forward", (PyCFunction)hartley_forward, METH_VARARGS | METH_KEYWORDS, hartley_forward_doc },
    { "hartley_backward_setup", (PyCFunction)hartley_backward_setup, METH_VARARGS | METH_KEYWORDS, hartley_backward_setup_doc },
    { "hartley_backward", (PyCFunction)hartley_backward, METH_VARARGS | METH_KEYWORDS, hartley_backward_doc },
    { NULL, NULL, 0, NULL }
};

static PyObject* CustomError = NULL;

static int custom_module_exec(PyObject* m)
{
    PyModule_AddObject(m, "modes", modes_get());
    return 0;
}

static PyModuleDef_Slot custom_module_slots[] =
{
    { Py_mod_exec, custom_module_exec},
    { 0, NULL },
};

static struct PyModuleDef custom_module =
{
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "filters",
    .m_size = 0,
    .m_slots = custom_module_slots,
    .m_methods = custom_methods,
};

PyMODINIT_FUNC PyInit_filters()
{
    return PyModuleDef_Init(&custom_module);
}