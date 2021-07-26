from zksk import Secret, DLRep
from zksk import utils

def ZK_equality(G,H):
    #generator G, publick key H (elliptic curve points)
    #Generate two El-Gamal ciphertexts (C1,C2) and (D1,D2)
    r1 = Secret(utils.get_random_num(bits=128))
    r2 = Secret(utils.get_random_num(bits=128))

    m = Secret(1)
    C1 = r1.value * G
    C2 = m * G + r1.value * H

    D1 = r2.value * G
    D2 = m*G + r2.value*H
    # stmt = DLRep(C1, r1 * H, simulated=True) | DLRep(C1 - G, r1 * H) | (DLRep(C2, r2 * H, simulated=True) | DLRep(C2 - G, r2 * H))
    stmt = DLRep(C1, r1 * H) and DLRep(C2 , r1 * H + m*G) and DLRep(D1, r2 * H) and DLRep(D2, r2 * H + m*G)

    # print(stmt)
    zk_proof = stmt.prove()
    #Generate a NIZK proving equality of the plaintexts

    #Return two ciphertexts and the proof
    return (C1,C2), (D1,D2), zk_proof


