#include <complex.h>
#include <math.h>

#define export __declspec(dllexport)
#define byte char
#define ubyte unsigned byte
#define pi M_PI

union complex_union
{
    ubyte raw[8];
    complex float data;
    struct { float real; float imag; };
};

struct complex2
{
    float real;
    float imag;
};

union complex2_union
{
    ubyte* raw;
    complex float* data;
    struct complex2* data2;
};

struct complex_data
{
    int n;
    ubyte* data;
};

struct __complex_data
{
    int n;
    complex float* data;
};

export complex float cmul(complex float A, complex float B)
{
    union complex_union C = {0};
    float a = creal(A);
    float b = cimag(A);
    float c = creal(B);
    float d = cimag(B);
    C.real = (a * c) - (b * d);
    C.imag = (a * d) + (b * c);
    return C.data;
}

export struct complex_data* integrate(struct complex_data* params, struct complex_data* result);
export struct __complex_data* __integrate(struct __complex_data* X, struct __complex_data* Y);

export struct complex_data* differentiate(struct complex_data* params, struct complex_data* result);
export struct __complex_data* __differentiate(struct __complex_data* Y, struct __complex_data* X);

export struct complex_data* convolute(struct complex_data* params, struct complex_data* result);
export struct __complex_data* __convolute(struct __complex_data* X, struct __complex_data* Y);

export struct complex_data* unwind(struct complex_data* params, struct complex_data* result);
export struct __complex_data* __unwind(struct __complex_data* Y, struct __complex_data* X);

export struct complex_data* integrate(struct complex_data* params, struct complex_data* result)
{
    struct __complex_data x;
    struct __complex_data y;
    complex float x_data[params->n];
    complex float y_data[params->n];
    union complex2_union ux = {0};
    union complex2_union uy = {0};
    
    x.data = x_data;
    y.data = y_data;

    ux.raw = params->data;
    x.data = ux.data;

    x.n = params->n;
    y = *__integrate(&x, &y);
    result->n = y.n;

    uy.data = y.data;
    result->data = uy.raw;

    return result;
}

export struct __complex_data* __integrate(struct __complex_data* X, struct __complex_data* Y)
{
    int N = X->n;

    Y->data[0] = X->data[0];
    for (int i = 1; i < N; ++i)
    {
        Y->data[i] = X->data[i - 1] + (0.5 * (X->data[i] - X->data[i - 1]));
    }

    Y->n = N;
    return Y;
}

export struct complex_data* differentiate(struct complex_data* params, struct complex_data* result)
{
    struct __complex_data y;
    struct __complex_data x;
    complex float y_data[params->n];
    complex float x_data[params->n];
    union complex2_union uy = {0};
    union complex2_union ux = {0};
    
    y.data = y_data;
    x.data = x_data;

    uy.raw = params->data;
    y.data = uy.data;

    y.n = params->n;
    x = *__differentiate(&y, &x);
    result->n = x.n;

    ux.data = x.data;
    result->data = ux.raw;

    return result;
}

export struct __complex_data* __differentiate(struct __complex_data* Y, struct __complex_data* X)
{
    int N = Y->n;

    X->data[0] = Y->data[0];
    for (int i = 1; i < N; ++i)
    {
        X->data[i] = (2.0 * Y->data[i]) - X->data[i - 1];
    }

    X->n = N;
    return X;
}

export struct complex_data* convolute(struct complex_data* params, struct complex_data* result)
{
    struct __complex_data x;
    struct __complex_data y;
    complex float x_data[params->n];
    complex float y_data[params->n];
    union complex2_union ux = {0};
    union complex2_union uy = {0};
    
    x.data = x_data;
    y.data = y_data;

    ux.raw = params->data;
    x.data = ux.data;

    x.n = params->n;
    y = *__convolute(&x, &y);
    result->n = y.n;

    uy.data = y.data;
    result->data = uy.raw;

    return result;
}

export struct __complex_data* __convolute(struct __complex_data* X, struct __complex_data* Y)
{
    int N = X->n;
    float tau = 2.0 * pi;
    float jin = 0.0;
    union complex_union K = {0};

    for (int i = 0; i < N; ++i)
    {
        Y->data[i] = 0.0;
        for (int j = 0; j < N; ++j)
        {
            jin = (tau * j * i) / N;
            K.real = cos(jin);
            K.imag = sin(jin);
            Y->data[i] += cmul(X->data[j], K.data);
        }
    }

    Y->n = N;
    return Y;
}

export struct complex_data* unwind(struct complex_data* params, struct complex_data* result)
{
    struct __complex_data y;
    struct __complex_data x;
    complex float y_data[params->n];
    complex float x_data[params->n];
    union complex2_union uy = {0};
    union complex2_union ux = {0};
    
    y.data = y_data;
    x.data = x_data;

    uy.raw = params->data;
    y.data = uy.data;

    y.n = params->n;
    x = *__unwind(&y, &x);
    result->n = x.n;

    ux.data = x.data;
    result->data = ux.raw;

    return result;
}

export struct __complex_data* __unwind(struct __complex_data* Y, struct __complex_data* X)
{
    int N = Y->n;
    float tau = 2.0 * pi;
    float jin = 0.0;
    float D = 1.0 / N;
    union complex_union K = {0};

    for (int i = 0; i < N; ++i)
    {
        X->data[i] = 0.0;
        for (int j = 0; j < N; ++j)
        {
            jin = (tau * j * i) / N;
            K.real = cos(jin);
            K.imag = -sin(jin);
            X->data[i] += cmul(Y->data[j], K.data) * D;
        }
    }

    X->n = N;
    return X;
}