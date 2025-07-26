# -*- coding: utf-8 -*-
"""
Bitcoin Transaction Signature Analyzer 
Author: https://github.com/8891689
"""
import sys
import hashlib
import argparse
import json
from urllib import request, error
from io import BytesIO

def setup_arg_parser():
    """Sets up the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="A tool to extract ECDSA signature components (r, s, z) from a Bitcoin transaction.",
        epilog="BTC Tip Jar: bc1qt3nh2e6gjsfkfacnkglt5uqghzvlrr6jahyj2k"
    )
    parser.add_argument("-d", "--txid", help="Transaction ID. Fetches the raw transaction from a public API.", type=str)
    parser.add_argument("-x", "--rawtx", help="The full raw transaction in hexadecimal format.", type=str)
    return parser

def fetch_raw_tx_from_api(txid: str) -> str:
    """Fetches raw transaction hex from a block explorer API."""
    url = f"https://blockstream.info/api/tx/{txid}/hex"
    print(f"Fetching raw transaction for txid: {txid}...")
    try:
        with request.urlopen(url, timeout=20) as response:
            if response.status == 200:
                print("Successfully fetched raw transaction.")
                return response.read().decode('utf-8')
            else:
                print(f"Error: API returned status code {response.status}")
    except error.URLError as e:
        print(f"Network error: Unable to connect to API. Details: {e.reason}")
    sys.exit(1)

class TxDataStream:
    """A stream-like reader for raw transaction hex data."""
    def __init__(self, raw_hex: str):
        self._stream = BytesIO(bytes.fromhex(raw_hex))

    def read_bytes(self, num_bytes: int) -> bytes:
        data = self._stream.read(num_bytes)
        if len(data) < num_bytes:
            raise EOFError("Stream ended unexpectedly.")
        return data

    def read_hex(self, num_bytes: int) -> str:
        return self.read_bytes(num_bytes).hex()

    def read_varint(self) -> int:
        val = int.from_bytes(self.read_bytes(1), 'little')
        if val < 0xfd:
            return val
        if val == 0xfd:
            return int.from_bytes(self.read_bytes(2), 'little')
        if val == 0xfe:
            return int.from_bytes(self.read_bytes(4), 'little')
        if val == 0xff:
            return int.from_bytes(self.read_bytes(8), 'little')
        
    def get_remaining_data_hex(self) -> str:
        return self._stream.read().hex()

def parse_der_signature(der_sig_bytes: bytes) -> (str, str):
    """
    Parses a DER-encoded signature to extract r and s values.
    """
    if der_sig_bytes[0] != 0x30:
        raise ValueError("Signature is not a valid DER sequence.")
    
    r_marker_pos = 2
    if der_sig_bytes[r_marker_pos] != 0x02:
        raise ValueError("R component marker not found.")
    r_len = der_sig_bytes[r_marker_pos + 1]
    r_start = r_marker_pos + 2
    r_val = der_sig_bytes[r_start : r_start + r_len]
    
    s_marker_pos = r_start + r_len
    if der_sig_bytes[s_marker_pos] != 0x02:
        raise ValueError("S component marker not found.")
    s_len = der_sig_bytes[s_marker_pos + 1]
    s_start = s_marker_pos + 2
    s_val = der_sig_bytes[s_start : s_start + s_len]
    
    if r_val.startswith(b'\x00'): r_val = r_val[1:]
    if s_val.startswith(b'\x00'): s_val = s_val[1:]

    return r_val.hex(), s_val.hex()


def double_sha256_hex(hex_str: str) -> str:
    """Computes the double SHA-256 hash and returns a hex string."""
    hash1 = hashlib.sha256(bytes.fromhex(hex_str)).digest()
    hash2 = hashlib.sha256(hash1).digest()
    return hash2.hex()

def hash160_hex(hex_str: str) -> str:
    """Computes the HASH160 and returns a hex string."""
    sha_hash = hashlib.sha256(bytes.fromhex(hex_str)).digest()
    ripemd_hash = hashlib.new('ripemd160', sha_hash).hexdigest()
    return ripemd_hash

def analyze_transaction_signatures(raw_tx_hex: str):
    """
    Analyzes a raw transaction to extract signature components for each input.
    """
    stream = TxDataStream(raw_tx_hex)
    
    version_hex = stream.read_hex(4)

    possible_marker = stream._stream.read(2)
    if possible_marker == b'\x00\x01':
        print("Unsupported Transaction Type: SegWit transactions are not handled.")
        sys.exit(1)
    
    stream._stream.seek(stream._stream.tell() - 2)

    input_count = stream.read_varint()
    
    inputs_data = []
    for _ in range(input_count):
        prev_txid_rev = stream.read_hex(32)
        output_index_hex = stream.read_hex(4)
        
        script_len = stream.read_varint()
        script_stream = TxDataStream(stream.read_hex(script_len))
        
        sig_pushdata_len = script_stream.read_varint()
        full_sig_bytes = script_stream.read_bytes(sig_pushdata_len)
        
        der_sig_bytes = full_sig_bytes[:-1]
        r, s = parse_der_signature(der_sig_bytes)
        
        pubkey_pushdata_len = script_stream.read_varint()
        pubkey_hex = script_stream.read_hex(pubkey_pushdata_len)

        sequence = stream.read_hex(4)
        
        inputs_data.append({
            "prev_tx": prev_txid_rev,
            "prev_out_index": output_index_hex,
            "pubkey": pubkey_hex,
            "sequence": sequence,
            "r": r,
            "s": s
        })
    
    outputs_and_locktime = stream.get_remaining_data_hex()
    
    base_tx_part1 = f"{version_hex}{input_count:02x}"
    base_tx_part3 = f"{outputs_and_locktime}01000000"

    for i, data in enumerate(inputs_data):
        middle_part = ""
        for j, other_data in enumerate(inputs_data):
            middle_part += other_data["prev_tx"]
            middle_part += other_data["prev_out_index"]
            if i == j:
                pubkey_hash = hash160_hex(data["pubkey"])
                script_pubkey = f"76a914{pubkey_hash}88ac"
                middle_part += f"{len(bytes.fromhex(script_pubkey)):02x}{script_pubkey}"
            else:
                middle_part += "00"
            middle_part += other_data["sequence"]

        tx_to_sign = base_tx_part1 + middle_part + base_tx_part3
        data['z'] = double_sha256_hex(tx_to_sign)
    
    return inputs_data

def main():
    parser = setup_arg_parser()
    args = parser.parse_args()

    if not args.txid and not args.rawtx:
        parser.print_help()
        sys.exit(1)

    raw_tx_hex = args.rawtx if args.rawtx else fetch_raw_tx_from_api(args.txid)
    
    if not raw_tx_hex:
        print("Could not obtain raw transaction data. Exiting.")
        return

    print("\nAnalyzing Transaction...")
    analysis_results = analyze_transaction_signatures(raw_tx_hex)

    for i, result in enumerate(analysis_results):
        print("=" * 70)
        print(f"[Input Index #: {i}]")
        print(f"     R: {result['r']}")
        print(f"     S: {result['s']}")
        print(f"     Z: {result['z']}")
        print(f"PubKey: {result['pubkey']}")
        
    print("=" * 70)
    print("\nAnalysis complete.")

if __name__ == '__main__':
    main()
