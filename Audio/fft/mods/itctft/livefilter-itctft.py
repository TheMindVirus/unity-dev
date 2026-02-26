import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time
import struct

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

tau = 2.0 * math.pi

eq = \
{
    "c": 5.0,
    "b": 2.0,
    "f": 0.0,
    "q": bsz,
    "g": 1.0,
    "l": 0.0,
}

def ctft(data, N = 1.0):
    n = len(data[0])
    result = [[], []]
    for a in range(0, n):
        for b in range(0, n):
            ban = (tau * data[0][b] * data[0][a]) / N
            k = complex(math.cos(ban.real), -math.sin(ban.real))
            result[0].append([data[0][a], data[0][b]])
            result[1].append(data[1][b] * k)
    return result

def ictft(data, N = 1.0):
    n = len(data[0])
    result = [[], []]
    d = 1.0 / N
    for a in range(0, n):
        i = data[0][a][0]
        j = data[0][a][1]
        jin = (tau * j * i) / N
        k = complex(math.cos(jin.real), math.sin(jin.real))
        if j in result[0]:
            jdx = result[0].index(j)
            result[1][jdx] += data[1][a] * k * d
        else:
            result[0].append(j)
            result[1].append(data[1][a] * k * d)
    return result

def tctft(data, N = 1.0):
    result = ctft([data[1], data[0]], N)
    return result

def itctft(data, N = 1.0):
    result = ictft(data, N)
    return [result[1], result[0]]

def __repr_fft(data):
    n = len(data[0])
    result = [[], []]
    for i in range(0, n):
        if data[0][i][0] in result[0]:
            idx = result[0].index(data[0][i][0])
            result[1][idx] += data[1][i]
        else:
            result[0].append(data[0][i][0])
            result[1].append(data[1][i])
    return result

def __repr_ifft(data):
    n = len(data[0])
    result = [[], []]
    for a in range(0, n):
        for b in range(0, n):
            i = data[0][a]
            j = data[0][b]
            result[0].append([i, j])
            result[1].append(data[1][a])
    return result

def gauss(data, N, eq):
    n = len(data[0])
    for i in range(0, n):
        p = data[0][i]
        if p > N / 2:
            p = N - p
        data[1][i] *= (pow(eq["c"], (-abs(pow(p - eq["f"], eq["b"])) / eq["q"])) * eq["g"]) + eq["l"]
    return data

def continuous(data):
    n = len(data)
    result = [[], []]
    for i in range(0, n):
        result[0].append(i)
        result[1].append(data[i])
    return result

def discrete(data):
    n = len(data[0])
    result = []
    for i in range(0, n):
        alpha = data[0][i] % 1.0
        minus = 1.0 - alpha
        idx1 = int(data[0][i] - alpha)
        idx2 = int(idx1 + 1)
        if idx1 < len(result):
            result[idx1] += (alpha * data[1][i])
        else:
            nz = (1 + idx1) - len(result)
            result.extend([0] * nz)
            result[idx1] += (alpha * data[1][i])
        if idx2 < len(result):
            result[idx2] += (minus * data[1][i])
        else:
            nz = (1 + idx2) - len(result)
            result.extend([0] * nz)
            result[idx2] += (minus * data[1][i])
    return result

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

        mod = continuous(dat)
        
        mod = __repr_fft(ctft(mod, n))
        mod = gauss(mod, n, eq)
        mod = ictft(__repr_ifft(mod), n)

        #mod = __repr_fft(tctft(mod, n))
        #mod = gauss(mod, n, eq)
        #mod = itctft(__repr_ifft(mod), n)

        dat = discrete(mod)[:n]
        print(len(mod), len(mod[0]), len(mod[1]), len(dat), n)
        
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

if __name__ == "__main__":
    while True:
        main()
