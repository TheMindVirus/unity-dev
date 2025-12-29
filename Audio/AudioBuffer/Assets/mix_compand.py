def compand(a):
    if (a >= 0.0):
        return 1.0 - (0.5 * a)
    else:
        return 1.0 - (-0.5 * a)

def mix(a, b):
    return (a * compand(b)) + (b * compand(a))

a = 1.0
b = 1.0
c = 1.0
print(a, b, mix(a, b), c)

a = -1.0
b = -1.0
c = -1.0
print(a, b, mix(a, b), c)

a = 1.0
b = -1.0
c = 0.0
print(a, b, mix(a, b), c)

a = -1.0
b = 1.0
c = 0.0
print(a, b, mix(a, b), c)
