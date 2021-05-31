import hashlib
import os


def hash_preimage(target_string):
    if not all([x in '01' for x in target_string]):
        print("Input should be a string of bits")
        return
    l = len(target_string)
    while True:
        nonce = os.urandom(20)
        sha_y = hashlib.sha256(nonce)
        hashy = sha_y.hexdigest().encode('utf-8')
        bity = bin(int(hashy, 16))
        if bity[-l:] == target_string:
            break
    return(nonce)
