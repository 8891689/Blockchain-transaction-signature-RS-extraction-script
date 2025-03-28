# Blockchain transaction signature RS extraction script

This script connects via RPC to a Bitcoin or compatible blockchain node, scans blocks within a specified range, and extracts the ECDSA signature R and S values from transaction input scripts (`scriptSig`). The extracted information is then saved to a specified output file.

## Features

*   Connects to a blockchain node via JSON-RPC.
*   Fetches block data for a specified block height range.
*   Iterates through each transaction in a block (skipping Coinbase transactions).
*   Parses and extracts ECDSA signature R and S values from the `scriptSig` of transaction inputs (`vin`).
*   Writes the transaction ID containing signatures, along with the corresponding R and S values, to the specified output file.
*   Includes an RPC connection retry mechanism and a prompt for manual reconnection ('P' key).
*   Displays a progress bar during processing.

## Requirements

*   Python 3
*   `requests` library (installable via `pip install requests`)
*   A running Bitcoin Core or compatible node with RPC service enabled.

## Setup

Before running the script, you **must** modify the following RPC connection settings at the beginning of the script to match your node's configuration:

```python
# RPC Connection Settings
RPC_USER = 'Your_RPC_Username'
RPC_PASSWORD = 'Your_RPC_Password'
RPC_PORT = 'Your_RPC_Port' # Default is usually 8332 (mainnet) or 18332 (testnet)
RPC_URL = f'http://127.0.0.1:{RPC_PORT}' # Modify the IP address if the node is not on localhost
```
# Usage

Run the script from the command line, providing three required arguments: start block height, end block height, and the output filename.
```
python3 extract_data.py <start_block> <end_block> <output_file>
```



Parameters:

<start_block>: The block height to start scanning from (integer).

<end_block>: The block height to end scanning at (integer, inclusive).

<output_file>: The path and name of the file to save the extracted results.

# Example:
```
python3 extract_data.py 700000 700010 signatures_output.txt
```


This command will scan blocks from 700000 to 700010 (inclusive) and save the extracted transaction IDs and signature R/S values to the signatures_output.txt file.

# Output Format

The output file will contain content in the following format:
```
Transaction ID: <Transaction Hash>
  Signature - R: <Signature R value (hex)>, S: <Signature S value (hex)>
Transaction ID: <Another Transaction Hash>
  Signature - R: <Signature R value (hex)>, S: <Signature S value (hex)>
  Signature - R: <Another Signature R value from the same transaction (hex)>, S: <Another Signature S value from the same transaction (hex)>
```


# Notes

The script assumes the RPC node is running at http://127.0.0.1. If your node is on a different host or uses a different protocol (e.g., HTTPS), be sure to modify the RPC_URL.

The signature extraction method relies on regular expression matching and basic parsing of the scriptSig.asm format. It might not cover all complex or non-standard script types.

If the RPC connection fails, the script will attempt to reconnect several times. If failures persist, it will prompt the user to press 'P' to manually trigger a reconnection attempt.


# Sponsorship
If this project was helpful to you, please buy me a coffee. Your support is greatly appreciated. Thank you!
```
BTC: bc1qt3nh2e6gjsfkfacnkglt5uqghzvlrr6jahyj2k
ETH: 0xD6503e5994bF46052338a9286Bc43bC1c3811Fa1
DOGE: DTszb9cPALbG9ESNJMFJt4ECqWGRCgucky
TRX: TAHUmjyzg7B3Nndv264zWYUhQ9HUmX4Xu4
```

# 📜 Disclaimer
Reminder: Do not enter the real private key on the connected device!

This tool is only for learning, analyzing, testing and vulnerability research. Please use it with understanding of the relevant risks. Cracking other people's private keys is unethical and will be punished by law. Please abide by local laws and regulations. The developer is not responsible for economic losses or legal liabilities caused by the use of this tool.

