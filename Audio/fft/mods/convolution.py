import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import cmath
import math
import time

import simplified
import complicated

import ctypes
dll = ctypes.cdll.LoadLibrary("complicated_dll.dll")

transform_modes = \
{
    "NULL": 0,
    "FFT": 1,
    "SIMPLIFIED": 2,
    "COMPLICATED": 3,
}

filter_modes = \
{
    "NULL": 0,
    "BRICKWALL": 1,
    "GAUSSIAN": 2,
    "MODIFIED": 3,
}

playback_modes = \
{
    "LIVE": 0,
    "BUFFERED": 1,
}

mode = 2

if mode == 1:
    playback_mode = playback_modes["LIVE"]
    forward_mode = transform_modes["FFT"]
    filter_mode = filter_modes["MODIFIED"]
    reverse_mode = transform_modes["FFT"]
if mode == 2:
    playback_mode = playback_modes["BUFFERED"]
    forward_mode = transform_modes["COMPLICATED"]
    filter_mode = filter_modes["GAUSSIAN"]
    reverse_mode = transform_modes["COMPLICATED"]

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
            if playback_mode == playback_modes["LIVE"]:
                data = pre(data)
            if playback_mode == playback_modes["BUFFERED"]:
                pass
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
    if len(output) == 0:
        return output
    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])

        if forward_mode == transform_modes["NULL"]:
            pass
        if forward_mode == transform_modes["FFT"]:
            dat = np.fft.fft(dat)
        if forward_mode == transform_modes["SIMPLIFIED"]:
            dat = simplified.convolute(dat)
        if forward_mode == transform_modes["COMPLICATED"]:
            dat = complicated.dll_convolute(dat)

        if filter_mode == filter_modes["NULL"]:
            pass
        if filter_mode == filter_modes["BRICKWALL"]:
            nn = int(n / 16)
            for i in range(nn, 15 * nn):
                dat[i] *= 0.0
        if filter_mode == filter_modes["GAUSSIAN"]:
            gain = 0.1
            for i in range(1, n):
                p = -pow(dat[i], 2) / 2
                p = complex(min(max(p.real, -3.5), 3.5),
                            min(max(p.imag, -3.5), 3.5))
                dat[i] *= cmath.exp(p) * gain
                dat[i] = complex(min(max(dat[i].real, -3.5), 3.5),
                                 min(max(dat[i].imag, -3.5), 3.5))
        if filter_mode == filter_modes["MODIFIED"]:
            qual = 3
            band = 10
            freq = 0
            gain = -1.0
            start = 1.0
            for i in range(1, n):
                dat[i] *= start - pow(5, -abs(pow(dat[i] - freq, band)) / qual) * gain

        if reverse_mode == transform_modes["NULL"]:
            pass
        if reverse_mode == transform_modes["FFT"]:
            dat = np.fft.ifft(dat)
        if reverse_mode == transform_modes["SIMPLIFIED"]:
            dat = simplified.unwind(dat)
        if reverse_mode == transform_modes["COMPLICATED"]:
            dat = complicated.dll_unwind(dat)
        
        for i in range(0, n):
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
            #q = queue.Queue()
            progress = 0.0
            while len(data):
                data = file.read(bsz)
                #print("pre")
                if playback_mode == playback_modes["LIVE"]:
                    pass
                if playback_mode == playback_modes["BUFFERED"]:
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
   
if __name__ == "__main__":
    while True:
        main()
