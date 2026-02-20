import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time
import struct

import pyopencl as cl

live = False #True #False

ch = 2
bsz = 1024 #8 #16 #32 #64 #100 #2048
sr = 44100
dev = None
file = None
stream = None
evt = threading.Event()
q = queue.Queue()
qpos = 0
full = False
progress = 0
ready = 0.50
skip = 0 #10000000
sweep = 0
tmp = None

eq = \
{
    "c": 5.0,
    "b": 2.0,
    "f": 0.0,
    "q": bsz,
    "g": 1.0,
    "l": 0.0,
}

cola = [0] * bsz
hbsz = int(bsz / 2)
for i in range(0, hbsz):
    cola[i] = cola[bsz - i - 1] = (i * 2) / bsz
cola = np.asarray(cola)

def setup_opencl(n):
    global ctx, device, queue, flags, code, program, logs
    global xr, xi, kr1, ki1, kr2, ki2, tr, ti, yr, yi, Nn
    global bXr, bXi, bKr, bKi, bTr, bTi, bYr, bYi, bNn
    global _test_fft, _test_ifft, _test_krn_fft, _test_krn_ifft

    ctx = cl.Context(dev_type = cl.device_type.ALL)
    device = ctx.get_info(cl.context_info.DEVICES)
    queue = cl.CommandQueue(ctx)
    flags = cl.mem_flags

    N = n
    N2 = N * N
    xr = np.linspace(0, N - 1, N, dtype = np.float32)
    xi = np.zeros_like(xr)
    yr = np.zeros_like(xr)
    yi = np.zeros_like(xr)
    zr = np.zeros_like(xr)
    zi = np.zeros_like(xr)
    tau = math.pi * 2.0
    kr1 = [0] * N2
    ki1 = [0] * N2
    kr2 = [0] * N2
    ki2 = [0] * N2
    for i in range(0, N):
        for j in range(0, N):
            idx = (i * N) + j
            jin = cmath.exp((0-1j * tau * j * i) / N)
            kr1[idx] = jin.real
            ki1[idx] = jin.imag
            jin = cmath.exp((0+1j * tau * j * i) / N)
            kr2[idx] = jin.real
            ki2[idx] = jin.imag
    kr1 = np.asarray(kr1, dtype = np.float32)
    ki1 = np.asarray(ki1, dtype = np.float32)
    kr2 = np.asarray(kr2, dtype = np.float32)
    ki2 = np.asarray(ki2, dtype = np.float32)
    tr = np.zeros_like(kr1)
    ti = np.zeros_like(kr1)

    bXr = cl.Buffer(ctx, flags.READ_WRITE, xr.nbytes)
    bXi = cl.Buffer(ctx, flags.READ_WRITE, xi.nbytes)
    bKr = cl.Buffer(ctx, flags.READ_WRITE, kr1.nbytes)
    bKi = cl.Buffer(ctx, flags.READ_WRITE, ki1.nbytes)
    bTr = cl.Buffer(ctx, flags.READ_WRITE, tr.nbytes)
    bTi = cl.Buffer(ctx, flags.READ_WRITE, ti.nbytes)
    bYr = cl.Buffer(ctx, flags.READ_WRITE, yr.nbytes)
    bYi = cl.Buffer(ctx, flags.READ_WRITE, yi.nbytes)

    Nn = np.asarray([N])
    bNn = cl.Buffer(ctx, flags.READ_WRITE, Nn.nbytes)

    code = ""
    with open("main.cl", "r") as file:
        code = file.read()

    program = cl.Program(ctx, code)
    build = program.build()
    logs = build.get_build_info(device[0], cl.program_build_info.LOG)

    _test_fft = getattr(program, "test_fft")
    _test_ifft = getattr(program, "test_ifft")
    _test_krn_fft = getattr(program, "test_krn_fft")
    _test_krn_ifft = getattr(program, "test_krn_ifft")

def test_fft(X):
    global queue, _test_fft
    global xr, xi, kr1, ki1, yr, yi
    global bXr, bXi, bKr, bKi, bYr, bYi
    N = len(X)
    Y = [0] * N
    for i in range(0, N):
        xr[i] = X[i].real
        xi[i] = X[i].imag
        yr[i] = 0.0
        yi[i] = 0.0
    cl.enqueue_copy(queue, bXr, xr)
    cl.enqueue_copy(queue, bXi, xi)
    cl.enqueue_copy(queue, bKr, kr1)
    cl.enqueue_copy(queue, bKi, ki1)
    cl.enqueue_copy(queue, bYr, yr)
    cl.enqueue_copy(queue, bYi, yi)
    queue.finish()
    _test_fft(queue, (N,), None, bXr, bXi, bKr, bKi, bYr, bYi)
    cl.enqueue_copy(queue, yr, bYr)
    cl.enqueue_copy(queue, yi, bYi)
    queue.finish()
    for i in range(0, N):
        Y[i] = complex(yr[i], yi[i])
    return Y

def test_ifft(X):
    global queue, _test_ifft
    global xr, xi, kr2, ki2, yr, yi
    global bXr, bXi, bKr, bKi, bYr, bYi
    N = len(X)
    Y = [0] * N
    for i in range(0, N):
        xr[i] = X[i].real
        xi[i] = X[i].imag
        yr[i] = 0.0
        yi[i] = 0.0
    cl.enqueue_copy(queue, bXr, xr)
    cl.enqueue_copy(queue, bXi, xi)
    cl.enqueue_copy(queue, bKr, kr2)
    cl.enqueue_copy(queue, bKi, ki2)
    cl.enqueue_copy(queue, bYr, yr)
    cl.enqueue_copy(queue, bYi, yi)
    queue.finish()
    _test_ifft(queue, (N,), None, bXr, bXi, bKr, bKi, bYr, bYi)
    cl.enqueue_copy(queue, yr, bYr)
    cl.enqueue_copy(queue, yi, bYi)
    queue.finish()
    for i in range(0, N):
        Y[i] = complex(yr[i], yi[i])
    return Y

def test_krn_fft(X):
    global queue, _test_krn_fft
    global xr, xi, kr1, ki1, tr, ti, yr, yi, Nn
    global bXr, bXi, bKr, bKi, bTr, bTi, bYr, bYi, bNn
    N = len(X)
    N2 = N * N
    Y = [0] * N
    for i in range(0, N):
        xr[i] = X[i].real
        xi[i] = X[i].imag
        yr[i] = 0.0
        yi[i] = 0.0
    cl.enqueue_copy(queue, bNn, Nn)
    cl.enqueue_copy(queue, bXr, xr)
    cl.enqueue_copy(queue, bXi, xi)
    cl.enqueue_copy(queue, bKr, kr1)
    cl.enqueue_copy(queue, bKi, ki1)
    cl.enqueue_copy(queue, bTr, tr)
    cl.enqueue_copy(queue, bTi, ti)
    cl.enqueue_copy(queue, bYr, yr)
    cl.enqueue_copy(queue, bYi, yi)
    queue.finish()
    _test_krn_fft(queue, (N2,), None, bNn, bXr, bXi, bKr, bKi, bTr, bTi, bYr, bYi)
    cl.enqueue_copy(queue, yr, bYr)
    cl.enqueue_copy(queue, yi, bYi)
    queue.finish()
    for i in range(0, N):
        Y[i] = complex(yr[i], yi[i])
    return Y

def test_krn_ifft(X):
    global queue, _test_krn_ifft
    global xr, xi, kr2, ki2, tr, ti, yr, yi, Nn
    global bXr, bXi, bKr, bKi, bTr, bTi, bYr, bYi, bNn
    N = len(X)
    N2 = N * N
    Y = [0] * N
    for i in range(0, N):
        xr[i] = X[i].real
        xi[i] = X[i].imag
        yr[i] = 0.0
        yi[i] = 0.0
    cl.enqueue_copy(queue, bNn, Nn)
    cl.enqueue_copy(queue, bXr, xr)
    cl.enqueue_copy(queue, bXi, xi)
    cl.enqueue_copy(queue, bKr, kr2)
    cl.enqueue_copy(queue, bKi, ki2)
    cl.enqueue_copy(queue, bTr, tr)
    cl.enqueue_copy(queue, bTi, ti)
    cl.enqueue_copy(queue, bYr, yr)
    cl.enqueue_copy(queue, bYi, yi)
    queue.finish()
    _test_krn_ifft(queue, (N2,), None, bNn, bXr, bXi, bKr, bKi, bTr, bTi, bYr, bYi)
    cl.enqueue_copy(queue, yr, bYr)
    cl.enqueue_copy(queue, yi, bYi)
    queue.finish()
    for i in range(0, N):
        Y[i] = complex(yr[i], yi[i])
    return Y

def dsp(output, frames, time, status):
    global qpos
    data = [0]
    if qpos < len(q.queue):
        data = q.queue[qpos]
        print(qpos)
        if live:
            data = pre(data.copy())
        qpos += 1
    if len(data) < len(output):
        output[:len(data)] = data
        output[len(data):] = 0
        evt.set()
    else:
        output[:] = data

def pre(output):
    global sweep, tmp, cola
    if len(output) == 0 \
    or len(output) != bsz:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])

        sweep += 0.1 #0.01
        sweep %= math.pi * 2.0
        eq["f"] = ((math.sin(sweep) + 1.0) / 2.0) / 16.0
        
        if tmp == None:
            tmp = [[0 for i in range(0, n)] for j in range(0, len(output[0]))]
        inv = [0] * n
        hn = int(n / 2)
        for i in range(0, hn):
            inv[i] = tmp[k][i + hn]
            inv[i + hn] = dat[i]
        
        orig = dat.copy()
        dat_mod = inv.copy()
        bac_mod = tmp[k].copy()
        fwd_mod = dat.copy()
        
        dat_mod *= cola
        bac_mod *= cola
        fwd_mod *= cola

        dat_mod = list(dat_mod)
        bac_mod = list(bac_mod)
        fwd_mod = list(fwd_mod)
        
        dat_mod = test_krn_fft(dat_mod)
        bac_mod = test_krn_fft(bac_mod)
        fwd_mod = test_krn_fft(fwd_mod)

        for i in range(0, n):
            p = float(i)
            if i > n / 2:
                p = n - i
            dat_mod[i] *= (pow(eq["c"], (-abs(pow(p - eq["f"], eq["b"])) / eq["q"])) * eq["g"]) + eq["l"]
            bac_mod[i] *= (pow(eq["c"], (-abs(pow(p - eq["f"], eq["b"])) / eq["q"])) * eq["g"]) + eq["l"]
            fwd_mod[i] *= (pow(eq["c"], (-abs(pow(p - eq["f"], eq["b"])) / eq["q"])) * eq["g"]) + eq["l"]
        
        dat_mod = test_krn_ifft(dat_mod)
        bac_mod = test_krn_ifft(bac_mod)
        fwd_mod = test_krn_ifft(fwd_mod)

        for i in range(0, hn):
            dat[i] = dat_mod[i] + bac_mod[i + hn]
            dat[i + hn] = dat_mod[i + hn] + fwd_mod[i]

        for i in range(0, n):
            tmp[k][i] = orig[i]
        
        for i in range(0, n):
            if math.isinf(dat[i].real) \
            or math.isnan(dat[i].real):
                output[i][k] = 0.0
            else:
                output[i][k] = dat[i].real

    return output

def main():
    global q, qpos, file, stream, progress, skip, full, evt
    try:
        if not full:
            file = sf.SoundFile("../../Bubblegum.mp3")
            print(file)
            ch = file.channels
            sr = file.samplerate
            file.seek(skip, sf.SEEK_SET)
            data = [0] * bsz
            stream = sd.OutputStream(samplerate = sr,
                                     blocksize = bsz,
                                     device = dev,
                                     channels = ch,
                                     callback = dsp)
            stream.stop()
            progress = 0.0
            while len(data):
                data = file.read(bsz)
                if not live:
                    data = pre(data.copy())
                q.put_nowait(data)
                if not live:
                    progress += (bsz / file.frames) * 100
                    print("{:0.2f}%".format(progress))
                    if progress >= ready:
                        break
            print("done?")
            full = True
        stream.stop()
        stream.start()
        evt.wait()
        evt.clear()
        print("evt")
        qpos = 0
    except Exception as error:
        raise error

def setup():
    print("loading...")
    setup_opencl(bsz)
    #setup_opencl(7)
    #x = [0,1,2,3,4,5,6]
    #y = test_krn_fft(x)
    #z = test_krn_ifft(y)
    #print(x)
    #print(y)
    #print(z)

if __name__ == "__main__":
    setup()
    while True:
        main()
