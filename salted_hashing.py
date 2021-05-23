import hashlib
import os


def myhash(m):
    # Generate random nonce
    nonce = hashlib.sha256(str(m).encode('utf-8'))
    # Generate hex digest
    r = nonce.hexdigest()
    s = r + m
    h_hex = hashlib.sha256(str(s).encode('utf-8')).hexdigest()
    return nonce, h_hex


data = "Chopper"
print(myhash(data))
a, b = myhash(data)
print(len(b))
