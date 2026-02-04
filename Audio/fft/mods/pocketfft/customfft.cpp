#include <cstdio>
#include <cmath>
#include <vector>
#include <complex>
#include <chrono>
#include <cstring>
using namespace std;

vector<complex<float>> fft(vector<complex<float>> x)
{
    int N = x.size();
    complex<float> K;
    float jin = 0.0;
    float tau = 2.0 * M_PI;
    vector<complex<float>> y(N, 0);
    for (int i = 0; i < N; ++i)
    {
        for (int j = 0; j < N; ++j)
        {
            jin = (tau * j * i) / N;
            K = complex<float>(cos(jin), -sin(jin));
            y[i] += x[j] * K;
        }
    }
    return y;
}

vector<complex<float>> ifft(vector<complex<float>> y)
{
    int N = y.size();
    float D = (1.0 / N);
    complex<float> K;
    float jin = 0.0;
    float tau = 2.0 * M_PI;
    vector<complex<float>> x(N, 0);
    for (int i = 0; i < N; ++i)
    {
        for (int j = 0; j < N; ++j)
        {
            jin = (tau * j * i) / N;
            K = complex<float>(cos(jin), sin(jin));
            x[i] += y[j] * K * D;
        }
    }
    return x;
}

int main()
{
    string xstr = "[";
    string ystr = "[";
    string zstr = "[";
    char buffer[255] = "";

    int N = 7; // pow(2, 20) - 1;
    vector<complex<float>> x(N, 0);
    vector<complex<float>> y(N, 0);
    vector<complex<float>> z(N, 0);

    for (int i = 0; i < N; ++i)
    {
        x[i] = i;
        y[i] = 0.0;
        z[i] = 0.0;
    }

    chrono::time_point<chrono::steady_clock> t1 = chrono::steady_clock::now();
    y = fft(x);
    z = ifft(y);
    chrono::time_point<chrono::steady_clock> t2 = chrono::steady_clock::now();
    chrono::duration<float> t = t2 - t1;
    printf("%s %f %s\n", "customfft", t.count(), "seconds");
    if (N > 10) { goto exit; }

    for (int i = 0; i < N; ++i)
    {
        sprintf(buffer, "(%f %f)", x[i].real(), x[i].imag());
        xstr += buffer;
        sprintf(buffer, "(%f %f)", y[i].real(), y[i].imag());
        ystr += buffer;
        sprintf(buffer, "(%f %f)", z[i].real(), z[i].imag());
        zstr += buffer;
        if (i < (N - 1))
        {
            xstr += ", ";
            ystr += ", ";
            zstr += ", ";
        }
    }
    xstr += "]";
    ystr += "]";
    zstr += "]";
    printf("%s\n%s\n%s\n", xstr.c_str(), ystr.c_str(), zstr.c_str());
exit:
    return 0;
}