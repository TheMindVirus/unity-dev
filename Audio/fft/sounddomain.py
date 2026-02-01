import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time

import scipy.integrate as integrate
import scipy.fft as fft

modes = \
{
    "NULL": 0,
    "FFT": 1,
    "IFFT": 2,
    "RFFT": 3,
    "PYFFT": 4,
    "SCIPY_FFT": 5,
    "SCIPY_DCT": 6,
}

mode = 6 #6 #modes["FFT"]

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

def pre(output):
    if len(output) == 0:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])

        if mode == 1:
            dat = np.fft.fft(dat)
        if mode == 2:
            dat = np.fft.ifft(dat)
        if mode == 3:
            dat = np.fft.fft(dat)
        if mode == 4:
            dat = py_fft(dat)
        if mode == 5:
            dat = fft.fft(dat)
        if mode == 6:
            dat = fft.dct(dat)
        
        for i in range(0, n):
            if i > n / 16 and i < (n / 15) * 16:
                dat[i] *= 0.00

        if mode == 1:
            dat = np.fft.ifft(dat) # Clippy Live Low Pass
        if mode == 2:
            dat = np.fft.fft(dat) # Clippy Live Low Pass
        if mode == 3:
            dat = np.fft.irfft(dat) # Clippy Live Low Pass Formant Filter
        if mode == 4:
            dat = py_ifft(dat)
        if mode == 5:
            dat = fft.ifft(dat)
        if mode == 6:
            dat = fft.idct(dat)
        
        for i in range(0, n):
            output[i][k] = dat[i].real

    return output

def main():
    a = py_fft([0,1,2,3,4,5,6])
    b = py_ifft(a)
    print(a)
    print(b)
    try:
        with sf.SoundFile("Bubblegum.mp3") as file:
            print(file)
            file.seek(0)
            ch = file.channels
            sr = file.samplerate
            data = [0] * sz
            #for i in range(0, sz):
            #    print(sz)
            #    data = file.read(bsz)
            #    if not len(data):
            #        break
            #    data = pre(data)
            #    #print("done!")
            #    #q.put_nowait(data)
            #print(data)
            stream = sd.OutputStream(samplerate = sr,
                                     blocksize = bsz,
                                     device = dev,
                                     channels = ch,
                                     callback = dsp)
            with stream:
                print(stream)
                while len(data):
                    data = file.read(bsz)
                    data = pre(data)
                    q.put(data) #, timeout = bsz * sz / sr)
                print("done?")
                q.empty()
                #evt.wait()
    except Exception as error:
        print(error)
    time.sleep(1)

def py_fft(data):
    #data = np.fft.fft(data)
    #data = fft.fft(data)
    """
    x = data
    N = len(x)
    y = [0+0j] * N
    for i in range(0, N):
        for j in range(0, N):
            y[i] += x[j] * math.cos((2.0 * math.pi * j * i) / N)
            y[i] += complex(0, x[j] * -math.sin((2.0 * math.pi * j * i) / N))
    data = y
    """
    for u in range(0, len(data)):
        data[u] = integrate.quad(lambda t: cmath.exp(0+1j * 2.0 * math.pi * u * t).real, -np.inf, np.inf)
    #data = integrate.quad(lambda x: data[int(x)], -np.inf, np.inf)
    #data[i] = integrate.quad(lambda x: cmath.exp(0+1j * 2.0 * math.pi * data[i]), -np.inf, np.inf)
    #data = integrate.quad(lambda x: cmath.exp(0+1j * 2.0 * math.pi * x), 0, len(data))
    return data

def py_ifft(data):
    #data = np.fft.ifft(data)
    #data = fft.ifft(data)
    """
    x = data
    N = len(x)
    y = [0+0j] * N
    for i in range(0, N):
        for j in range(0, N):
            t = math.cos((2.0 * math.pi * j * i) / N)
            t -= math.sin((2.0 * math.pi * j * i) / N)
            y[i] += x[j] * t * (1 / N)
            t = math.cos((2.0 * math.pi * j * i) / N)
            t += math.sin((2.0 * math.pi * j * i) / N)
            y[i] += complex(0, x[j] * t * (1 / N))
    for i in range(0, N):
        y[i] = round(y[i].real)
    data = y
    """
    #data = integrate.quad(lambda x: data[int(x)], -np.inf, np.inf)
    return data

if __name__ == "__main__":
    while True:
        main()
