import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time
import struct

import filters

live = False #True
#filter_mode = filters.modes["NULL"]
#filter_mode = filters.modes["FOURIER"]
filter_mode = filters.modes["LAPLACE"]
#filter_mode = filters.modes["HILBERT"]
#filter_mode = filters.modes["HARTLEY"]

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
ready = 0.10
sweep = 0
tmp = None

eq = \
{
    "x": 0.0,
    "y": 0.0,
    "c": 5.0,
    "b": 2.0,
    "q": bsz,
    "g": 1.0,
    "l": 0.0,
}

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
    global sweep, tmp
    if len(output) == 0:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])

        sweep += 0.01
        sweep %= math.pi * 2.0
        eq["x"] = ((math.sin(sweep) + 1.0) / 2.0) / 16.0
        eq["y"] = 0.5 #((math.cos(sweep) + 1.0) / 2.0) / 16.0
        
        if filter_mode == filters.modes["NULL"]:
            if tmp == None:
                tmp = [[0 for i in range(0, n)] for j in range(0, len(output[0]))]
            inv = [0] * n
            hn = int(n / 2)
            for i in range(0, hn):
                inv[i] = tmp[k][i + hn]
                inv[i + hn] = dat[i]
            orig = dat.copy()
            dat_mod = inv.copy()
            inv_mod = tmp[k].copy()
            fwd_mod = dat.copy()
            dat_mod *= np.hanning(n)
            inv_mod *= np.hanning(n)
            fwd_mod *= np.hanning(n)
            dat_mod = np.fft.fft(dat_mod)
            inv_mod = np.fft.fft(inv_mod)
            fwd_mod = np.fft.fft(fwd_mod)
            dat_mod *= filters.gauss_filter(bsz, eq)[:bsz]
            inv_mod *= filters.gauss_filter(bsz, eq)[:bsz]
            fwd_mod *= filters.gauss_filter(bsz, eq)[:bsz]
            dat_mod = np.fft.ifft(dat_mod)
            inv_mod = np.fft.ifft(inv_mod)
            fwd_mod = np.fft.ifft(fwd_mod)
            for i in range(0, hn):
                dat[i] = dat_mod[i] + inv_mod[hn + i]
                dat[i + hn] = dat_mod[i + hn] + fwd_mod[i]
            for i in range(0, n):
                tmp[k][i] = orig[i]
            pass
        if filter_mode == filters.modes["FOURIER"]:
            #t = time.monotonic()
            dat = filters.fourier_forward(dat)
            #dat = np.multiply(dat, filters.gauss_filter_2d(bsz, eq))
            dat = filters.fourier_backward(list(dat))
            #t = time.monotonic() - t
            #print(t)
            pass
        if filter_mode == filters.modes["LAPLACE"]:
            #t = time.monotonic()
            dat = filters.laplace_forward(dat)
            for i in range(0, n):
                for j in range(0, n):
                    dat[(i * n) + j] = dat[(i * n) + (n - j - 1)]
                    #if j < n / 16:
                    #    dat[(i * n) + j] = 0.0
            #dat = np.multiply(dat, filters.gauss_filter_2d(bsz, eq))
            dat = filters.laplace_backward(list(dat))
            #t = time.monotonic() - t
            #print(t)
            pass
        if filter_mode == filters.modes["HILBERT"]:
            #t = time.monotonic()
            dat = filters.hilbert_forward(dat)
            #dat = np.multiply(dat, filters.gauss_filter_2d(bsz, eq))
            dat = filters.hilbert_backward(list(dat))
            #t = time.monotonic() - t
            #print(t)
            pass
        if filter_mode == filters.modes["HARTLEY"]:
            #t = time.monotonic()
            dat = filters.hartley_forward(dat)
            for i in range(0, n):
                for j in range(0, n):
                    if j < n / 2:
                        dat[(i * n) + j] = 0.0
            #dat = np.multiply(dat, filters.gauss_filter_2d(bsz, eq))
            dat = filters.hartley_backward(list(dat))
            #t = time.monotonic() - t
            #print(t)
            pass
        
        for i in range(0, n):
            if math.isinf(dat[i].real) \
            or math.isnan(dat[i].real):
                output[i][k] = 0.0
            else:
                output[i][k] = dat[i].real

    return output

def main():
    global q, qpos, file, stream, progress, full, evt
    try:
        if not full:
            file = sf.SoundFile("../../Bubblegum.mp3")
            print(file)
            ch = file.channels
            sr = file.samplerate
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

def test():
    n = 7 #2048 #pow(2, 20) - 1 #7
    x = [0, 1, 2, 3, 4, 5, 6]
    x = np.linspace(0, n - 1, n)
    if filter_mode == filters.modes["FOURIER"]:
        filters.fourier_forward_setup(n)
        filters.fourier_backward_setup(n)
    if filter_mode == filters.modes["LAPLACE"]:
        filters.laplace_forward_setup(n)
        filters.laplace_backward_setup(n)
    if filter_mode == filters.modes["HILBERT"]:
        filters.hilbert_forward_setup(n)
        filters.hilbert_backward_setup(n)
    if filter_mode == filters.modes["HARTLEY"]:
        filters.hartley_forward_setup(n)
        filters.hartley_backward_setup(n)
    if filter_mode == filters.modes["FOURIER"]:
        t = time.monotonic()
        for i in range(0, 10):
            a = filters.fourier_forward(list(x))
            b = filters.fourier_backward(a)
        t = time.monotonic() - t
    if filter_mode == filters.modes["LAPLACE"]:  
        t = time.monotonic()
        for i in range(0, 10):
            a = filters.laplace_forward(list(x))
            b = filters.laplace_backward(a)
        t = time.monotonic() - t
    if filter_mode == filters.modes["HILBERT"]:  
        t = time.monotonic()
        for i in range(0, 10):
            a = filters.hilbert_forward(list(x))
            b = filters.hilbert_backward(a)
        t = time.monotonic() - t
    if filter_mode == filters.modes["HARTLEY"]:  
        t = time.monotonic()
        for i in range(0, 10):
            a = filters.hartley_forward(list(x))
            b = filters.hartley_backward(a)
        t = time.monotonic() - t
    if filter_mode == filters.modes["NULL"]:
        return
    print(t, "seconds")
    if filter_mode == filters.modes["FOURIER"]:
        t = time.monotonic()
        for i in range(0, 10):
            c = np.fft.fft(x)
            d = np.fft.ifft(c)
        t = time.monotonic() - t
        print(t, "seconds")
    if len(x) < 10:
        print(x)
        print(a)
        print(b)
        if filter_mode == filters.modes["FOURIER"]: 
            print(c)
            print(d)

def setup():
    print("loading...")
    if filter_mode == filters.modes["FOURIER"]:
        filters.fourier_forward_setup(bsz)
        filters.fourier_backward_setup(bsz)
    if filter_mode == filters.modes["LAPLACE"]:
        filters.laplace_forward_setup(bsz)
        filters.laplace_backward_setup(bsz)
    if filter_mode == filters.modes["HILBERT"]:
        filters.hilbert_forward_setup(bsz)
        filters.hilbert_backward_setup(bsz)
    if filter_mode == filters.modes["HARTLEY"]:
        filters.hartley_forward_setup(bsz)
        filters.hartley_backward_setup(bsz)

if __name__ == "__main__":
    test()
    setup()
    while True:
        main()
