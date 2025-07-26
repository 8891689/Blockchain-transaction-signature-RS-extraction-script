# -*- coding: utf-8 -*-
"""
Private Key Recovery from Reused r Nonce 
Author: https://github.com/8891689
"""

def modular_inverse(n: int, prime: int) -> int:
    """
    Calculates the modular multiplicative inverse of n modulo a prime.
    """
    return pow(n, -1, prime)

def recover_private_key_from_reused_k(r, s1, s2, z1, z2, p):
    """
    Calculates the private key (d) given two signatures (s1, s2) that
    share the same random nonce 'k' (and thus the same 'r' value).    
    The formula is: d = (z1*s2 - z2*s1) * modinv(r*(s1-s2), p) mod p
    """
    
    s_diff = (s1 - s2) % p
    if s_diff == 0:
        raise ValueError("s1 and s2 cannot be the same, as it leads to division by zero.")
    
    denominator = (r * s_diff) % p
    
    term1 = (z1 * s2) % p
    term2 = (z2 * s1) % p
    numerator = (term1 - term2) % p
    
    inv_denominator = modular_inverse(denominator, p)
    
    private_key = (numerator * inv_denominator) % p
    
    return private_key

if __name__ == '__main__':
    
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    
    r = 0xfb1299738dc025ca0e2fdc140879513458b2e6bdc03a692fef4299ddfd359ef7
    
    s1 = 0x97af3747a2a4d04ab3dc0a1f101d258c4634cc49e4c29f5305e13780f7ec862d
    z1 = 0x54737b1ad70cf21757206164ed417f7a11dbc510116d9d6dc86f7d713fa5f250
   
    s2 = 0x96e3e090fc4ba12ec875caae59dc4bbeb8a39ff7ba9b2313b0452f07da3a455c
    z2 = 0x6ed90a1bda828e926cc9e4b1f6bc0bb04b535f1769bd61979fa562e4a7f95598

    print("--- Recovering ECDSA Private Key ---")
    
    try:
        d = recover_private_key_from_reused_k(r, s1, s2, z1, z2, p)
        
        print(f"Recovered key: 0x{d:064x}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
