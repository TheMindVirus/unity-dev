import sounddevice as sd
import soundfile as sf
import scipy as sp
import numpy as np
import threading
import queue
import math

import scipy.signal as sp_signal

ch = 2
sz = 100
bsz = 2048 # 100
sr = 44100
dev = None
q = queue.Queue(maxsize = sz)
evt = threading.Event()

def dsp(output, frames, time, status):
    assert frames == bsz
    if status.output_underflow:
        raise sd.CallbackAbort
    assert not status
    try:
        data = q.get_nowait()
    except queue.Empty as error:
        raise sd.CallbackAbort from error
    if len(data) < len(output):
        output[:len(data)] = data
        output[len(data):].fill(0)
        raise sd.CallbackStop
    else:
        output[:] = data

    for i in range(0, len(output)):
        pass
        #output[i] *= 0.25
        #output[i] *= math.sin(time.inputBufferAdcTime * 1000)
        #fft = np.fft.fft(output)
        #ifft = np.fft.ifft(output)

"""
def pre(data):
    for k in range(0, len(data[0])):
        dat = []
        for i in range(0, len(data)):
            dat.append(data[i][k])
        b, a = sp_signal.iirfilter(4, Wn = 2.5, fs = 30, btype = "low", ftype = "butter")
        dat = sp_signal.lfilter(b, a, dat)
        for i in range(0, len(data)):
            data[i][k] = dat[i].real
    return data
"""
    
"""
def pre(data):
    for k in range(0, len(data[0])):
        dat = []
        for i in range(0, len(data)):
            dat.append(data[i][k])
        dat = np.fft.fft(dat)
        n = len(dat)
        for i in range(0, n):
            #if i < n / 4 or i > (n / 4) * 3:
            #    dat[i] *= 2.00 # Clippy Bass Boost
            #if i > n / 4 and i < (n / 4) * 3:
            #    dat[i] *= 0.00 # Clippy Mid Cut
            #o = -0.30 ; p = 0.20 ; q = 0.05 ; b = 8.00 ; c = 5.00
            #dat[i] += o * pow(c, -pow(abs((i / n) - p), b) / q) # Strange Resonance
        dat = np.fft.ifft(dat)
        for i in range(0, len(data)):
            data[i][k] = dat[i].real
    return data
"""

"""
def pre(data):
    for i in range(0, len(data)):
        data[i][1] = 0 # Functional Left Pan
    return data
"""

#"""
def pre(data): # Odd Bitcrusher
    for channel in range(0, ch):
        dat = []
        nsz = int(len(data) / ch)
        for i in range(0, nsz):
            dat.append(data[(i * ch) + channel])
            if channel == 0:
                dat[i] *= 0.0
        for i in range(0, nsz):
            data[(i * ch) + channel] = dat[i]
    return data
#"""

"""
def pre(data):
    data = np.fft.fft(data)
    n = len(data)
    for i in range(0, n):
        #if i < n / 4 or i > (n / 4) * 3:
        #    data.real *= 1.03 # Clippy Bass Boost
        o = 1.00
        p = 0.50
        q = 0.05
        data += o * pow(5.0, -pow(abs((i / n) - p), 2) / q) # Odd Stereo Pan
    data = np.fft.ifft(data)
    data = data.real
    return data
"""

try:
    with sf.SoundFile("Bubblegum.mp3") as file:
        ch = file.channels
        sr = file.samplerate
        for i in range(0, sz):
            data = file.read(bsz)
            if not len(data):
                break
            data = pre(data)
            q.put_nowait(data)
        stream = sd.OutputStream(samplerate = sr,
                                 blocksize = bsz,
                                 device = dev,
                                 channels = ch,
                                 callback = dsp)
        with stream:
            while len(data):
                data = file.read(bsz)
                data = pre(data)
                q.put(data, timeout = bsz * sz / sr)
            evt.wait()
except queue.Full as error:
    raise error
