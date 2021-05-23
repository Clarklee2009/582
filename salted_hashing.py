import hashlib
import os


def myhash(m):
    # Generate random nonce
    nonce = hashlib.sha256(str(m).encode('utf-8'))
    # Generate hex digest
    h_hex = nonce.hexdigest()
    return nonce, h_hex


# data = "Chopper"
# print(myhash(data))
