import hashlib
import os


def hash_collision(k):
    if not isinstance(k, int):
        print("hash_collision expects an integer")
        return(b'\x00', b'\x00')
    if k < 0:
        print("Specify a positive number of bits")
        return(b'\x00', b'\x00')

    # Collision finding code goes here
    x = os.urandom(20)

    # strx = bytes.fromhex(x)
    # stry = bytes.fromhex(y)
    sha_x = hashlib.sha256(x)
    hashx = sha_x.hexdigest().encode('utf-8')
    bitx = bin(int(hashx, 16))
    # byte_x = x.encode('utf-8')
    while True:
        y = os.urandom(20)
        sha_y = hashlib.sha256(y)
        hashy = sha_y.hexdigest().encode('utf-8')
        bity = bin(int(hashy, 16))
        if bity[-k:] == bitx[-k:]:
            break

    print(bitx, bity)
    return(x, y)
