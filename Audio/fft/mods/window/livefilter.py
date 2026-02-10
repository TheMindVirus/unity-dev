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

live = True #False #True
filter_mode = filters.modes["FOURIER"]
#filter_mode = filters.modes["LAPLACE"]

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
sweep = 0
tmp = None
tmp2 = None

eq = \
{
    "c": 5.0,
    "f": 0.0,
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
    global sweep, tmp, tmp2
    if len(output) == 0:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])

        sweep += 0.00048828125
        sweep %= 0.09765625
        eq["f"] = sweep
        if sweep > 0.048828125:
            eq["f"] = 0.09765625 - sweep

        if filter_mode == filters.modes["FOURIER"]:
            if tmp == None:
                tmp = [[0 for i in range(0, n)] for j in range(0, len(output[0]))]
            if tmp2 == None:
                tmp2 = [[0 for i in range(0, n)] for j in range(0, len(output[0]))]
            inv = [0] * n
            fwd = [0] * n
            hn = int(n / 2)
            for i in range(0, hn):
                inv[i] = tmp2[k][i + hn]
                inv[i + hn] = tmp[k][i]
                fwd[i] = tmp[k][i + hn]
                fwd[i + hn] = dat[i]
            orig = dat.copy()
            dat_mod = tmp[k].copy()
            inv_mod = inv.copy()
            fwd_mod = fwd.copy()
            dat_mod = dat_mod * np.hanning(n)
            inv_mod = inv_mod * np.hanning(n)
            fwd_mod = fwd_mod * np.hanning(n)
            dat_mod = np.fft.fft(dat_mod)
            inv_mod = np.fft.fft(inv_mod)
            fwd_mod = np.fft.fft(fwd_mod)
            #dat_mod = filters.fourier_forward(list(dat_mod))
            #inv_mod = filters.fourier_forward(list(inv_mod))
            #fwd_mod = filters.fourier_forward(list(fwd_mod))
            dat_mod = filters.gauss_filter(list(dat_mod), eq)
            inv_mod = filters.gauss_filter(list(inv_mod), eq)
            fwd_mod = filters.gauss_filter(list(fwd_mod), eq)
            #dat_mod = filters.fourier_backward(dat_mod)
            #inv_mod = filters.fourier_backward(inv_mod)
            #fwd_mod = filters.fourier_backward(fwd_mod)
            dat_mod = np.fft.ifft(dat_mod)
            inv_mod = np.fft.ifft(inv_mod)
            fwd_mod = np.fft.ifft(fwd_mod)
            for i in range(0, hn):
                dat[i] = dat_mod[i] + inv_mod[hn + i]
                dat[i + hn] = dat_mod[i + hn] + fwd_mod[i]
            for i in range(0, n):
                tmp2[k][i] = tmp[k][i]
            for i in range(0, n):
                tmp[k][i] = orig[i]
        if filter_mode == -3: #filters.modes["FOURIER"]:
            n2 = n # * 10
            mod = [0] * n2
            mod[:n] = dat[:n]
            mod = np.fft.fft(mod)
            """
            for i in range(0, n2):
                if i > 150:
                    mod[i] = 0
            xp = mod.copy()
            yc = [0] * n
            hn = int(n / 2)
            h = np.hanning(
            for i in range(0, n):
                xp[0:hn] = xp[i]
                xp[hn
                yp = np.multiply(np.fft.ifft(xp), np.fft())
            """
            #for i in range(0, int(n/2)):
            #    mod[i] = mod[i] * (i / int(n/4)) #complex(-mod[i].real * (i / n), -mod[i].imag * (i / n))
            #for i in range(int(n/2), n):
            #    mod[i] = mod[i] * 0
            mod = np.fft.ifft(mod)
            dat = mod[:n]
        if filter_mode == -2: #filters.modes["FOURIER"]:
            inv = [0] * n
            fwd = [0] * n
            hn = int(n / 2)
            for i in range(0, hn):
                inv[i] = dat[i + hn]
                inv[i + hn] = dat[i]
                fwd[i] = dat[i + hn]
                fwd[i + hn] = dat[i]
                #inv[i] = dat[hn - i - 1]
                #inv[i + hn] = dat[i]
                #fwd[i] = dat[i + hn]
                #fwd[i + hn] = dat[n - i - 1]
            dat_mod = dat.copy()
            inv_mod = inv.copy()
            fwd_mod = fwd.copy()
            dat_mod = dat_mod * np.hanning(n)
            inv_mod = inv_mod * np.hanning(n)
            fwd_mod = fwd_mod * np.hanning(n)
            dat_mod = np.fft.fft(dat_mod)
            inv_mod = np.fft.fft(inv_mod)
            fwd_mod = np.fft.fft(fwd_mod)
            dat_mod = filters.gauss_filter(list(dat_mod), eq)
            inv_mod = filters.gauss_filter(list(inv_mod), eq)
            fwd_mod = filters.gauss_filter(list(fwd_mod), eq)
            dat_mod = np.fft.ifft(dat_mod)
            inv_mod = np.fft.ifft(inv_mod)
            fwd_mod = np.fft.ifft(fwd_mod)
            dat_mod = dat_mod * np.hanning(n)
            inv_mod = inv_mod * np.hanning(n)
            fwd_mod = fwd_mod * np.hanning(n)
            for i in range(0, hn):
                #dat[i] = inv_mod[hn + i]
                #dat[i + hn] = fwd_mod[i]
                dat[i] = dat_mod[i] + inv_mod[hn + i]
                dat[i + hn] = dat_mod[i + hn] + fwd_mod[i]
        if filter_mode == -1: #filters.modes["FOURIER"]:
            #t = time.monotonic()
            #tmp = dat.copy()
            #dat = dat * np.hanning(n)
            dat = np.fft.fft(dat)
            #mod = filters.fourier_forward(dat)
            #dat = filters.gauss_filter(list(dat), eq)
            #dat = filters.fourier_backward(dat)
            #"""
            for i in range(1, int(n / 2)):
                p = n - i
                if (i > 50):
                    dat[i] = 0
                if (p > 50):
                    dat[p] = 0
            #"""
            if type(tmp) != type(None):
                pass
            tmp = dat.copy()
            dat = np.fft.ifft(dat)
            #dat = np.add(tmp, dat)
            tmp = dat.copy()
            #t = time.monotonic() - t
            #print(t)
        if filter_mode == filters.modes["LAPLACE"]:
            #t = time.monotonic()
            #dat = filters.fourier_forward(dat)
            dat = filters.laplace_forward(dat)
            #dat = filters.gauss_filter(list(dat), eq)
            dat = filters.laplace_backward(dat)
            #dat = filters.fourier_backward(dat)
            #t = time.monotonic() - t
            #print(t)

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

if __name__ == "__main__":
    test()
    setup()
    while True:
        main()
