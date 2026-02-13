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
    PyDict_SetItem(modes, PyUnicode_FromString("HADAMARD"), PyLong_FromLong(5));
    PyDict_SetItem(modes, PyUnicode_FromString("GAUSS"), PyLong_FromLong(6));
    return modes;
}

PyDoc_STRVAR(gauss_doc, "gauss transform");
static PyObject* gauss(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    PyObject* eq = NULL;
    static char* keywords[] = { "n", "eq", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &n, &eq)) { return NULL; }
    Py_ssize_t N = PyLong_AsLong(n);
    PyObject* y = PyList_New(N);
    float c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float f = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("f")));
    float q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    f *= N;
    float X = 0.0;
    float factor = 0.0;
    int idx = 0;
    for (Py_ssize_t i = 0; i < N; ++i)
    {
        X = ((float)i);
        if (i > N / 2) { X = (N - i); }
        factor = (pow(c, (-abs(pow(X - f, b)) / q)) * g) + l;
        PyList_SetItem(y, i, PyFloat_FromDouble(factor));
    }
    return y;
}

PyDoc_STRVAR(hadamard_doc, "hadamard transform");
static PyObject* hadamard(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    PyObject* eq = NULL;
    static char* keywords[] = { "x", "eq", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &x, &eq)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    if (N & (N - 1) != 0) { PyErr_SetString(PyExc_AssertionError, "length must be a power of 2"); return NULL; }
    int i = 0;
    int j = 0;
    int a = 0;
    int h = 0;
    float complex A = 0;
    float complex B = 0;
    Py_complex data = {};
    PyObject* y = PyList_New(N);
    float complex k = 0;
    Py_ssize_t sz = sizeof(k);
    float complex* X = (float complex*)malloc(N * sz);
    float eq_c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float eq_b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float eq_f = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("f")));
    float eq_q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float eq_g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float eq_l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    float eq_p = 0.0;
    eq_f *= N;
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    //#pragma omp parallel //!!! BUG: while loops halt indefinitely when enabled!
    {
        h = 1;
        //#pragma omp while ordered
        while (h < N)
        {
            #pragma omp for ordered
            for (i = 0; i < N; i += h * 2)
            {
                //#pragma omp for
                for (j = i; j < i + h; ++j)
                {
                    A = X[j];
                    B = X[j + h];
                    X[j] = A + B;
                    X[j + h] = A - B;
                }
            }
            #pragma omp for
            for (i = 0; i < N; ++i) { X[i] /= sqrt(2); }
            h *= 2;
        }
        #pragma omp for
        for (i = 0; i < N; ++i)
        {
            eq_p = ((float)i);
            if (i > N / 2) { eq_p = (N - i); }
            X[i] *= ((pow(eq_c, (-abs(pow(eq_p - eq_f, eq_b)) / eq_q)) * eq_g) + eq_l);
        }
        h = 1;
        //#pragma omp while ordered
        while (h < N)
        {
            #pragma omp for ordered
            for (i = 0; i < N; i += h * 2)
            {
                //#pragma omp for
                for (j = i; j < i + h; ++j)
                {
                    A = X[j];
                    B = X[j + h];
                    X[j] = A + B;
                    X[j + h] = A - B;
                }
            }
            #pragma omp for
            for (i = 0; i < N; ++i) { X[i] /= sqrt(2); }
            h *= 2;
        }
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    free(X);
    return y;
}

struct _fourier_struct
{
    float complex* K1;
    float complex* K2;
    float complex* X;
    float complex* Y;
    float complex* Z;
};
static struct _fourier_struct fourier_struct;

PyDoc_STRVAR(fourier_setup_doc, "setup for fourier transform");
static PyObject* fourier_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    float complex* K1 = (float complex*)malloc(N2 * sz);
    float complex* K2 = (float complex*)malloc(N2 * sz);
    float complex* X = (float complex*)malloc(N * sz);
    float complex* Y = (float complex*)malloc(N2 * sz);
    float complex* Z = (float complex*)malloc(N * sz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    //#pragma omp parallel for //!!! BUG: calculation errors occur when enabled!
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = (-I * tau * j * i) / N;
        K1[idx] = cexp(jin);
        //K2[idx] = pow(K1[idx], -1); //!!! BUG: incorrect results for float complex!
        K2[idx] = cpowf(K1[idx], -1);
    }
    fourier_struct.K1 = K1;
    fourier_struct.K2 = K2;
    fourier_struct.X = X;
    fourier_struct.Y = Y;
    fourier_struct.Z = Z;
    return Py_None;
}

PyDoc_STRVAR(fourier_doc, "fourier transform");
static PyObject* fourier(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    PyObject* eq = NULL;
    static char* keywords[] = { "x", "eq", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &x, &eq)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    int idx = 0;
    int jdx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data = {};
    float complex* K1 = fourier_struct.K1;
    float complex* K2 = fourier_struct.K2;
    float complex* X = fourier_struct.X;
    float complex* Y = fourier_struct.Y;
    float complex* Z = fourier_struct.Z;
    PyObject* result = PyList_New(N);
    float eq_c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float eq_b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float eq_f = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("f")));
    float eq_q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float eq_g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float eq_l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    float eq_p = 0.0;
    eq_f *= N;
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    #pragma omp parallel
    {
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            Y[a] = 0.0;
        }
        #pragma omp for
        for (a = 0; a < N; ++a)
        {
            Z[a] = 0.0;
        }
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            i = a / N;
            j = a - (i * N);
            idx = (i * N) + j;
            eq_p = ((float)i);
            if (i > N / 2) { eq_p = (N - i); }
            Y[idx] = X[j] * K1[idx];
            Z[i] += Y[idx] * ((pow(eq_c, (-abs(pow(eq_p - eq_f, eq_b)) / eq_q)) * eq_g) + eq_l);
            //Y[idx] = Z[j] * K2[idx] * (1.0 / N);
        }
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            i = a / N;
            j = a - (i * N);
            idx = (i * N) + j;
            Y[idx] = Z[j] * K2[idx] * (1.0 / N);
        }
        #pragma omp for
        for (a = 0; a < N; ++a)
        {
            X[a] = 0.0;
        }
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            i = a / N;
            j = a - (i * N);
            idx = (i * N) + j;
            X[i] += Y[idx];
        }
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(result, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    return result;
}

struct _laplace_struct
{
    float complex* K1;
    float complex* K2;
    float complex* X;
    float complex* Y;
    float complex* Z;
};
static struct _laplace_struct laplace_struct;

PyDoc_STRVAR(laplace_setup_doc, "setup for laplace transform");
static PyObject* laplace_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    float complex* K1 = (float complex*)malloc(N2 * sz);
    float complex* K2 = (float complex*)malloc(N2 * sz);
    float complex* X = (float complex*)malloc(N * sz);
    float complex* Y = (float complex*)malloc(N2 * sz);
    float complex* Z = (float complex*)malloc(N2 * sz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    //#pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        //jin = -(j * i) / N; //!!! BUG: overflow error from 85:95 in K2!
        jin = -(j * i) / N2;
        K1[idx] = cexp(jin);
        //K2[idx] = pow(K1[idx], -1);
        K2[idx] = cpowf(K1[idx], -1);
    }
    laplace_struct.K1 = K1;
    laplace_struct.K2 = K2;
    laplace_struct.X = X;
    laplace_struct.Y = Y;
    laplace_struct.Z = Z;
    return Py_None;
}

PyDoc_STRVAR(laplace_doc, "laplace transform");
static PyObject* laplace(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    PyObject* eq = NULL;
    PyObject* mode = NULL;
    static char* keywords[] = { "x", "eq", "mode", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|O", keywords, &x, &eq, &mode)) { return NULL; }
    int _mode = 0; if (mode != NULL) { _mode = PyLong_AsLong(mode); }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    int idx = 0;
    int jdx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data = {};
    float complex* K1 = laplace_struct.K1;
    float complex* K2 = laplace_struct.K2;
    float complex* X = laplace_struct.X;
    float complex* Y = laplace_struct.Y;
    float complex* Z = laplace_struct.Z;
    PyObject* result = PyList_New(N);
    float eq_c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float eq_b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float eq_f = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("f")));
    float eq_q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float eq_g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float eq_l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    float eq_p = 0.0;
    eq_f *= N;
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    #pragma omp parallel
    {
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            Y[a] = 0.0;
            Z[a] = 0.0;
        }
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            i = a / N;
            j = a - (i * N);
            idx = (i * N) + j;
            eq_p = ((float)i);
            if (i > N / 2) { eq_p = (N - i); }
            Y[idx] = X[j] * K1[idx];
            if (_mode == 1)
            {
                Z[j] = Y[idx] * ((pow(eq_c, (-abs(pow(eq_p - eq_f, eq_b)) / eq_q)) * eq_g) + eq_l);
            }
            else
            {
                Z[idx] = Y[idx] * K2[idx] * ((pow(eq_c, (-abs(pow(eq_p - eq_f, eq_b)) / eq_q)) * eq_g) + eq_l);
            }
        }
        if (_mode == 1)
        {
            #pragma omp for
            for (a = 0; a < N2; ++a)
            {
                i = a / N;
                j = a - (i * N);
                idx = (i * N) + j;
                Y[idx] = Z[j] * K2[idx] * (1.0 / N);
            }
            #pragma omp for
            for (a = 0; a < N; ++a)
            {
                X[a] = 0.0;
            }
            #pragma omp for
            for (a = 0; a < N2; ++a)
            {
                i = a / N;
                j = a - (i * N);
                idx = (i * N) + j;
                X[i] += Y[idx];
            }
        }
        else
        {
            #pragma omp for
            for (a = 0; a < N; ++a)
            {
                X[a] = 0.0;
            }
            #pragma omp for
            for (a = 0; a < N2; ++a)
            {
                i = a / N;
                j = a - (i * N);
                jdx = (j * N) + i;
                X[i] += Z[jdx] * (1.0 / N);
            }
        }
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(result, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    return result;
}

struct _hilbert_struct
{
    float complex* K1;
    float complex* K2;
    float complex* X;
    float complex* Y;
    float complex* Z;
};
static struct _hilbert_struct hilbert_struct;

PyDoc_STRVAR(hilbert_setup_doc, "setup for hilbert transform");
static PyObject* hilbert_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    float complex* K1 = (float complex*)malloc(N2 * sz);
    float complex* K2 = (float complex*)malloc(N2 * sz);
    float complex* X = (float complex*)malloc(N * sz);
    float complex* Y = (float complex*)malloc(N2 * sz);
    float complex* Z = (float complex*)malloc(N2 * sz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    //#pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        if ((j == 0) || (i == 0)) { jin = 0.0; }
        else { jin = 1.0 / (j * i); }
        K1[idx] = jin / tau;
        K2[idx] = cpowf(K1[idx], -1);
    }
    hilbert_struct.K1 = K1;
    hilbert_struct.K2 = K2;
    hilbert_struct.X = X;
    hilbert_struct.Y = Y;
    hilbert_struct.Z = Z;
    return Py_None;
}

PyDoc_STRVAR(hilbert_doc, "hilbert transform");
static PyObject* hilbert(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    PyObject* eq = NULL;
    static char* keywords[] = { "x", "eq", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &x, &eq)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    int idx = 0;
    int jdx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    int c = 0;
    Py_complex data = {};
    float complex* K1 = hilbert_struct.K1;
    float complex* K2 = hilbert_struct.K2;
    float complex* X = hilbert_struct.X;
    float complex* Y = hilbert_struct.Y;
    float complex* Z = hilbert_struct.Z;
    PyObject* result = PyList_New(N);
    float eq_c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float eq_b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float eq_f = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("f")));
    float eq_q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float eq_g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float eq_l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    float eq_p = 0.0;
    eq_f *= N;
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    #pragma omp parallel
    {
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            Y[a] = 0.0;
            Z[a] = 0.0;
        }
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            i = a / N;
            j = a - (i * N);
            idx = (i * N) + j;
            eq_p = ((float)i);
            if (i > N / 2) { eq_p = (N - i); }
            Y[idx] = X[j] * K1[idx];
            Z[idx] = Y[idx] * K2[idx] * ((pow(eq_c, (-abs(pow(eq_p - eq_f, eq_b)) / eq_q)) * eq_g) + eq_l);
        }
        #pragma omp for
        for (a = 0; a < N; ++a)
        {
            X[a] = 0.0;
        }
    }
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        jdx = (j * N) + i;
        if (j == 0) { c = N; }
        if (isnan(creal(Z[jdx]))) { --c; }
        else { X[i] += Z[jdx]; }
        if (j == N - 1)
        {
            if (c > 0) { X[i] /= c; }
            else { X[i] = 0.0; }
        }
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(result, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    return result;
}

struct _hartley_struct
{
    float complex* K1;
    float complex* K2;
    float complex* X;
    float complex* Y;
    float complex* Z;
};
static struct _hartley_struct hartley_struct;

PyDoc_STRVAR(hartley_setup_doc, "setup for hartley transform");
static PyObject* hartley_setup(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    float tau = (float)6.283185307179586;
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    size_t sz = sizeof(float complex);
    float complex* K1 = (float complex*)malloc(N2 * sz);
    float complex* K2 = (float complex*)malloc(N2 * sz);
    float complex* X = (float complex*)malloc(N * sz);
    float complex* Y = (float complex*)malloc(N2 * sz);
    float complex* Z = (float complex*)malloc(N2 * sz);
    float complex jin = 0.0;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    //#pragma omp parallel for
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = (cos(j * i) + sin(j * i));
        K1[idx] = jin / sqrt(tau);
        K2[idx] = cpowf(K1[idx], -1);
    }
    hartley_struct.K1 = K1;
    hartley_struct.K2 = K2;
    hartley_struct.X = X;
    hartley_struct.Y = Y;
    hartley_struct.Z = Z;
    return Py_None;
}

PyDoc_STRVAR(hartley_doc, "hartley transform");
static PyObject* hartley(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    PyObject* eq = NULL;
    static char* keywords[] = { "x", "eq", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &x, &eq)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    int idx = 0;
    int jdx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data = {};
    float complex* K1 = hartley_struct.K1;
    float complex* K2 = hartley_struct.K2;
    float complex* X = hartley_struct.X;
    float complex* Y = hartley_struct.Y;
    float complex* Z = hartley_struct.Z;
    PyObject* result = PyList_New(N);
    float eq_c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float eq_b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float eq_f = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("f")));
    float eq_q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float eq_g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float eq_l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    float eq_p = 0.0;
    eq_f *= N;
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        X[a] = data.real + (I * data.imag);
    }
    #pragma omp parallel
    {
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            Y[a] = 0.0;
            Z[a] = 0.0;
        }
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            i = a / N;
            j = a - (i * N);
            idx = (i * N) + j;
            eq_p = ((float)i);
            if (i > N / 2) { eq_p = (N - i); }
            Y[idx] = X[j] * K1[idx];
            Z[idx] = Y[idx] * K2[idx] * ((pow(eq_c, (-abs(pow(eq_p - eq_f, eq_b)) / eq_q)) * eq_g) + eq_l);
        }
        #pragma omp for
        for (a = 0; a < N; ++a)
        {
            X[a] = 0.0;
        }
        #pragma omp for
        for (a = 0; a < N2; ++a)
        {
            i = a / N;
            j = a - (i * N);
            jdx = (j * N) + i;
            X[i] += Z[jdx] * (1.0 / N);
        }
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(result, a, PyComplex_FromDoubles(creal(X[a]), cimag(X[a])));
    }
    return result;
}

static PyMethodDef custom_methods[] = 
{
    { "gauss", (PyCFunction)gauss, METH_VARARGS | METH_KEYWORDS, gauss_doc },
    { "hadamard", (PyCFunction)hadamard, METH_VARARGS | METH_KEYWORDS, hadamard_doc },
    { "fourier_setup", (PyCFunction)fourier_setup, METH_VARARGS | METH_KEYWORDS, fourier_setup_doc },
    { "fourier", (PyCFunction)fourier, METH_VARARGS | METH_KEYWORDS, fourier_doc },
    { "laplace_setup", (PyCFunction)laplace_setup, METH_VARARGS | METH_KEYWORDS, laplace_setup_doc },
    { "laplace", (PyCFunction)laplace, METH_VARARGS | METH_KEYWORDS, laplace_doc },
    { "hilbert_setup", (PyCFunction)hilbert_setup, METH_VARARGS | METH_KEYWORDS, hilbert_setup_doc },
    { "hilbert", (PyCFunction)hilbert, METH_VARARGS | METH_KEYWORDS, hilbert_doc },
    { "hartley_setup", (PyCFunction)hartley_setup, METH_VARARGS | METH_KEYWORDS, hartley_setup_doc },
    { "hartley", (PyCFunction)hartley, METH_VARARGS | METH_KEYWORDS, hartley_doc },
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