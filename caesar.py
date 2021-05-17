
def encrypt(key, plaintext):
    ciphertext = ""
    # YOUR CODE HERE
    for i in plaintext:
        ciphertext += chr((ord(i) + key-65) % 26 + 65)
    return ciphertext


def decrypt(key, ciphertext):
    plaintext = ""
    # YOUR CODE HERE
    for i in ciphertext:
        plaintext += chr((ord(i) - key - 65) % 26 + 65)

    return plaintext
