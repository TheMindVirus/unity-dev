#define _hypot hypot
#include <cmath>
#include <complex>
#include <vector>
#include <fstream>
#include <CL/opencl.hpp>
#include <Python.h>
#include <omp.h>
using namespace std;

static complex<float> I = complex<float>(0.0, 1.0);
static float tau = M_PI * 2.0;

static const char* FILENAME = "main.cl";

static vector<cl::Platform> platforms;
static vector<cl::Device> devices;
static int platform = 0;
static int device = 0;

static cl::Context context;
static cl::CommandQueue queue;

static unique_ptr<float[]> X;
static unique_ptr<float[]> Y;
static float* Xr;
static float* Xi;
static float* Yr;
static float* Yi;
static float* Kr1;
static float* Ki1;
static float* Kr2;
static float* Ki2;
static float* Tr;
static float* Ti;
static size_t* Nn;

static cl::Buffer bX;
static cl::Buffer bY;
static cl::Buffer bXr;
static cl::Buffer bXi;
static cl::Buffer bYr;
static cl::Buffer bYi;
static cl::Buffer bKr1;
static cl::Buffer bKi1;
static cl::Buffer bKr2;
static cl::Buffer bKi2;
static cl::Buffer bTr;
static cl::Buffer bTi;
static cl::Buffer bNn;

static ifstream source;
static string code;
static cl::Program::Sources src;

static cl::Program program;
static cl_int result;
static string logs;

static cl::Kernel k_test;
static cl::Kernel k_test_fft;
static cl::Kernel k_test_ifft;
static cl::Kernel k_test_krn_fft;
static cl::Kernel k_test_krn_ifft;

static cl::NDRange Nrange;
static cl::NDRange N2range;

static PyObject* PyExc_OpenCLError;

PyDoc_STRVAR(test_doc, "setup for opencl test");
static PyObject* test(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* n = NULL;
    static char* keywords[] = { "n", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &n)) { return NULL; }
    Py_ssize_t N = PyLong_AsLong(n);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N);
    size_t sz = sizeof(float);
    size_t nsz = N * sz;
    size_t nsz2 = N2 * sz;
    size_t szsz = sizeof(size_t);
    complex<float> jin;
    int idx = 0;
    int i = 0;
    int j = 0;
    int a = 0;
PySys_WriteStdout("[CKPT]: %d\n", 1);
    cl::Platform::get(&platforms);
PySys_WriteStdout("[CKPT]: %f\n", 1.1);
    platforms[platform].getDevices(CL_DEVICE_TYPE_GPU, &devices);
PySys_WriteStdout("[CKPT]: %f\n", 1.2);
    context = cl::Context(devices);
PySys_WriteStdout("[CKPT]: %f\n", 1.3);
    queue = cl::CommandQueue(context, devices[device]);
PySys_WriteStdout("[CKPT]: %d\n", 2);
    X = unique_ptr<float[]>(new float[N]);
    Y = unique_ptr<float[]>(new float[N]);
    Xr = (float*)malloc(nsz);
    Xi = (float*)malloc(nsz);
    Yr = (float*)malloc(nsz);
    Yi = (float*)malloc(nsz);
    Kr1 = (float*)malloc(nsz2);
    Ki1 = (float*)malloc(nsz2);
    Kr2 = (float*)malloc(nsz2);
    Ki2 = (float*)malloc(nsz2);
    Tr = (float*)malloc(nsz2);
    Ti = (float*)malloc(nsz2);
    Nn = (size_t*)malloc(szsz);
    Nn[0] = N;
PySys_WriteStdout("[CKPT]: %d\n", 3);
    for (a = 0; a < N; ++a)
    {
        X[a] = 0.0;
        Y[a] = 0.0;
        Xr[a] = 0.0;
        Xi[a] = 0.0;
        Yr[a] = 0.0;
        Yi[a] = 0.0;
    }
PySys_WriteStdout("[CKPT]: %d\n", 4);
    for (a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        jin = exp(-I * complex<float>((tau * j * i) / N));
        Kr1[idx] = jin.real();
        Ki1[idx] = jin.imag();
        jin = exp(I * complex<float>((tau * j * i) / N));
        Kr2[idx] = jin.real();
        Ki2[idx] = jin.imag();
        Tr[a] = 0.0;
        Ti[a] = 0.0;
    }
PySys_WriteStdout("[CKPT]: %d\n", 5);
    bX = cl::Buffer(context, CL_MEM_READ_WRITE, nsz);
    bY = cl::Buffer(context, CL_MEM_READ_WRITE, nsz);
    queue.enqueueWriteBuffer(bX, CL_TRUE, 0, nsz, X.get());
    queue.enqueueWriteBuffer(bY, CL_TRUE, 0, nsz, Y.get());
PySys_WriteStdout("[CKPT]: %d\n", 6);
    bXr = cl::Buffer(context, CL_MEM_READ_WRITE, nsz);
    bXi = cl::Buffer(context, CL_MEM_READ_WRITE, nsz);
    bYr = cl::Buffer(context, CL_MEM_READ_WRITE, nsz);
    bYi = cl::Buffer(context, CL_MEM_READ_WRITE, nsz);
    bKr1 = cl::Buffer(context, CL_MEM_READ_WRITE, nsz2);
    bKi1 = cl::Buffer(context, CL_MEM_READ_WRITE, nsz2);
    bKr2 = cl::Buffer(context, CL_MEM_READ_WRITE, nsz2);
    bKi2 = cl::Buffer(context, CL_MEM_READ_WRITE, nsz2);
    bTr = cl::Buffer(context, CL_MEM_READ_WRITE, nsz2);
    bTi = cl::Buffer(context, CL_MEM_READ_WRITE, nsz2);
    bNn = cl::Buffer(context, CL_MEM_READ_WRITE, szsz);
    queue.enqueueWriteBuffer(bXr, CL_TRUE, 0, nsz, Xr);
    queue.enqueueWriteBuffer(bXi, CL_TRUE, 0, nsz, Xi);
    queue.enqueueWriteBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueWriteBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    queue.enqueueWriteBuffer(bKr1, CL_TRUE, 0, nsz2, Kr1);
    queue.enqueueWriteBuffer(bKi1, CL_TRUE, 0, nsz2, Ki1);
    queue.enqueueWriteBuffer(bKr2, CL_TRUE, 0, nsz2, Kr2);
    queue.enqueueWriteBuffer(bKi2, CL_TRUE, 0, nsz2, Ki2);
    queue.enqueueWriteBuffer(bTr, CL_TRUE, 0, nsz2, Tr);
    queue.enqueueWriteBuffer(bTi, CL_TRUE, 0, nsz2, Ti);
    queue.enqueueWriteBuffer(bNn, CL_TRUE, 0, szsz, Nn);
PySys_WriteStdout("[CKPT]: %d\n", 7);
    source = ifstream(FILENAME);
    code = string(istreambuf_iterator<char>(source), istreambuf_iterator<char>());
    src = cl::Program::Sources(1, code.c_str());
PySys_WriteStdout("[CKPT]: %d\n", 8);
    program = cl::Program(context, src);
    result = program.build(devices);
    logs = program.getBuildInfo<CL_PROGRAM_BUILD_LOG>(devices[device]);
    if (result != CL_SUCCESS) { PyErr_SetString(PyExc_OpenCLError, logs.c_str()); return y; }
PySys_WriteStdout("[CKPT]: %d\n", 9);
    k_test = cl::Kernel(program, "test");
    k_test.setArg(0, bX);
    k_test.setArg(1, bY);
PySys_WriteStdout("[CKPT]: %d\n", 10);
    k_test_fft = cl::Kernel(program, "test_fft");
    k_test_fft.setArg(0, bXr);
    k_test_fft.setArg(1, bXi);
    k_test_fft.setArg(2, bKr1);
    k_test_fft.setArg(3, bKi1);
    k_test_fft.setArg(4, bYr);
    k_test_fft.setArg(5, bYi);
PySys_WriteStdout("[CKPT]: %d\n", 11);
    k_test_ifft = cl::Kernel(program, "test_ifft");
    k_test_ifft.setArg(0, bXr);
    k_test_ifft.setArg(1, bXi);
    k_test_ifft.setArg(2, bKr2);
    k_test_ifft.setArg(3, bKi2);
    k_test_ifft.setArg(4, bYr);
    k_test_ifft.setArg(5, bYi);
PySys_WriteStdout("[CKPT]: %d\n", 12);
    k_test_krn_fft = cl::Kernel(program, "test_krn_fft");
    k_test_krn_fft.setArg(0, bNn);
    k_test_krn_fft.setArg(1, bXr);
    k_test_krn_fft.setArg(2, bXi);
    k_test_krn_fft.setArg(3, bKr1);
    k_test_krn_fft.setArg(4, bKi1);
    k_test_krn_fft.setArg(5, bTr);
    k_test_krn_fft.setArg(6, bTi);
    k_test_krn_fft.setArg(7, bYr);
    k_test_krn_fft.setArg(8, bYi);
PySys_WriteStdout("[CKPT]: %d\n", 13);
    k_test_krn_ifft = cl::Kernel(program, "test_krn_ifft");
    k_test_krn_ifft.setArg(0, bNn);
    k_test_krn_ifft.setArg(1, bXr);
    k_test_krn_ifft.setArg(2, bXi);
    k_test_krn_ifft.setArg(3, bKr2);
    k_test_krn_ifft.setArg(4, bKi2);
    k_test_krn_ifft.setArg(5, bTr);
    k_test_krn_ifft.setArg(6, bTi);
    k_test_krn_ifft.setArg(7, bYr);
    k_test_krn_ifft.setArg(8, bYi);
PySys_WriteStdout("[CKPT]: %d\n", 14);
    Nrange = cl::NDRange(N);
    N2range = cl::NDRange(N2);
    result = queue.enqueueNDRangeKernel(k_test, cl::NullRange, Nrange, cl::NullRange);
    if (result != CL_SUCCESS) { char buffer[255] = ""; sprintf(buffer, "%d", result); PyErr_SetString(PyExc_OpenCLError, buffer); return y; }
    queue.enqueueReadBuffer(bY, CL_TRUE, 0, nsz, Y.get());
    cl::finish(); ///!!! BUG: Failing to call cl::finish corrupts the buffers for the next calls!
PySys_WriteStdout("[CKPT]: %d\n", 15);
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(y, a, PyFloat_FromDouble(Y[a]));
    }
PySys_WriteStdout("[CKPT]: %d\n", 16);
    return y;
}

PyDoc_STRVAR(test_fft_doc, "setup for opencl fft test");
static PyObject* test_fft(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N);
    size_t sz = sizeof(float);
    size_t nsz = N * sz;
    //size_t nsz2 = N2 * sz;
    Py_complex data;
    int a = 0;

    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        Xr[a] = data.real;
        Xi[a] = data.imag;
        Yr[a] = 0.0;
        Yi[a] = 0.0;
    }

    queue.enqueueWriteBuffer(bXr, CL_TRUE, 0, nsz, Xr);
    queue.enqueueWriteBuffer(bXi, CL_TRUE, 0, nsz, Xi);
    //queue.enqueueWriteBuffer(bKr1, CL_TRUE, 0, nsz2, Kr1);
    //queue.enqueueWriteBuffer(bKi1, CL_TRUE, 0, nsz2, Ki1);
    queue.enqueueWriteBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueWriteBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    result = queue.enqueueNDRangeKernel(k_test_fft, cl::NullRange, Nrange, cl::NullRange);
    if (result != CL_SUCCESS) { char buffer[255] = ""; sprintf(buffer, "%d", result); PyErr_SetString(PyExc_OpenCLError, buffer); return y; }
    queue.enqueueReadBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueReadBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    cl::finish();
    
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(Yr[a], Yi[a]));
    }

    return y;
}

PyDoc_STRVAR(test_ifft_doc, "setup for opencl ifft test");
static PyObject* test_ifft(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N);
    size_t sz = sizeof(float);
    size_t nsz = N * sz;
    //size_t nsz2 = N2 * sz;
    Py_complex data;
    int a = 0;

    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        Xr[a] = data.real;
        Xi[a] = data.imag;
        Yr[a] = 0.0;
        Yi[a] = 0.0;
    }
    
    queue.enqueueWriteBuffer(bXr, CL_TRUE, 0, nsz, Xr);
    queue.enqueueWriteBuffer(bXi, CL_TRUE, 0, nsz, Xi);
    //queue.enqueueWriteBuffer(bKr2, CL_TRUE, 0, nsz2, Kr2);
    //queue.enqueueWriteBuffer(bKi2, CL_TRUE, 0, nsz2, Ki2);
    queue.enqueueWriteBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueWriteBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    result = queue.enqueueNDRangeKernel(k_test_ifft, cl::NullRange, Nrange, cl::NullRange);
    if (result != CL_SUCCESS) { char buffer[255] = ""; sprintf(buffer, "%d", result); PyErr_SetString(PyExc_OpenCLError, buffer); return y; }
    queue.enqueueReadBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueReadBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    cl::finish();
    
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(Yr[a], Yi[a]));
    }

    return y;
}

PyDoc_STRVAR(test_krn_fft_doc, "setup for opencl krn fft test");
static PyObject* test_krn_fft(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N);
    size_t sz = sizeof(float);
    size_t nsz = N * sz;
    size_t nsz2 = N2 * sz;
    size_t szsz = sizeof(size_t);
    Py_complex data;
    int a = 0;

    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        Xr[a] = data.real;
        Xi[a] = data.imag;
        Yr[a] = 0.0;
        Yi[a] = 0.0;
    }
    
    queue.enqueueWriteBuffer(bNn, CL_TRUE, 0, szsz, Nn);
    queue.enqueueWriteBuffer(bXr, CL_TRUE, 0, nsz, Xr);
    queue.enqueueWriteBuffer(bXi, CL_TRUE, 0, nsz, Xi);
    //queue.enqueueWriteBuffer(bKr1, CL_TRUE, 0, nsz2, Kr1);
    //queue.enqueueWriteBuffer(bKi1, CL_TRUE, 0, nsz2, Ki1);
    queue.enqueueWriteBuffer(bTr, CL_TRUE, 0, nsz2, Tr);
    queue.enqueueWriteBuffer(bTi, CL_TRUE, 0, nsz2, Ti);
    queue.enqueueWriteBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueWriteBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    result = queue.enqueueNDRangeKernel(k_test_krn_fft, cl::NullRange, N2range, cl::NullRange);
    if (result != CL_SUCCESS) { char buffer[255] = ""; sprintf(buffer, "%d", result); PyErr_SetString(PyExc_OpenCLError, buffer); return y; }
    queue.enqueueReadBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueReadBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    cl::finish();
    
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(Yr[a], Yi[a]));
    }

    return y;
}

PyDoc_STRVAR(test_krn_ifft_doc, "setup for opencl krn ifft test");
static PyObject* test_krn_ifft(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* x = NULL;
    static char* keywords[] = { "x", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &x)) { return NULL; }
    Py_ssize_t N = PyList_Size(x);
    Py_ssize_t N2 = N * N;
    PyObject* y = PyList_New(N);
    size_t sz = sizeof(float);
    size_t nsz = N * sz;
    size_t nsz2 = N2 * sz;
    size_t szsz = sizeof(size_t);
    Py_complex data;
    int a = 0;

    for (a = 0; a < N; ++a)
    {
        data = PyComplex_AsCComplex(PyList_GetItem(x, a));
        Xr[a] = data.real;
        Xi[a] = data.imag;
        Yr[a] = 0.0;
        Yi[a] = 0.0;
    }
    
    queue.enqueueWriteBuffer(bNn, CL_TRUE, 0, szsz, Nn);
    queue.enqueueWriteBuffer(bXr, CL_TRUE, 0, nsz, Xr);
    queue.enqueueWriteBuffer(bXi, CL_TRUE, 0, nsz, Xi);
    //queue.enqueueWriteBuffer(bKr2, CL_TRUE, 0, nsz2, Kr2);
    //queue.enqueueWriteBuffer(bKi2, CL_TRUE, 0, nsz2, Ki2);
    queue.enqueueWriteBuffer(bTr, CL_TRUE, 0, nsz2, Tr);
    queue.enqueueWriteBuffer(bTi, CL_TRUE, 0, nsz2, Ti);
    queue.enqueueWriteBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueWriteBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    result = queue.enqueueNDRangeKernel(k_test_krn_ifft, cl::NullRange, N2range, cl::NullRange);
    if (result != CL_SUCCESS) { char buffer[255] = ""; sprintf(buffer, "%d", result); PyErr_SetString(PyExc_OpenCLError, buffer); return y; }
    queue.enqueueReadBuffer(bYr, CL_TRUE, 0, nsz, Yr);
    queue.enqueueReadBuffer(bYi, CL_TRUE, 0, nsz, Yi);
    cl::finish();
    
    for (a = 0; a < N; ++a)
    {
        PyList_SetItem(y, a, PyComplex_FromDoubles(Yr[a], Yi[a]));
    }

    return y;
}

static PyMethodDef custom_methods[] = 
{
    { "test", (PyCFunction)test, METH_VARARGS | METH_KEYWORDS, test_doc },
    { "test_fft", (PyCFunction)test_fft, METH_VARARGS | METH_KEYWORDS, test_fft_doc },
    { "test_ifft", (PyCFunction)test_ifft, METH_VARARGS | METH_KEYWORDS, test_ifft_doc },
    { "test_krn_fft", (PyCFunction)test_krn_fft, METH_VARARGS | METH_KEYWORDS, test_krn_fft_doc },
    { "test_krn_ifft", (PyCFunction)test_krn_ifft, METH_VARARGS | METH_KEYWORDS, test_krn_ifft_doc },
    { NULL, NULL, 0, NULL }
};

static PyObject* CustomError = NULL;

static int custom_module_exec(PyObject* m)
{
    PyExc_OpenCLError = PyErr_NewException("main.OpenCLError", NULL, NULL);
    return 0;
}

static PyModuleDef_Slot custom_module_slots[] =
{
    { Py_mod_exec, (void*)custom_module_exec},
    { 0, NULL },
};

static struct PyModuleDef custom_module =
{
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "main",
    .m_size = 0,
    .m_methods = custom_methods,
    .m_slots = custom_module_slots,
};

PyMODINIT_FUNC PyInit_main()
{
    return PyModuleDef_Init(&custom_module);
}