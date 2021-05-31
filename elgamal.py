import random

from params import p
from params import g


def keygen():
    q = (p-1)//2
    sk = random.randint(1, q)
    pk = pow(g, sk, p)
    return pk, sk


pk, sk = keygen()
# print(pk, sk)


def encrypt(pk, m):

    q = (p-1)//2
    r = random.randint(1, q)
    c1 = pow(g, r, p)
    c2 = (pow(pk, r, p) * (m % p)) % p
    return [c1, c2]


c = encrypt(pk, 10)

# print(c1)


def decrypt(sk, c):
    c1, c2 = c
    m = ((c2 % p) * (pow(pow(c1, sk, p), -1, p) % p)) % p
    return m


# m = decrypt(sk, c)
# print(m)
