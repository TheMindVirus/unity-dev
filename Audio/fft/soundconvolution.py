import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time

modes = \
{
    "NULL": 0,
    "FFT": 1,
    "CONVOLUTION_FOURIER": 2,
    "CONVOLUTION_CMATH": 3,
    "CONVOLUTION_ZERO": 4,
    "CONVOLUTION_ONE": 5,
    "CONVOLUTION_0+1J": 6,
    "CONVOLUTION_1+1J": 7,
    "CONVOLUTION_LAPLACE": 8,
    "CONVOLUTION_ABEL": 9,
    "CONVOLUTION_HILBERT": 10,
    "CONVOLUTION_MELLIN": 11,
    "CONVOLUTION_STRASS": 12,
}

mode = 2 #modes["FFT"]

ch = 2
bsz = 100 # 2048
sr = 44100
skip = 10000000
dev = None
file = None
stream = None
evt = threading.Event()
q = queue.Queue()
qpos = 0
full = False
progress = 0.0
ready = 0.5

def dsp(output, frames, time, status):
    global qpos
    assert frames == bsz
    if status.output_underflow:
        raise sd.CallbackAbort
    assert not status
    try:
        if qpos < len(q.queue):
            data = q.queue[qpos] #q.get_nowait()
            qpos += 1
        else:
            data = []
            evt.set()
    except queue.Empty as error:
        raise sd.CallbackAbort from error
    if len(data) < len(output):
        #output[:len(data)] = data
        #output[len(data):].fill(0)
        raise sd.CallbackStop
    else:
        output[:] = data

def pre(output):
    global pos
    if len(output) == 0:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])

        if mode == 1:
            dat = np.fft.fft(dat)
        if mode >= 2:
            dat = convolute(dat, convolution_filter_fwd)

        if (mode > 0):
            # Clippy Low Pass Formant Filter
            for i in range(0, n):
                if i > n / 16 and i < (n / 15) * 16:
                    dat[i] *= 0.00

        if mode == 1:
            dat = np.fft.ifft(dat)
        if mode >= 2:
            dat = deconvolute(dat, convolution_filter_inv)
        
        for i in range(0, n):
            output[i][k] = dat[i].real

    return output

def setup():
    print("Now Loading...")
    integral_abel_setup(bsz)
    convolution_setup(bsz)

def loop():
    global q, qpos, file, stream, progress, full, evt
    try:
        if not full:
            file = sf.SoundFile("Bubblegum.mp3")
            print(file)
            file.seek(skip, sf.SEEK_SET)
            ch = file.channels
            sr = file.samplerate
            data = [0] * bsz
            stream = sd.OutputStream(samplerate = sr,
                                     blocksize = bsz,
                                     device = dev,
                                     channels = ch,
                                     callback = dsp)
            stream.stop()
            #q = queue.Queue()
            progress = 0.0
            while len(data):
                data = file.read(bsz)
                #print("pre")
                data = pre(data)
                #print("post")
                q.put_nowait(data)
                progress += (bsz / file.frames) * 100
                print(str("{:0.2f}".format(progress)) + "%")
                if progress >= ready:
                    full = True
                    break
            print("done?")

        stream.stop()
        stream.start()
        #time.sleep(10)
        evt.wait()
        evt.clear()
        print("evt")
        #q.empty()
        qpos = 0
    except Exception as error:
        #print(error)
        raise error
    #time.sleep(1)
   
def convolution_setup(N):
    global convolution_filter_fwd, convolution_filter_inv
    global integral_abel_inv
    fwd = []
    inv = []
    for t in range(0, N):
        fwd.append([])
        inv.append([])
        for u in range(0, N):
            fwd[t].append([0.0, 0.0])
            inv[t].append([0.0, 0.0])
    for t in range(0, N):
        for u in range(0, N):
            if mode == 2:
                fwd[u][t][0] = math.cos((2.0 * math.pi * u * t) / N)
                fwd[u][t][1] = -math.sin((2.0 * math.pi * u * t) / N)
                inv[u][t][0] = math.cos((2.0 * math.pi * u * t) / N)
                inv[u][t][1] = math.sin((2.0 * math.pi * u * t) / N)
            if mode == 3:
                fwd[u][t][0] = cmath.exp((0-1j * 2.0 * math.pi * u * t) / N).real
                fwd[u][t][1] = cmath.exp((0-1j * 2.0 * math.pi * u * t) / N).imag
                inv[u][t][0] = cmath.exp((0+1j * 2.0 * math.pi * u * t) / N).real
                inv[u][t][1] = cmath.exp((0+1j * 2.0 * math.pi * u * t) / N).imag
            if mode == 4:
                fwd[u][t][0] = 0
                fwd[u][t][1] = 0
                inv[u][t][0] = 0
                inv[u][t][1] = 0
            if mode == 5:
                fwd[u][t][0] = 1
                fwd[u][t][1] = 0
                inv[u][t][0] = 1
                inv[u][t][1] = 0
            if mode == 6:
                fwd[u][t][0] = 0
                fwd[u][t][1] = 1
                inv[u][t][0] = 0
                inv[u][t][1] = 1
            if mode == 7:
                fwd[u][t][0] = 1
                fwd[u][t][1] = 1
                inv[u][t][0] = 1
                inv[u][t][1] = 1
            if mode == 8:
                fwd[u][t][0] = cmath.exp(-(u * t) / N).real
                fwd[u][t][1] = cmath.exp(-(u * t) / N).imag
                inv[u][t][0] = (cmath.exp((u * t) / N) / (0+1j * 2.0 * math.pi)).real
                inv[u][t][1] = (cmath.exp((u * t) / N) / (0+1j * 2.0 * math.pi)).imag
            if mode == 9:
                f = cmath.sqrt(pow(t, 2) - pow(u, 2))
                if f == 0:
                    f = 1
                fwd[u][t][0] = ((2.0 * t) / f).real
                fwd[u][t][1] = ((2.0 * t) / f).imag
                inv[u][t][0] = differentiate([integral_abel_inv[u][t]], [1])[0].real
                inv[u][t][1] = differentiate([integral_abel_inv[u][t]], [1])[0].imag
            if mode == 10:
                f = u - t
                if f == 0:
                    f = 1
                fwd[u][t][0] = ((1.0 / math.pi) * (1.0 / f)).real
                fwd[u][t][1] = ((1.0 / math.pi) * (1.0 / f)).imag
                inv[u][t][0] = ((1.0 / math.pi) * (1.0 / f)).real
                inv[u][t][1] = ((1.0 / math.pi) * (1.0 / f)).imag
            if mode == 11:
                if t == 0:
                    t = 1
                fwd[u][t][0] = pow(t, u - 1).real
                fwd[u][t][1] = pow(t, u - 1).imag
                inv[u][t][0] = (pow(t, u) * pow(0+1j * 2.0 * math.pi, -1)).real
                inv[u][t][1] = (pow(t, u) * pow(0+1j * 2.0 * math.pi, -1)).imag
            if mode == 12:
                try:
                    f = cmath.exp(pow(u - t, 2) / 4.0)
                except:
                    f = 1
                fwd[u][t][0] = (cmath.exp(-pow(u - t, 2) / 4.0) / math.sqrt(4.0 * math.pi)).real
                fwd[u][t][1] = (cmath.exp(-pow(u - t, 2) / 4.0) / math.sqrt(4.0 * math.pi)).imag
                inv[u][t][0] = (f * pow(0+1j * math.sqrt(4.0 * math.pi), -1)).real
                inv[u][t][1] = (f * pow(0+1j * math.sqrt(4.0 * math.pi), -1)).imag

    convolution_filter_fwd = fwd.copy()
    convolution_filter_inv = inv.copy()

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
            t += Y[j][i][1]
            x[i] += y[j].real * t * (1 / N)
    return x

def integral_abel_setup(N):
    global integral_abel_inv
    inv = []
    for t in range(0, N):
        inv.append([])
        for u in range(0, N):
            inv[t].append(0.0)
    for t in range(0, N):
        for u in range(0, N):
            f = (math.pi * cmath.sqrt(pow(u, 2) - pow(t, 2)))
            if f == 0:
                f = 1
            inv[u][t] = -1.0 / f
    integral_abel_inv = inv.copy()

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
    #x = [0, 1, 2, 3, 4, 5, 6]
    #f = [1, 1, 1, 1, 1, 1, 1]
    #b = [1, 1, 1, 1, 1, 1, 1]
    #x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    #f = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    #b = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    x = [0.0+0.0j, 1.0+1.0j, 2.0+2.0j, 3.0+3.0j, 4.0+4.0j, 5.0+5.0j, 6.0+6.0j]
    f = [0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j, 0.0+2.0j]
    b = [0.0-0.5j, 0.0-0.5j, 0.0-0.5j, 0.0-0.5j, 0.0-0.5j, 0.0-0.5j, 0.0-0.5j]
    integral_abel_setup(len(x))
    convolution_setup(len(x))
    y = convolute(x, convolution_filter_fwd)
    z = deconvolute(y, convolution_filter_inv)
    print(x, y, z, sep = "\n")

if __name__ == "__main__":
    #test()
    setup()
    while True:
        loop()
