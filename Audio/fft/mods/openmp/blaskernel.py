import threading
import numpy as np
import random
import cmath
import math
import time

from blaskernel_src import *

class task_data:
    def __init__(self, target):
        self.label = ""
        self.target = target
        self.n = pow(2, 20) - 1 #4096 #2048
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

def task_cython_blas(task):
    task.begin_profile("cython_blas")
    task.x = list(task.x)
    task.y = blas_fft(task.x)
    task.y = blas_ifft(task.y)
    task.end_profile()

def task_python_mac(task):
    task.begin_profile("python_mac")
    N = task.n
    D = 1.0 / N
    tmp_y = [0+0j] * N
    tmp_x = [0+0j] * N
    tau = 2.0 * math.pi
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            K = complex(math.cos(jin), -math.sin(jin))
            tmp_y[i] += task.x[j] * K
    for i in range(0, N):
        for j in range(0, N):
            jin = (tau * j * i) / N
            K = complex(math.cos(jin), math.sin(jin))
            tmp_x[i] += tmp_y[j] * K * D
    task.y = tmp_x.copy()
    task.end_profile()

p = profiler()
p.schedule(task_numpy_fft)
p.schedule(task_cython_blas)
#p.schedule(task_python_mac)
p.run()

"""
cython_blas 0.14100000000325963 seconds
numpy_fft 0.21899999998277053 seconds
"""

"""
python_mac DNF
"""
