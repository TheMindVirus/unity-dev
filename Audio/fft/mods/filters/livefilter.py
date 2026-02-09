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
#import filters2 as filters
#import filters_src as filters

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
    global sweep
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
            #t = time.monotonic()
            #dat = np.fft.fft(dat)
            dat = filters.fourier_forward(dat)
            dat = filters.gauss_filter(list(dat), eq)
            dat = filters.fourier_backward(dat)
            #dat = np.fft.ifft(dat)
            #t = time.monotonic() - t
            #print(t)
        if filter_mode == filters.modes["LAPLACE"]:
            #t = time.monotonic()
            dat = filters.laplace_forward(dat)
            #dat = filters.gauss_filter(list(dat), eq)
            dat = filters.laplace_backward(dat)
            #t = time.monotonic() - t
            #print(t)

        for i in range(0, n):
            if math.isnan(dat[i].real):
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
