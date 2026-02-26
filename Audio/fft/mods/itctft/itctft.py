import math

x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
y = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

#x = [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0]
#y = [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0]

data = [x, y]
N = 7.0

tau = 2.0 * math.pi

def ctft(data, N = 1.0):
    n = len(data[0])
    result = [[], []]
    for a in range(0, n):
        for b in range(0, n):
            ban = (tau * data[0][b] * data[0][a]) / N
            k = complex(math.cos(ban), -math.sin(ban))
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
        k = complex(math.cos(jin), math.sin(jin))
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

Adata = __repr_fft(ctft(data, N))
Bdata = ictft(__repr_ifft(Adata), N)

Tdata = tctft(data, N)
Odata = itctft(Tdata, N)

print(Adata)
print(Bdata)

print(__repr_fft(Tdata))
print(Odata)
