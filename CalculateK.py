def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist for a={a} and m={m}. GCD is {g}.")
    return x % m

def extended_gcd(a, b):
    lastremainder, remainder = abs(a), abs(b)
    x, lastx = 0, 1
    y, lasty = 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)

def compute_k(r, s, Z, n):
    r_inv = modinv(r, n)
    k = (s * r + Z) * r_inv % n
    return k

# Example values (replace these with actual values)
r = 0xaa03ea5459a1f3e4cbd4cc294c35f539dd6d4ca9070249dbd905610e835f7fea
s = 0x556f71f86a08a9bea27a4b11e44966011eca08a5e8ec370e76bdd8cbc4ceb0b9
Z = 0xd5a179e8ad7e4e042ad4d0b2465aa1a10b180713f02ac965cfc919009731d4a9
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Calculate k
k = compute_k(r, s, Z, n)
print(f"Random number k: {hex(k)}")

