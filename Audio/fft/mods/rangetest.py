import time

print("loading")

N = 2048
A = []
B = []
C = []

for i in range(0, N):
    A.append([])
    B.append([])
    C.append([])
    for j in range(0, N):
        A[i].append(0.0)
        B[i].append(0.0)
        C[i].append(0.0)

print("start")

t = time.monotonic()

for i in range(0, N):
    for j in range(0, N):
        A[i][j] = complex(i, j)

t = time.monotonic() - t

print(t)

i = 0
j = 0
arange = range(0, N)
brange = range(0, N)

t = time.monotonic()

for i in arange:
    for j in brange:
        B[i][j] = complex(i, j)

t = time.monotonic() - t

print(t)

f = lambda i, j: complex(i, j)

t = time.monotonic()

C = [[f(i, j) for j in range(0, N)] for i in range(0, N)]

t = time.monotonic() - t

print(t)

#print(A)
#print(B)
#print(C)
