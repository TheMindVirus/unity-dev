#include <Python.h>
#include <omp.h>

static PyObject* modes_get()
{
    PyObject* modes = PyDict_New();
    PyDict_SetItem(modes, PyUnicode_FromString("NULL"), PyLong_FromLong(0));
    PyDict_SetItem(modes, PyUnicode_FromString("FOURIER"), PyLong_FromLong(1));
    PyDict_SetItem(modes, PyUnicode_FromString("LAPLACIAN"), PyLong_FromLong(2));
    return modes;
}

PyDoc_STRVAR(gauss_filter_doc, "gauss filter transform");
static PyObject* gauss_filter(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    PyObject* eq = NULL;
    static char* keywords[] = { "x", "eq", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &x, &eq)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    PyObject* y = PyList_New(N);
    float c = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("c")));
    float f = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("f")));
    float b = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("b")));
    float q = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("q")));
    float g = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("g")));
    float l = (float)PyFloat_AsDouble(PyDict_GetItem(eq, PyUnicode_FromString("l")));
    Py_complex data = PyComplex_AsCComplex(PyList_GetItem(x, 0));
    PyList_SetItem(y, 0, PyComplex_FromDoubles(data.real, data.imag));
    float p = 0.0;
    float factor = 0.0;
    for (Py_ssize_t i = 1; i < N; ++i)
    {
        p = ((float)i);
        if (i > N / 2) { p = (N - i); }
        data = PyComplex_AsCComplex(PyList_GetItem(x, i));
        factor = (pow(c, -abs(pow(p - f, b)) / q) * g) + l;
        data.real = (data.real * factor) - (data.imag * 0);
        data.imag = (data.real * 0) + (data.imag * factor);
        PyList_SetItem(y, i, PyComplex_FromDoubles(data.real, data.imag));
    }
    return y;
}

PyDoc_STRVAR(fourier_forward_doc, "forward fourier transform");
static PyObject* fourier_forward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N);
    float Kr = 0.0;
    float Ki = 0.0;
    float tau = 6.283185307179586;
    float jin = 0.0;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float);
    float* Xr = (float*)malloc(N * sz);
    float* Xi = (float*)malloc(N * sz);
    float* Yr = (float*)malloc(N * sz);
    float* Yi = (float*)malloc(N * sz);

    //struct timespec t1;
    //struct timespec t2;
    //float dur = 0.0;
    char buffer[255] = "";
    //clock_gettime(CLOCK_MONOTONIC, &t1);

    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        Xr[a] = data.real;
        Xi[a] = data.imag;
        Yr[a] = 0.0;
        Yi[a] = 0.0;
    }

    //clock_gettime(CLOCK_MONOTONIC, &t2);
    //dur = (t2.tv_sec + t2.tv_nsec * 1e-9) - (t1.tv_sec + t1.tv_nsec * 1e-9);
    //sprintf(buffer, "%f", dur);
    //PySys_WriteStdout("%s: %s\n", "Load in", buffer);
    //clock_gettime(CLOCK_MONOTONIC, &t1);

    //PyGILState_STATE state = PyGILState_Ensure();
    //Py_BEGIN_ALLOW_THREADS
    //sprintf(buffer, "max: %d", omp_get_max_threads());
    //PySys_WriteStdout("%s\n", buffer);

    #pragma omp parallel for ordered num_threads(256) //reduction(+ : Yr[i])
    for (a = 0; a < N2; ++a)
    {
        if (omp_get_thread_num() >= 0)
        {
            i = (int)(a / N);
            j = a - (i * N);
            jin = (tau * j * i) / N;
            Kr = cos(jin);
            Ki = -sin(jin);
            Yr[i] = Yr[i] + ((Xr[j] * Kr) - (Xi[j] * Ki));
            Yi[i] = Yi[i] + ((Xr[j] * Ki) + (Xi[j] * Kr));
        }
    }

    //clock_gettime(CLOCK_MONOTONIC, &t2);
    //dur = (t2.tv_sec + t2.tv_nsec * 1e-9) - (t1.tv_sec + t1.tv_nsec * 1e-9);
    //sprintf(buffer, "%f", dur);
    //PySys_WriteStdout("%s: %s\n", "Process", buffer);
    //clock_gettime(CLOCK_MONOTONIC, &t1);

    //Py_END_ALLOW_THREADS
    //PyGILState_Release(state);
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(Yr[a], Yi[a]));
    }

    //clock_gettime(CLOCK_MONOTONIC, &t2);
    //dur = (t2.tv_sec + t2.tv_nsec * 1e-9) - (t1.tv_sec + t1.tv_nsec * 1e-9);
    //sprintf(buffer, "%f", dur);
    //PySys_WriteStdout("%s: %s\n", "Load out", buffer);

    free(Xr);
    free(Xi);
    free(Yr);
    free(Yi);
    return y;
}

PyDoc_STRVAR(fourier_backward_doc, "backward fourier transform");
static PyObject* fourier_backward(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* y = NULL;
    static char* keywords[] = { "y", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &y)) { return NULL; }
    Py_ssize_t N = PyList_Size(y);
    Py_ssize_t N2 = N * N;
    PyObject* x = PyList_New(N);
    float Kr = 0.0;
    float Ki = 0.0;
    float tau = 6.283185307179586;
    float jin = 0.0;
    float D = 1.0 / N;
    int i = 0;
    int j = 0;
    int a = 0;
    Py_complex data;
    size_t sz = sizeof(float);
    float* Yr = (float*)malloc(N * sz);
    float* Yi = (float*)malloc(N * sz);
    float* Xr = (float*)malloc(N * sz);
    float* Xi = (float*)malloc(N * sz);
    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(y, a));
        Yr[a] = data.real;
        Yi[a] = data.imag;
        Xr[a] = 0.0;
        Xi[a] = 0.0;
    }
    #pragma omp parallel for ordered num_threads(256) 
    for (a = 0; a < N2; ++a)
    {
        if (omp_get_thread_num() >= 0)
        {
            i = (int)(a / N);
            j = a - (i * N);
            jin = (tau * j * i) / N;
            Kr = cos(jin);
            Ki = sin(jin);
            Xr[i] = Xr[i] + (((Yr[j] * Kr) - (Yi[j] * Ki)) * D);
            Xi[i] = Xi[i] + (((Yr[j] * Ki) + (Yi[j] * Kr)) * D);
        }
    }
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(x, a, PyComplex_FromDoubles(Xr[a], Xi[a]));
    }
    free(Yr);
    free(Yi);
    free(Xr);
    free(Xi);
    return x;
}

static PyMethodDef custom_methods[] = 
{
    { "gauss_filter", (PyCFunction)gauss_filter, METH_VARARGS | METH_KEYWORDS, gauss_filter_doc },
    { "fourier_forward", (PyCFunction)fourier_forward, METH_VARARGS | METH_KEYWORDS, fourier_forward_doc },
    { "fourier_backward", (PyCFunction)fourier_backward, METH_VARARGS | METH_KEYWORDS, fourier_backward_doc },
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
    .m_name = "filters2",
    .m_size = 0,
    .m_slots = custom_module_slots,
    .m_methods = custom_methods,
};

PyMODINIT_FUNC PyInit_filters2()
{
    return PyModuleDef_Init(&custom_module);
}