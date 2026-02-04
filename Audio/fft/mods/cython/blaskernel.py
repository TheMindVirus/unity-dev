import threading
import numpy as np
import random
import cmath
import math
import time

from _pocketfft_internal import execute as pfft
from blaskernel_src import *
import mingw32_dll
import blaskernel_cython as cpp_dll

class task_data:
    def __init__(self, target):
        self.label = ""
        self.target = target
        self.n = 7 #pow(2, 20) - 1 #4096 #2048
        self.x = np.linspace(1, self.n, self.n) - 1
        #self.x = np.random.random(self.n)
        self.y = np.zeros_like(self.x)
    def begin_profile(self, label):
        self.label = label
        self.t = time.monotonic()
    def end_profile(self):
        self.t = time.monotonic() - self.t
    def __repr__(self):
        return self.label
    def __lt__(self, other):
        return self.t < other.t
    def __gt__(self, other):
        return self.t > other.t

class profiler():
    def __init__(self):
        self.tasks = []
        self.order = []
    def schedule(self, task):
        self.tasks.append(task_data(task))
    def run(self):
        self.order = []
        for task in self.tasks:
            t = threading.Thread(target = task.target, args = (task,))
            t.start()
            t.join()
        self.order = sorted(self.tasks)
        for task in self.order:
            if task.n < 10:
                print(task.label, task.y)
            else:
                print(task.label, task.t, "seconds")

def task_numpy_fft(task): 
    task.begin_profile("numpy_fft")
    task.y = np.fft.fft(task.x)
    task.y = np.fft.ifft(task.y)
    task.end_profile()

def task_pfft_execute(task):
    task.begin_profile("pfft_execute")
    task.y = pfft(task.x, False, True, 1.0)
    task.y = pfft(task.y, False, False, 1.0 / task.n)
    task.end_profile()

def task_cython_blas(task):
    task.begin_profile("cython_blas")
    task.y = blas_fft(task.x)
    task.y = blas_ifft(task.y)
    task.end_profile()

def task_cpp_dll(task):
    task.begin_profile("cpp_dll")
    task.y = cpp_dll.wrap_fft(task.x)
    task.y = cpp_dll.wrap_ifft(task.y)
    task.end_profile()

def task_mingw32_dll(task):
    task.begin_profile("mingw32_dll")
    task.y = mingw32_dll.fft(task.x)
    task.y = mingw32_dll.ifft(task.y)
    task.end_profile()

def task_python_mac(task):
    task.begin_profile("python_mac")
    N = task.n
    D = 1.0 / N
    tmp = [0+0j] * N
    tmp2 = [0+0j] * N
    tau = 2.0 * math.pi
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            K = complex(math.cos(jin), -math.sin(jin))
            tmp[i] += task.x[j] * K
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            K = complex(math.cos(jin), math.sin(jin))
            tmp2[i] += tmp[j] * K * D
    task.y = tmp2.copy()
    task.end_profile()

p = profiler()
p.schedule(task_numpy_fft)
p.schedule(task_pfft_execute)
p.schedule(task_cython_blas)
p.schedule(task_cpp_dll)
p.schedule(task_mingw32_dll)
p.schedule(task_python_mac)
p.run()
