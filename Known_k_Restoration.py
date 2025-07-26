# -*- coding: utf-8 -*-
"""
ECDSA Private Key Recovery from a Known 'k' Nonce
Author: https://github.com/8891689
"""

def recover_private_key_from_known_nonce(signature: dict, nonce: int, curve_order: int) -> int:
    """
    Recovers the ECDSA private key (d) when the random nonce 'k' used for
    signing is known.

    Args:
        signature: A dictionary containing the signature components 'r', 's', and 'z'.
        nonce: The known random nonce 'k' used to generate the signature.
        curve_order: The order of the elliptic curve (a large prime number 'n').

    Returns:
        The calculated private key as an integer.
    """
    
    r = signature['r']
    s = signature['s']
    z = signature['z']

    try:
        r_inverse = pow(r, -1, curve_order)
    except ValueError:

        raise ValueError("Modular inverse of 'r' does not exist. Cannot recover key.")

    s_times_k = (s * nonce) % curve_order
    s_k_minus_z = (s_times_k - z) % curve_order
    
    private_key = (s_k_minus_z * r_inverse) % curve_order
    
    return private_key

def format_hex(number: int, length: int = 64) -> str:
    """
    Formats an integer as a hexadecimal string, removing the '0x' prefix
    and padding with leading zeros to the specified length.
    """
    return f"{number:0{length}x}"

if __name__ == '__main__':

    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

    R = 0x83fe1c06236449b69a7bee5be422c067d02c4ce3f4fa3756bd92c632f971de06
    S = 0x7405249d2aa9184b688f5307006fddc3bd4a7eb89294e3be3438636384d64ce7
    Z = 0x070239c013e8f40c8c2a0e608ae15a6b1bb4b8fbcab3cff151a6e4e8e05e10b7
    K = 0x070239C013E8F40C8C2A0E608AE15A6B23D4A09295BE678B21A5F1DCEAE1F634
    
    signature_data = {'r': R, 's': S, 'z': Z}
    
    print("--- Recovering ECDSA Private Key with a Known Nonce 'k' ---")

    try:
        recovered_key = recover_private_key_from_known_nonce(signature_data, K, N)
        
        print(f"Recovered Key: {format_hex(recovered_key)}")

    except ValueError as e:
        print(f"Error during calculation: {e}")
