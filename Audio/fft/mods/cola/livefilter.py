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

live = False #True #False
filter_mode = filters.modes["GAUSS"]
#filter_mode = filters.modes["FOURIER"]
#filter_mode = filters.modes["LAPLACE"]
#filter_mode = filters.modes["HILBERT"]
#filter_mode = filters.modes["HARTLEY"]
#filter_mode = filters.modes["HADAMARD"]

#window_mode = "HANN"
window_mode = "COLA"

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
hann = np.hanning(bsz)
cola = np.asarray(cola)

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
    global sweep, tmp, hann, cola
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

        if window_mode == "HANN":
            dat_mod *= hann
            bac_mod *= hann
            fwd_mod *= hann
            
        if window_mode == "COLA":
            dat_mod *= cola
            bac_mod *= cola
            fwd_mod *= cola
        
        if filter_mode == filters.modes["GAUSS"]:
            dat_mod = np.fft.fft(dat_mod)
            bac_mod = np.fft.fft(bac_mod)
            fwd_mod = np.fft.fft(fwd_mod)
            dat_mod *= filters.gauss(n, eq)
            bac_mod *= filters.gauss(n, eq)
            fwd_mod *= filters.gauss(n, eq)
            dat_mod = np.fft.ifft(dat_mod)
            bac_mod = np.fft.ifft(bac_mod)
            fwd_mod = np.fft.ifft(fwd_mod)
        
        if filter_mode == filters.modes["FOURIER"]:
            dat_mod = filters.fourier(list(dat_mod), eq)
            bac_mod = filters.fourier(list(bac_mod), eq)
            fwd_mod = filters.fourier(list(fwd_mod), eq)
            
        if filter_mode == filters.modes["LAPLACE"]:
            eq["g"] = 10.0
            eq["f"] = 0.5
            dat_mod = filters.laplace(list(dat_mod), eq, mode = 0)
            bac_mod = filters.laplace(list(bac_mod), eq, mode = 0)
            fwd_mod = filters.laplace(list(fwd_mod), eq, mode = 0)
        
        if filter_mode == filters.modes["HILBERT"]:
            eq["g"] = 10.0
            eq["f"] = 0.5
            dat_mod = filters.hilbert(list(dat_mod), eq)
            bac_mod = filters.hilbert(list(bac_mod), eq)
            fwd_mod = filters.hilbert(list(fwd_mod), eq)
            
        if filter_mode == filters.modes["HARTLEY"]:
            eq["g"] = 10.0
            eq["f"] = 0.5
            dat_mod = filters.hartley(list(dat_mod), eq)
            bac_mod = filters.hartley(list(bac_mod), eq)
            fwd_mod = filters.hartley(list(fwd_mod), eq)

        if filter_mode == filters.modes["HADAMARD"]:
            dat_mod = filters.hadamard(list(dat_mod), eq)
            bac_mod = filters.hadamard(list(bac_mod), eq)
            fwd_mod = filters.hadamard(list(fwd_mod), eq)

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
    if filter_mode == filters.modes["FOURIER"]:
        filters.fourier_setup(bsz)
    if filter_mode == filters.modes["LAPLACE"]:
        filters.laplace_setup(bsz)
    if filter_mode == filters.modes["HILBERT"]:
        filters.hilbert_setup(bsz)
    if filter_mode == filters.modes["HARTLEY"]:
        filters.hartley_setup(bsz)

if __name__ == "__main__":
    setup()
    while True:
        main()
