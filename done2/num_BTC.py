import math

def num_BTC(b):
    c = float(0)
    integer = b // 210000
    v = 50
    if b <= 210000:
        c += v * b
    else:
        for i in range(integer):
            v = 50/(2**i)
            c += 210000 * v
        c += (b - integer * 210000) * v /2

    
    return c
print(num_BTC(13156))