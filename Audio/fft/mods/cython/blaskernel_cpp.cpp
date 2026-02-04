#include <complex>
#include <math.h>
using namespace std;

#define ubyte unsigned char
#define tau 6.283185307179586

struct complex_data
{
    int n;
    ubyte* data;
};

union complex_union
{
    ubyte raw[8];
    complex<float> data;
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
    complex<float>* data;
    struct complex2* data2;
};

static struct complex_data* fft(struct complex_data* params, struct complex_data* result)
{
    int n = params->n;
    float jin = 0.0;

    union complex_union K = {0};
    union complex_union C = {0};

    union complex2_union x = {0};
    union complex2_union y = {0};

    float a = 0.0;
    float b = 0.0;
    float c = 0.0;
    float d = 0.0;

    int i = 0;
    int j = 0;

    x.data = new complex<float>[n];
    y.data = new complex<float>[n];

    x.raw = params->data;
    for (i = 0; i < n; ++i)
    {
        y.data[i] = 0.0;
        for (j = 0; j < n; ++j)
        {
            jin = (tau * j * i) / n;
            K.real = cos(jin);
            K.imag = -sin(jin);
            a = x.data2[j].real;
            b = x.data2[j].imag;
            c = K.real;
            d = K.imag;
            C.real = (a * c) - (b * d);
            C.imag = (a * d) + (b * c);
            y.data[i] += C.data;
        }
    }

    result->data = y.raw;
    result->n = n;
    return result;
}

static struct complex_data* ifft(struct complex_data* params, struct complex_data* result)
{
    int n = params->n;
    float D = 1.0 / n;
    float jin = 0.0;

    union complex_union K = {0};
    union complex_union C = {0};

    union complex2_union y = {0};
    union complex2_union x = {0};

    float a = 0.0;
    float b = 0.0;
    float c = 0.0;
    float d = 0.0;

    int i = 0;
    int j = 0;

    y.data = new complex<float>[n];
    x.data = new complex<float>[n];

    y.raw = params->data;
    for (i = 0; i < n; ++i)
    {
        x.data[i] = 0.0;
        for (j = 0; j < n; ++j)
        {
            jin = (tau * j * i) / n;
            K.real = cos(jin);
            K.imag = sin(jin);
            a = y.data2[j].real;
            b = y.data2[j].imag;
            c = K.real;
            d = K.imag;
            C.real = (a * c) - (b * d);
            C.imag = (a * d) + (b * c);
            x.data[i] += C.data * D;
        }
    }

    result->data = x.raw;
    result->n = n;
    return result;
}