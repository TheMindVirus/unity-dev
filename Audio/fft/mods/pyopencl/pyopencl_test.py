import pyopencl as cl
import numpy as np
import cmath
import math
import time

N = 7 #2048
N2 = N * N
xr = np.linspace(0, N - 1, N, dtype = np.float32)
#xr = np.random.random(N)
xi = np.zeros_like(xr)
yr = np.zeros_like(xr)
yi = np.zeros_like(xr)
zr = np.zeros_like(xr)
zi = np.zeros_like(xr)
tau = math.pi * 2.0
kr1 = [0] * N2
ki1 = [0] * N2
kr2 = [0] * N2
ki2 = [0] * N2
for i in range(0, N):
    for j in range(0, N):
        idx = (i * N) + j
        jin = cmath.exp((0-1j * tau * j * i) / N)
        kr1[idx] = jin.real
        ki1[idx] = jin.imag
        jin = cmath.exp((0+1j * tau * j * i) / N)
        kr2[idx] = jin.real
        ki2[idx] = jin.imag
kr1 = np.asarray(kr1, dtype = np.float32)
ki1 = np.asarray(ki1, dtype = np.float32)
kr2 = np.asarray(kr2, dtype = np.float32)
ki2 = np.asarray(ki2, dtype = np.float32)
tr = np.zeros_like(kr1)
ti = np.zeros_like(kr1)

#ctx = cl.create_some_context()
ctx = cl.Context(dev_type = cl.device_type.ALL)
dev = ctx.get_info(cl.context_info.DEVICES)
queue = cl.CommandQueue(ctx)
flags = cl.mem_flags

bXr = cl.Buffer(ctx, flags.READ_WRITE, xr.nbytes)
bXi = cl.Buffer(ctx, flags.READ_WRITE, xi.nbytes)
bKr = cl.Buffer(ctx, flags.READ_WRITE, kr1.nbytes)
bKi = cl.Buffer(ctx, flags.READ_WRITE, ki1.nbytes)
bTr = cl.Buffer(ctx, flags.READ_WRITE, tr.nbytes)
bTi = cl.Buffer(ctx, flags.READ_WRITE, ti.nbytes)
bYr = cl.Buffer(ctx, flags.READ_WRITE, yr.nbytes)
bYi = cl.Buffer(ctx, flags.READ_WRITE, yi.nbytes)

n = np.asarray([N])
bN = cl.Buffer(ctx, flags.READ_WRITE, n.nbytes)

code = ""
with open("main.cl", "r") as file:
    code = file.read()

program = cl.Program(ctx, code)
#err = program.build()
#print(type(err))
#if err != cl.status_code.SUCCESS:
#    raise err
self = program.build()
log = self.get_build_info(dev[0], cl.program_build_info.LOG)
print(log)

test_fft = getattr(program, "test_fft")
test_ifft = getattr(program, "test_ifft")
test_krn_fft = getattr(program, "test_krn_fft")
test_krn_ifft = getattr(program, "test_krn_ifft")

t = time.monotonic()
cl.enqueue_copy(queue, bXr, xr)
cl.enqueue_copy(queue, bXi, xi)
cl.enqueue_copy(queue, bKr, kr1)
cl.enqueue_copy(queue, bKi, ki1)
cl.enqueue_copy(queue, bYr, yr)
cl.enqueue_copy(queue, bYi, yi)
queue.finish()
test_fft(queue, (N,), None, bXr, bXi, bKr, bKi, bYr, bYi)
cl.enqueue_copy(queue, yr, bYr)
cl.enqueue_copy(queue, yi, bYi)
queue.finish()
cl.enqueue_copy(queue, bXr, yr)
cl.enqueue_copy(queue, bXi, yi)
cl.enqueue_copy(queue, bKr, kr2)
cl.enqueue_copy(queue, bKi, ki2)
cl.enqueue_copy(queue, bYr, zr)
cl.enqueue_copy(queue, bYi, zi)
queue.finish()
test_ifft(queue, (N,), None, bXr, bXi, bKr, bKi, bYr, bYi)
cl.enqueue_copy(queue, zr, bYr)
cl.enqueue_copy(queue, zi, bYi)
queue.finish()
t = time.monotonic() - t

print("test_fft:", t, "seconds")
print(xr)
print(xi)
print(yr)
print(yi)
print(zr)
print(zi)
print()

xi = np.zeros_like(xr)
yr = np.zeros_like(xr)
yi = np.zeros_like(xr)
zr = np.zeros_like(xr)
zi = np.zeros_like(xr)
cl.enqueue_copy(queue, bXr, xr)
cl.enqueue_copy(queue, bXi, xi)
cl.enqueue_copy(queue, bYr, yr)
cl.enqueue_copy(queue, bYi, yi)
queue.finish()

t = time.monotonic()
cl.enqueue_copy(queue, bN, n)
cl.enqueue_copy(queue, bXr, xr)
cl.enqueue_copy(queue, bXi, xi)
cl.enqueue_copy(queue, bKr, kr1)
cl.enqueue_copy(queue, bKi, ki1)
cl.enqueue_copy(queue, bTr, tr)
cl.enqueue_copy(queue, bTi, ti)
cl.enqueue_copy(queue, bYr, yr)
cl.enqueue_copy(queue, bYi, yi)
queue.finish()
test_krn_fft(queue, (N2,), None, bN, bXr, bXi, bKr, bKi, bTr, bTi, bYr, bYi)
cl.enqueue_copy(queue, yr, bYr)
cl.enqueue_copy(queue, yi, bYi)
queue.finish()
cl.enqueue_copy(queue, bN, n)
cl.enqueue_copy(queue, bXr, yr)
cl.enqueue_copy(queue, bXi, yi)
cl.enqueue_copy(queue, bKr, kr2)
cl.enqueue_copy(queue, bKi, ki2)
cl.enqueue_copy(queue, bTr, tr)
cl.enqueue_copy(queue, bTi, ti)
cl.enqueue_copy(queue, bYr, zr)
cl.enqueue_copy(queue, bYi, zi)
queue.finish()
test_krn_ifft(queue, (N2,), None, bN, bXr, bXi, bKr, bKi, bTr, bTi, bYr, bYi)
cl.enqueue_copy(queue, zr, bYr)
cl.enqueue_copy(queue, zi, bYi)
queue.finish()
t = time.monotonic() - t

print("test_krn_fft:", t, "seconds")
print(xr)
print(xi)
print(yr)
print(yi)
print(zr)
print(zi)
print()

"""
test_fft: 5.655999999959022 seconds
[0.000e+00 1.000e+00 2.000e+00 ... 2.045e+03 2.046e+03 2.047e+03]
[0. 0. 0. ... 0. 0. 0.]
[ 2.09612800e+06 -1.02448083e+03 -1.02398853e+03 ... -1.02397644e+03
 -1.02398853e+03 -1.02448083e+03]
[      0.    667542.75  333771.22 ... -222513.33 -333771.22 -667542.75]
[-5.2511692e-04  9.9966788e-01  1.9994340e+00 ...  2.0449995e+03
  2.0460005e+03  2.0469995e+03]
[ 0.0000000e+00 -6.1035156e-05  6.1035156e-05 ...  0.0000000e+00
 -1.8310547e-04 -1.2207031e-04]

test_krn_fft: 0.07899999991059303 seconds
[0.000e+00 1.000e+00 2.000e+00 ... 2.045e+03 2.046e+03 2.047e+03]
[0. 0. 0. ... 0. 0. 0.]
[ 2.0961280e+06 -1.0244808e+03 -1.0239885e+03 ... -5.1647490e+03
 -5.7688794e+03 -6.1483984e+03]
[      0.    667542.75  333771.22 ... -225532.3  -335887.8  -668633.1 ]
[  2.5121975   1.4060874   3.1397605 ... 778.2772    875.291
 973.6605   ]
[ 1128.3469     -16.23761    -18.198608 ... -1661.1135   -1693.2285
 -1707.5679  ]
"""
