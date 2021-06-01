from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256

def sign(m):
	#generate public key
	#Your code here
    
    
    d = keys.gen_private_key(curve.secp256k1)
    public_key = keys.get_public_key(d, curve.secp256k1)
    print(public_key)
    #generate signature
    #Your code here
    
#     k = keys.gen_private_key(curve.secp256k1.G.curve)
#     x1, y1 = k * G
    
#     r = x1 % n
#     z = int(sha256(m.encode()).hexdigest(),16)
#     s = (z + r * d) % n
    r, s = ecdsa.sign(m, d, hashfunc=sha256, curve=curve.secp256k1)
    valid = ecdsa.verify((r, s), m, public_key, hashfunc=sha256, curve=curve.secp256k1)
    
#     print("%%%%%%%%%%%%%%%%", point.Point)
    
#     print("&&&&&&&&&&", r)
#     print("****************", s)

    assert isinstance( public_key, point.Point )
    assert isinstance( r, int )
    assert isinstance( s, int )
    return( public_key, [r,s] )

sign("I")

