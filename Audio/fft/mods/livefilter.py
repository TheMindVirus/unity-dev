import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time
import struct
import ctypes
dll = ctypes.cdll.LoadLibrary("live.dll")

live = True

ch = 2
bsz = 8 #16 #32 #64 #100 # 2048
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

class complex_data(ctypes.Structure):
    _fields_ = \
    [
        ("n", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte))
    ]

dll.convolute.argtypes = \
[
    ctypes.POINTER(complex_data),
    ctypes.POINTER(complex_data)
]
dll.convolute.restype = ctypes.POINTER(complex_data)

def dll_convolute(x):
    N = len(x)
    T = ctypes.c_ubyte * (N * 8)
    bstr = b''
    for i in range(0, N):
        bstr += struct.pack("<ff", x[i].real, x[i].imag)
    params = complex_data()
    result = complex_data()
    params.n = N
    params.data = T(*bstr)
    result2 = dll.convolute(ctypes.byref(params), ctypes.byref(result))
    y = [0] * result2.contents.n
    for i in range(0, result2.contents.n):
        j = i * 8
        c = struct.unpack("<ff", bytearray(result2.contents.data[j:j+8]))
        y[i] = complex(c[0], c[1])
    return y

def dsp(output, frames, time, status):
    global qpos
    assert frames == bsz
    if status.output_underflow:
        raise sd.CallbackAbort
    assert not status
    try:
        if qpos < len(q.queue):
            data = q.queue[qpos]
            if live:
                data = pre(data.copy())
            qpos += 1
        else:
            data = []
            evt.set()
    except queue.Empty as error:
        raise sd.CallbackAbort from error
    if len(data) < len(output):
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
        dat = dll_convolute(dat)
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
            file = sf.SoundFile("../Bubblegum.mp3")
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
            progress = 0.0
            while len(data):
                data = file.read(bsz)
                if not live:
                    data = pre(data.copy())
                q.put_nowait(data)
                progress += (bsz / file.frames) * 100
                print(str("{:0.2f}".format(progress)) + "%")
                if progress >= ready:
                    full = True
                    break
            print("done?")

        stream.stop()
        stream.start()
        evt.wait()
        evt.clear()
        qpos = 0
    except Exception as error:
        raise error
   
if __name__ == "__main__":
    while True:
        main()
