def inverse_mod(a, m):
    """Calculate the modular inverse of a mod m."""
    if a < 0 or m <= a:
        a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod(d, c) + (c,)
        uc, vc, ud, vd = ud - q * uc, vd - q * vc, uc, vc

    assert d == 1
    return ud if ud > 0 else ud + m

def derivate_privkey(p, r, s1, s2, z1, z2):
    """Derive private key and k from the given parameters."""
    z = z1 - z2
    s = s1 - s2
    r_inv = inverse_mod(r, p)
    s_inv = inverse_mod(s, p)
    k = (z * s_inv) % p
    d = (r_inv * (s1 * k - z1)) % p
    return d, k

# Test values
z1 = 0xd5a179e8ad7e4e042ad4d0b2465aa1a10b180713f02ac965cfc919009731d4a9
s1 = 0x556f71f86a08a9bea27a4b11e44966011eca08a5e8ec370e76bdd8cbc4ceb0b9
r = 0x00aa03ea5459a1f3e4cbd4cc294c35f539dd6d4ca9070249dbd905610e835f7fea
z2 = 0x866674068d62c4baa3fbe4565d3ae65289f30e42adfcc63169811487a3be7c8b
s2 = 0x556f71f86a08a9bea27a4b11e44966011eca08a5e8ec370e76bdd8cbc4ceb0b9

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 

# Print results
d, k = derivate_privkey(p, r, s1, s2, z1, z2)
print("privatekey: {:x}".format(d))
print("k: {:x}".format(k))

