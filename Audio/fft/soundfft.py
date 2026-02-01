import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import math

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

    for k in range(0, len(output[0])):
        dat = []
        n = len(output)
        for i in range(0, n):
            dat.append(output[i][k])
        dat = np.fft.fft(dat)
        for i in range(0, n):
            if i > n / 16 and i < (n / 15) * 16:
                dat[i] *= 0.00 # Clippy Live Low Pass
        dat = np.fft.ifft(dat)
        for i in range(0, n):
            output[i][k] = dat[i].real

try:
    with sf.SoundFile("Bubblegum.mp3") as file:
        ch = file.channels
        sr = file.samplerate
        for i in range(0, sz):
            data = file.read(bsz)
            if not len(data):
                break
            q.put_nowait(data)
        stream = sd.OutputStream(samplerate = sr,
                                 blocksize = bsz,
                                 device = dev,
                                 channels = ch,
                                 callback = dsp)
        with stream:
            while len(data):
                data = file.read(bsz)
                q.put(data) #, timeout = bsz * sz / sr)
            evt.wait()
except queue.Full as error:
    raise error
