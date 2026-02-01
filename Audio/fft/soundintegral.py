import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import cmath
import math
import time

modes = \
{
    "NULL": 0,
    "FFT": 1,
    "IFFT": 2,
    "RFFT": 3,
    "CONVOLUTION": 4,
    "INTEGRAL_FOURIER": 5,
}

mode = 4 #modes["FFT"]

ch = 2
sz = 100
bsz = 2048 # 100
div = 32 # 64
sr = 44100
dev = None
q = queue.Queue(maxsize = sz)
progress = 0.0

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

#pos = 0
#nrg = 10
#ini = 100
#tot = 1000000000

def pre(output):
    global pos
    if len(output) == 0:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        nn = int(n / div)
        for i in range(0, n):
            dat.append(output[i][k])

        if mode == 1:
            dat = np.fft.fft(dat)
        if mode == 2:
            dat = np.fft.ifft(dat)
        if mode == 3:
            dat = np.fft.fft(dat)
        if mode == 4:
            for i in range(0, n, nn):
                #dat[i:i+nn] = np.fft.fft(dat[i:i+nn])
                dat[i:i+nn] = convolute(dat[i:i+nn], convolution_filter)
                break
        if mode == 5:
            dat = integrate(dat, integral_fourier_filter_fwd)

        if (mode < 4):
            # Clippy Low Pass Formant Filter
            for i in range(0, n):
                if i > n / 16 and i < (n / 15) * 16:
                    dat[i] *= 0.00

        if (mode == 4):
            for i in range(0, n, nn):
                for j in range(i, i+nn):
                    m = j - i
                    if m > nn / 16 and m < (nn / 15) * 16:
                        dat[j] *= 0.00
                break

        if (mode >= 5):
            for i in range(0, n):
                gain = 0.5
                phase = 441
                tmp = dat[i] * gain * ((math.sin((i / n) * 2.0 * math.pi * phase) + 1.0) * 0.5)
                dat[i] += tmp
            #for i in range(0, n):
            #    gain = 1.0
            #    phase = pos / nrg
            #    tmp = dat[i] * gain * (math.sin((i / n) * 2.0 * math.pi * phase))
            #    pos += 1
            #    pos %= tot
            #    if pos < ini:
            #        pos = ini
            #    dat[i] += tmp

        if mode == 1:
            dat = np.fft.ifft(dat) 
        if mode == 2:
            dat = np.fft.fft(dat)
        if mode == 3:
            dat = np.fft.irfft(dat)
        if mode == 4:
            for i in range(0, n, nn):
                #dat[i:i+nn] = np.fft.ifft(dat[i:i+nn])                
                dat[i:i+nn] = deconvolute(dat[i:i+nn], convolution_filter)
                break
        if mode == 5:
            dat = differentiate(dat, integral_fourier_filter_inv)

        for i in range(0, n):
            output[i][k] = dat[i].real

    return output

def setup():
    print("Now Loading...")
    convolution_setup(int(bsz / div))
    integral_fourier_setup(bsz)

def loop():
    global q, progress
    try:
        with sf.SoundFile("Bubblegum.mp3") as file:
            print(file)
            ch = file.channels
            sr = file.samplerate
            data = [0] * bsz
            stream = sd.OutputStream(samplerate = sr,
                                     blocksize = bsz,
                                     device = dev,
                                     channels = ch,
                                     callback = dsp)
            with stream:
                print(stream)
                q = queue.Queue(maxsize = sz)
                progress = 0.0
                if mode == 4:
                    sd.stop()
                while len(data):
                    data = file.read(bsz)
                    #print("pre")
                    data = pre(data)
                    #print("post")
                    q.put(data)
                    progress += (bsz / file.frames) * 100
                    #print(str(progress) + "%")
                print("done?")
                q.empty()
    except Exception as error:
        #print(error)
        raise error
    time.sleep(1)
   
def convolution_setup(N):
    global convolution_filter
    flt = []
    for t in range(0, N):
        flt.append([])
        for u in range(0, N):
            flt[t].append([0.0, 0.0])
    for t in range(0, N):
        for u in range(0, N):
            flt[u][t][0] = math.cos((2.0 * math.pi * u * t) / N)
            flt[u][t][1] = -math.sin((2.0 * math.pi * u * t) / N)
    convolution_filter = flt.copy()

def convolute(x, X):
    x = x.copy()
    N = len(x)
    y = [0] * N
    r = [0] * N
    c = [0] * N
    for i in range(0, N):
        for j in range(0, N):
            r[i] += x[j] * X[j][i][0]
            c[i] += x[j] * X[j][i][1]
    for i in range(0, N):
        y[i] = complex(r[i], c[i])
    return y

def deconvolute(y, Y):
    y = y.copy()
    N = len(y)
    x = [0] * N
    for i in range(0, N):
        for j in range(0, N):
            t = Y[j][i][0]
            t -= Y[j][i][1]
            x[i] += y[j].real * t * (1 / N)
    return x

def integral_fourier_setup(N):
    global integral_fourier_filter_fwd
    global integral_fourier_filter_inv
    fwd = [0] * N
    inv = [0] * N
    for t in range(0, N):
        for u in range(0, N):
            fwd[t] = cmath.exp((0-1j * 2.0 * math.pi * u * t))
            inv[t] = cmath.exp((0+1j * 2.0 * math.pi * u * t))
    integral_fourier_filter_fwd = fwd.copy()
    integral_fourier_filter_inv = inv.copy()

def integrate(x, X):
    x = x.copy()
    N = len(x)
    y = [0] * N
    r = [0] * N
    c = [0] * N
    for i in range(0, N):
        x[i] *= X[i]
    y[0] = x[0]
    for i in range(1, N):
        r[i] = x[i - 1].real + (0.5 * (x[i].real - x[i - 1].real))
        c[i] = x[i - 1].imag + (0.5 * (x[i].imag - x[i - 1].imag))
        y[i] = complex(r[i], c[i])
    return y
    
def differentiate(y, Y):
    y = y.copy()
    N = len(y)
    x = [0] * N
    r = [0] * N
    c = [0] * N
    x[0] = y[0]
    for i in range(1, N):
        r[i] = 0.5 * ((4.0 * y[i].real) - (2.0 * x[i - 1].real))
        c[i] = 0.5 * ((4.0 * y[i].imag) - (2.0 * x[i - 1].imag))
        x[i] = complex(r[i], c[i])
    for i in range(0, N):
        x[i] *= Y[i]
    return x

def test():
    x = [0, 1, 2, 3, 4, 5, 6]
    #f = [1, 1, 1, 1, 1, 1, 1]
    #b = [1, 1, 1, 1, 1, 1, 1]
    #x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    #f = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    #b = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    x = [0.0+0.0j, 1.0+1.0j, 2.0+2.0j, 3.0+3.0j, 4.0+4.0j, 5.0+5.0j, 6.0+6.0j]
    f = [0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j]
    b = [0.0-0.5j, 0.0-0.5j, 0.0-0.5j, 0.0-0.5j, 0.0-0.5j, 0.0-0.5j, 0.0-0.5j]
    y = integrate(x, f)
    z = differentiate(y, b)
    #integral_fourier_setup(len(x))
    #y = integrate(x, integral_fourier_filter_fwd)
    #z = differentiate(y, integral_fourier_filter_inv)
    #convolution_setup(len(x))
    #y = convolute(x, convolution_filter)
    #z = deconvolute(y, convolution_filter)
    print(x, y, z, sep = "\n")

if __name__ == "__main__":
    #test()
    setup()
    while True:
        loop()
