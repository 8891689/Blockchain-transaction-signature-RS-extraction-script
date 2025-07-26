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
*   `requests` library (installable via `pip install requests base58`)
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

# Get Bitcoin R, S, Z values from transaction hash

Getting RSZ values you can recover Bitcoin private key using weak signatures with random vulnerability.
```
https://allprivatekeys.com/get-rsz-signature-from-tx
```
# Or use script extract_rszp.py

View raw transaction data https://btc.exan.tech/tx/b5add54960756c58ebabb332c5ef89098d2c3b8f2107b939ec542178e846108b
```
python3 extract_rszp.py -d b5add54960756c58ebabb332c5ef89098d2c3b8f2107b939ec542178e846108b
Fetching raw transaction for txid: b5add54960756c58ebabb332c5ef89098d2c3b8f2107b939ec542178e846108b...
Successfully fetched raw transaction.

Analyzing Transaction...
======================================================================
[Input Index #: 0]
     R: 83fe1c06236449b69a7bee5be422c067d02c4ce3f4fa3756bd92c632f971de06
     S: 7405249d2aa9184b688f5307006fddc3bd4a7eb89294e3be3438636384d64ce7
     Z: 070239c013e8f40c8c2a0e608ae15a6b1bb4b8fbcab3cff151a6e4e8e05e10b7
PubKey: 04ca5606a1e820e7a2f6bb3ab090e8ade7b04a7e0b5909a68dda2744ae3b8ecbfa280a47639c811134d648e8ee8096c33b41611be509ebca837fbda10baaa1eb15
======================================================================

Analysis complete.

python3 extract_rszp.py -x 01000000013bf51de6fb77fb5aacd88b39d94af438145aa7c2d728979d3ee33651ed09c5fd000000008b48304502210083fe1c06236449b69a7bee5be422c067d02c4ce3f4fa3756bd92c632f971de0602207405249d2aa9184b688f5307006fddc3bd4a7eb89294e3be3438636384d64ce7014104ca5606a1e820e7a2f6bb3ab090e8ade7b04a7e0b5909a68dda2744ae3b8ecbfa280a47639c811134d648e8ee8096c33b41611be509ebca837fbda10baaa1eb15ffffffff01905f010000000000232103bec42e5d718b0e5b3853243c9bcf00dd671a335b0eb99fd8ca32f8d5784a9476ac00000000

Analyzing Transaction...
======================================================================
[Input Index #: 0]
     R: 83fe1c06236449b69a7bee5be422c067d02c4ce3f4fa3756bd92c632f971de06
     S: 7405249d2aa9184b688f5307006fddc3bd4a7eb89294e3be3438636384d64ce7
     Z: 070239c013e8f40c8c2a0e608ae15a6b1bb4b8fbcab3cff151a6e4e8e05e10b7
PubKey: 04ca5606a1e820e7a2f6bb3ab090e8ade7b04a7e0b5909a68dda2744ae3b8ecbfa280a47639c811134d648e8ee8096c33b41611be509ebca837fbda10baaa1eb15
======================================================================

Analysis complete.

```
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

This tool is only used for learning, analysis, vulnerability repair, software testing BUG and other research. Please use it with understanding of the relevant risks. Cracking other people's private keys is unethical and will be subject to legal sanctions. Please abide by local laws and regulations. The developer does not assume any responsibility for economic losses or legal liabilities caused by the use of this tool.

