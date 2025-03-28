def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m

p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

r  = 0xaa03ea5459a1f3e4cbd4cc294c35f539dd6d4ca9070249dbd905610e835f7fea

s1 = 0x556f71f86a08a9bea27a4b11e44966011eca08a5e8ec370e76bdd8cbc4ceb0b9
s2 = 0x556f71f86a08a9bea27a4b11e44966011eca08a5e8ec370e76bdd8cbc4ceb0b9

z1 = 0xd5a179e8ad7e4e042ad4d0b2465aa1a10b180713f02ac965cfc919009731d4a9
z2 = 0x866674068d62c4baa3fbe4565d3ae65289f30e42adfcc63169811487a3be7c8b


print (hex(((z1*s2 - z2*s1) * modinv((r*(s1-s2)),p)) % p))
