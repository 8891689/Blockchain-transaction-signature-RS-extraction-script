# author：8891689
import requests
import json
import sys
import hashlib
import base58
import re
from time import sleep

# RPC Connection Settings
RPC_USER = '8891689'
RPC_PASSWORD = '1111111111111111111111$ddbbda8cbc8c0a8cc32a84d0590f2de17f1f8dc798c4411111111111111111111'
RPC_PORT = '8332'
RPC_URL = f'http://127.0.0.1:{RPC_PORT}'

def wait_for_reconnect():
    # print("Please press 'P' to reconnect...") # Original Chinese print statement
    print("Please press 'P' to reconnect...") # English translation
    while True:
        user_input = input().strip().upper()
        if user_input == 'P':
            break

def rpc_request(method, params=None):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "1.0",
        "id": "python_rpc",
        "method": method,
        "params": params or []
    }
    for attempt in range(3):
        try:
            response = requests.post(
                RPC_URL,
                auth=(RPC_USER, RPC_PASSWORD),
                headers=headers,
                data=json.dumps(payload),
                timeout=10  # Set timeout period
            )
            response_data = response.json()
            if 'error' in response_data and response_data['error']:
                # print(f"RPC 错误: {response_data['error']}") # Original Chinese print statement
                print(f"RPC Error: {response_data['error']}") # English translation
                return None
            return response_data['result']
        except requests.exceptions.RequestException as e:
            # print(f"RPC 请求失败: {e}") # Original Chinese print statement
            print(f"RPC request failed: {e}") # English translation
            sleep(5)  # Wait 5 seconds before retrying after failure
    # print("所有重试已用尽") # Original Chinese print statement
    print("All retry attempts exhausted.") # English translation
    wait_for_reconnect()  # Wait for user to press 'P' to reconnect
    return rpc_request(method, params)  # Try the request again

def get_block_hash(block_height):
    # print(f"获取区块哈希: {block_height}") # Original Chinese print statement
    print(f"Getting block hash: {block_height}") # English translation
    return rpc_request('getblockhash', [block_height])

def get_block(block_hash):
    # print(f"获取区块数据: {block_hash}") # Original Chinese print statement
    print(f"Getting block data: {block_hash}") # English translation
    return rpc_request('getblock', [block_hash, 2]) # Verbosity level 2 for detailed block data

def get_transaction(txid):
    # print(f"获取交易数据: {txid}") # Original Chinese print statement
    print(f"Getting transaction data: {txid}") # English translation
    return rpc_request('getrawtransaction', [txid, True]) # True for verbose output

def extract_signatures_from_transaction(tx):
    signatures = []
    txid = None

    if not tx:
        return signatures, txid

    txid = tx.get('txid')

    # Skip coinbase transactions as they don't have standard inputs/signatures
    if 'vin' in tx and len(tx['vin']) > 0 and 'coinbase' in tx['vin'][0]:
        return signatures, txid

    for vin in tx.get('vin', []):
        if 'scriptSig' in vin and 'asm' in vin['scriptSig']:
            scriptSig_asm = vin['scriptSig']['asm']
            # Use regular expression to match signature R and S values (hex strings)
            matches = re.findall(r'([0-9a-fA-F]+)', scriptSig_asm)
            if len(matches) > 1:
                # Simple attempt to find DER encoded signature:
                # Find potential signature data by joining hex parts.
                # This is a basic approach and might not work for all script types.
                sig_data = ''.join(matches) # Concatenate matched parts
                try:
                    # Parse the signature (basic DER parsing attempt)
                    offset = 0
                    length = len(sig_data)
                    if sig_data[offset:offset+2] == '30':  # 0x30: Start of sequence
                        offset += 2
                        seq_len = int(sig_data[offset:offset+2], 16)  # Sequence length
                        offset += 2
                        # Check for R value
                        if sig_data[offset:offset+2] == '02':  # 0x02: Start of integer
                            offset += 2
                            r_len = int(sig_data[offset:offset+2], 16)  # R length
                            offset += 2
                            r = sig_data[offset:offset + r_len * 2]  # R value (hex)
                            offset += r_len * 2
                            # Check for S value
                            if sig_data[offset:offset+2] == '02':  # 0x02: Start of integer
                                offset += 2
                                s_len = int(sig_data[offset:offset+2], 16)  # S length
                                offset += 2
                                s = sig_data[offset:offset + s_len * 2]  # S value (hex)
                                signatures.append({'r': r, 's': s})
                except Exception as e:
                    # print(f"解析签名数据时发生错误: {e}") # Original Chinese print statement
                    print(f"Error parsing signature data: {e}") # English translation

    return signatures, txid

def print_progress(current, total):
    percent = (current / total) * 100
    bar_length = 40
    filled_length = int(round(bar_length * percent / 100))
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    # Use \r to return to the beginning of the line, overwriting the previous progress bar instead of creating a new line
    # print(f'\r进度: [{bar}] {percent:.2f}% 完成', end="") # Original Chinese print statement
    print(f'\rProgress: [{bar}] {percent:.2f}% Complete', end="") # English translation
    sys.stdout.flush()
    if current == total:
        print()  # Print a newline when progress is complete

def process_block(block_height, file_handle, recorded_txids): # recorded_txids is currently unused
    block_hash = get_block_hash(block_height)
    if not block_hash:
        # print(f"无法获取区块哈希: {block_height}") # Original Chinese print statement
        print(f"Could not get block hash for height: {block_height}") # English translation
        return

    block = get_block(block_hash)
    if not block:
        # print(f"无法获取区块数据: {block_height}") # Original Chinese print statement
        print(f"Could not get block data for hash: {block_hash} (height: {block_height})") # English translation
        return

    transactions = block.get('tx', [])

    for tx in transactions:
        # Handle both transaction objects (dict) and transaction IDs (str) if needed,
        # although getblock with verbosity 2 should return objects.
        if isinstance(tx, dict):
            txid = tx.get('txid')
        elif isinstance(tx, str):
            txid = tx # Assuming it's just the txid string
            # Note: If only txid string is provided, cannot extract signatures without another RPC call
        else:
            # print(f"未知交易格式: {tx}") # Original Chinese print statement
            print(f"Unknown transaction format: {tx}") # English translation
            continue

        if not isinstance(txid, str):
            # print(f"交易 ID 不是字符串类型: {txid}") # Original Chinese print statement
            print(f"Transaction ID is not a string: {txid}") # English translation
            continue

        # Removed deduplication check logic
        # if txid in recorded_txids:
        #     continue

        # Extract signatures only if we have the full transaction object
        signatures = []
        if isinstance(tx, dict):
            signatures, _ = extract_signatures_from_transaction(tx)
        # Else: Cannot extract signature from txid string alone here

        if signatures:
            # Record transaction ID and signatures
            file_handle.write(f"Transaction ID: {txid}\n")
            for sig in signatures:
                file_handle.write(f"  Signature - R: {sig['r']}, S: {sig['s']}\n")

            # Immediately flush the file buffer to ensure data is written, preventing data loss on crash
            file_handle.flush()

def main(start_block, end_block, output_file):
    if start_block < 0 or end_block < start_block:
        # print("错误: 区块范围不合法") # Original Chinese print statement
        print("Error: Invalid block range") # English translation
        sys.exit(1)

    total_blocks = end_block - start_block + 1

    try:
        # Open the output file in write mode ('w')
        with open(output_file, 'w') as file_handle:
            for current_block in range(start_block, end_block + 1):
                # Process each block, passing None for recorded_txids as deduplication is removed
                process_block(current_block, file_handle, None)
                # Update progress bar
                print_progress(current_block - start_block + 1, total_blocks)
    except Exception as e:
        # print(f"写入文件时发生错误: {e}") # Original Chinese print statement
        print(f"An error occurred while writing to the file: {e}") # English translation
        sys.exit(1)

    print()  # Add a newline to clear the progress bar line

if __name__ == "__main__":
    if len(sys.argv) != 4:
        # print("用法: python3 extract_data.py <start_block> <end_block> <output_file>") # Original Chinese print statement
        print("Usage: python3 extract_data.py <start_block> <end_block> <output_file>") # English translation
        sys.exit(1)

    try:
        start_block = int(sys.argv[1])
        end_block = int(sys.argv[2])
        output_file = sys.argv[3]
    except ValueError:
        # print("区块高度参数无效，请输入整数。") # Original Chinese print statement
        print("Invalid block height arguments. Please provide integers.") # English translation
        sys.exit(1)

    main(start_block, end_block, output_file)
    
