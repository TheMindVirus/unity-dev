hexmap = "0123456789ABCDEF"

def ToHexStr(data, cols = 16):
    hexstr = ""
    for i in range(0, len(data)):
        hi = hexmap[(data[i] >> 4) & 15]
        lo = hexmap[data[i] & 15]
        hexstr += hi + lo
        if i % cols == cols - 1:
            hexstr += "\n"
    return hexstr

def FromHexStr(hexstr):
    data = []
    hexstr = "".join(x for x in hexstr if x in hexmap)
    for i in range(0, len(hexstr), 2):
        item = 0
        if hexstr[i] in hexmap:
            item += hexmap.index(hexstr[i]) << 4
        if hexstr[i + 1] in hexmap:
            item += hexmap.index(hexstr[i + 1])
        data.append(item)
    return data

A = [100, 200, 255, 20, 6, 0, 5, 10] # Array of Bytes Never Above 255 (0xFF)
A += A
A += A
B = ToHexStr(A)
C = FromHexStr(B)

print(A)
print(B)
print(C)

D = \
"""
7B0A202020202261223A0A202020207B
0A20202020202020202262223A20322C
0A20202020202020202263223A202254
68726565220A202020207D0A7D
"""
E = FromHexStr(D)
F = "".join(chr(x) for x in E)
print(chr(119))

print(D)
print(E)
print(F)

G = "7B2261223A7B2262223A322C2263223A225468726565227D7D"
H = FromHexStr(G)
I = "".join(chr(x) for x in H)

print(G)
print(H)
print(I)
