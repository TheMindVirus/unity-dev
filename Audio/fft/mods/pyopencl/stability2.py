import numpy as np
import main as filters
import time

n = 2048
x = [0,1,2,3,4,5,6]
x = list(np.linspace(0, n - 1, n))
N = len(x)
y = filters.test(N)

while True:
    y = [0] * N
    t = time.monotonic()
    y = filters.test_fft(x)
    t = time.monotonic() - t
    print("test_fft:", t, "seconds")
    z = [0] * N
    t = time.monotonic()
    z = filters.test_ifft(y)
    t = time.monotonic() - t
    print("test_ifft:", t, "seconds")
    
