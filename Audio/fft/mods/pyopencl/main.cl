kernel void test(global float* X, global float* Y)
{
    const int idx = get_global_id(0);
    Y[idx] = idx;
}

kernel void test_fft(global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Yr, global float* Yi)
{
    const int gid = get_global_id(0);
    const int lid = get_local_id(0);
    if ((gid != 0) || (lid != 0)) { return; }

    const int N = get_global_size(0);
    const int N2 = N * N;
    int i = 0;
    int j = 0;
    int idx = 0;
    for (int a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Yr[i] = Yr[i] + ((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx]));
        Yi[i] = Yi[i] + ((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx]));
    }
}

kernel void test_ifft(global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Yr, global float* Yi)
{
    const int gid = get_global_id(0);
    const int lid = get_local_id(0);
    if ((gid != 0) || (lid != 0)) { return; }

    const int N = get_global_size(0);
    const int N2 = N * N;
    int i = 0;
    int j = 0;
    int idx = 0;
    float D = 1.0 / N;
    for (int a = 0; a < N2; ++a)
    {
        i = a / N;
        j = a - (i * N);
        idx = (i * N) + j;
        Yr[i] = Yr[i] + (((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx])) * D);
        Yi[i] = Yi[i] + (((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx])) * D);
    }
}

kernel void test_krn_fft(global int* SZ, global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Tr, global float* Ti, global float* Yr, global float* Yi)
{
    //#pragma disable(local) //!!! BUG: output of function when local work group is set to (1,) is incorrect and with None it is correct!
    int N = SZ[0];
    int a = get_global_id(0);
    int sz = get_global_size(0);
    int i = a / N;
    int j = a - (i * N);
    int idx = (i * N) + j;
    Tr[idx] = ((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx]));
    Ti[idx] = ((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx]));
    barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);
    if (a > N) { return; }
    for (int k = 0; k < N; ++k)
    {
        idx = (a * N) + k;
        Yr[a] += Tr[idx];
        Yi[a] += Ti[idx];
    }
}

kernel void test_krn_ifft(global int* SZ, global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Tr, global float* Ti, global float* Yr, global float* Yi)
{
    //#pragma disable(local)
    int N = SZ[0];
    int a = get_global_id(0);
    int sz = get_global_size(0);
    int i = a / N;
    int j = a - (i * N);
    int idx = (i * N) + j;
    float D = 1.0 / N;
    Tr[idx] = (((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx])) * D);
    Ti[idx] = (((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx])) * D);
    barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);
    if (a > N) { return; }
    for (int k = 0; k < N; ++k)
    {
        idx = (a * N) + k;
        Yr[a] += Tr[idx];
        Yi[a] += Ti[idx];
    }
}
/*
kernel void test_krn_fft(global int* SZ, global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Tr, global float* Ti, global float* Yr, global float* Yi)
{
    //#pragma disable(local) //!!! BUG: output of function when local work group is set to (1,) is incorrect and with None it is correct!
    int N = SZ[0];
    int a = get_global_id(0);
    int sz = get_global_size(0);
    int i = a / N;
    int j = a - (i * N);
    int idx = (i * N) + j;
    Tr[idx] = ((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx]));
    Ti[idx] = ((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx]));
    barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);
    if (a > 1) { return; }
    if (a == 0)
    {
        for (int k = 0; k < sz; ++k)
        {
            i = k / N;
            j = k - (i * N);
            idx = (i * N) + j;
            Yr[i] += Tr[idx];
        }
    }
    if (a == 1)
    {
        for (int k = 0; k < sz; ++k)
        {
            i = k / N;
            j = k - (i * N);
            idx = (i * N) + j;
            Yi[i] += Ti[idx];
        }
    }
}

kernel void test_krn_ifft(global int* SZ, global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Tr, global float* Ti, global float* Yr, global float* Yi)
{
    //#pragma disable(local)
    int N = SZ[0];
    int a = get_global_id(0);
    int sz = get_global_size(0);
    int i = a / N;
    int j = a - (i * N);
    int idx = (i * N) + j;
    float D = 1.0 / N;
    Tr[idx] = (((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx])) * D);
    Ti[idx] = (((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx])) * D);
    barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);
    if (a > 1) { return; }
    if (a == 0)
    {
        for (int k = 0; k < sz; ++k)
        {
            i = k / N;
            j = k - (i * N);
            idx = (i * N) + j;
            Yr[i] += Tr[idx]; //atomic_add(Yr[i], Tr[idx]);
        }
    }
    if (a == 1)
    {
        for (int k = 0; k < sz; ++k)
        {
            i = k / N;
            j = k - (i * N);
            idx = (i * N) + j;
            Yi[i] += Ti[idx]; //atomic_add(Yi[i], Ti[idx]);
        }
    }
}

kernel void test_krn_fft(global int* SZ, global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Yr, global float* Yi)
{
    int N = SZ[0];
    int a = get_global_id(0);
    int sz = get_global_size(0);
    int i = a / N;
    int j = a - (i * N);
    int idx = (i * N) + j;
    for (int k = 0; k < sz; ++k)
    {
        barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);
        if (k == a)
        {
            Yr[i] = Yr[i] + ((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx]));
            Yi[i] = Yi[i] + ((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx]));
        }
        barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);
    }
}

kernel void test_krn_ifft(global int* SZ, global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Yr, global float* Yi)
{
    int N = SZ[0];
    int a = get_global_id(0);
    int sz = get_global_size(0);
    int i = a / N;
    int j = a - (i * N);
    int idx = (i * N) + j;
    float D = 1.0 / N;
    for (int k = 0; k < sz; ++k)
    {
        barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);
        if (k == a)
        {
            Yr[i] = Yr[i] + (((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx])) * D);
            Yi[i] = Yi[i] + (((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx])) * D);
        }
        barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);
    }
}

kernel void test_krn_fft(global int* SZ, global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Yr, global float* Yi)
{
    //#pragma disable(local) //!!! BUG: output of function when local work group is set to (1,) is incorrect and with None it is correct!
    int N = SZ[0];
    int a = get_global_id(0);
    int sz = get_global_size(0);
    int i = a / N;
    int j = a - (i * N);
    int idx = (i * N) + j;
    Yr[i] = Yr[i] + ((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx]));
    Yi[i] = Yi[i] + ((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx]));
}

kernel void test_krn_ifft(global int* SZ, global float* Xr, global float* Xi, global float* Kr, global float* Ki, global float* Yr, global float* Yi)
{
    //#pragma disable(local)
    int N = SZ[0];
    int a = get_global_id(0);
    int sz = get_global_size(0);
    int i = a / N;
    int j = a - (i * N);
    int idx = (i * N) + j;
    float D = 1.0 / N;
    Yr[i] = Yr[i] + (((Xr[j] * Kr[idx]) - (Xi[j] * Ki[idx])) * D);
    Yi[i] = Yi[i] + (((Xr[j] * Ki[idx]) + (Xi[j] * Kr[idx])) * D);
}
*/