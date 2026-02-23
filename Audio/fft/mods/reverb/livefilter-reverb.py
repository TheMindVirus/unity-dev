import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time
import struct
import random

live = False #True #False

ch = 2
bsz = 2048 #2048 #8 #16 #32 #64 #100 #2048
sr = 44100
dev = None
file = None
stream = None
evt = threading.Event()
q = queue.Queue()
qpos = 0
full = False
progress = 0
ready = 1.00 #0.50
skip = 10000000
peak = None
mode = None
decay = 0.95
scale = 64

#tau = 2.0 * math.pi
hbsz = int(bsz / 2)
hann = np.hanning(bsz)
cola = np.append(np.linspace(0, 1, hbsz), np.linspace(1, 0, hbsz))
#sss = (np.random.random(bsz * 2) * 2.0) - 1.0

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
    global peak, mode, decay, scale, hann, cola, sss
    if len(output) == 0 \
    or len(output) != bsz:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])

        if peak == None:
            peak = [0 for k in range(0, len(output[0]))]

        if mode == None:
            mode = [[0 for i in range(0, n)] for k in range(0, len(output[0]))]
            
        orig = dat.copy()

        #costable = [0] * n
        #for i in range(0, n):
        #    for j in range(0, n):
        #        costable[j] += (1 / n) * mag * math.cos((freq * (j + (period * phi)) / sr) * tau)

        mod = np.fft.fft(dat)

        for i in range(0, n):
            mag = math.sqrt(mod[i].real * mod[i].real
                          + mod[i].imag * mod[i].imag)
            #phi = math.atan2(mod[i].imag, mod[i].real) / tau
            #mod[i] = complex(mag * math.cos(phi), mag * math.sin(phi))
            #pos = i if i > (n / 2) else n - i
            #freq = pos * (sr / n) if i > (n / 2) else -pos * (sr / n)
            #period = 0 if freq == 0 else int((1.0 / freq) * sr)
            #offset = 0 if period == 0 else (n % period) / period
            mag /= scale
            if mag > mode[k][i]:
                mode[k][i] = mag
            else:
                mode[k][i] *= decay

        for i in range(0, n):
            if abs(dat[i]) > peak[k]:
                peak[k] = abs(dat[i])
        if peak[k] > 0:
            peak[k] *= decay

        hn = int(n / 2)
        sss = (np.random.random(bsz * 2) * 2.0) - 1.0

        sss_bac = sss[:n].copy()
        sss_dat = sss[hn:n+hn].copy()
        sss_fwd = sss[n:2*n].copy()

        sss_bac *= cola #hann
        sss_dat *= cola #hann
        sss_fwd *= cola #hann
        
        sss_bac = np.fft.fft(sss_bac)
        sss_dat = np.fft.fft(sss_dat)
        sss_fwd = np.fft.fft(sss_fwd)
        
        sss_bac *= mode[k]
        sss_dat *= mode[k]
        sss_fwd *= mode[k]
        
        sss_bac = np.fft.ifft(sss_bac)
        sss_dat = np.fft.ifft(sss_dat)
        sss_fwd = np.fft.ifft(sss_fwd)
        
        sss_mod = sss_dat + np.append(sss_bac[hn:], sss_fwd[:hn])
                
        for i in range(0, n):
            dat[i] = (1.0 * dat[i]) + (1.0 * peak[k] * sss_mod[i])
        
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
                    if progress > 0.5:
                        for i in range(0, len(data)):
                            for k in range(0, len(data[0])):
                                data[i][k] = 0.0
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

if __name__ == "__main__":
    while True:
        main()
