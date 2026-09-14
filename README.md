# SnakeCoin Blockchain

A small Python and Flask project for learning the basic ideas behind a blockchain.
It demonstrates blocks, hashes, transactions, proof of work, mining, and a simple
HTTP API.

This is an educational prototype. It is not production cryptocurrency software.

## What It Demonstrates

- A genesis block starts the chain.
- Each block stores an index, timestamp, data, and previous hash.
- SHA-256 creates a hash for each block.
- Transactions wait in memory until a block is mined.
- Mining adds a reward transaction for the miner.
- A simple proof-of-work algorithm searches for a number divisible by 9 and the
	previous proof.
- Chain validation checks block hashes, links, indexes, and proof of work.
- Flask exposes the blockchain through HTTP endpoints.

## Requirements

- Python 3
- Flask
- WSL or another Linux environment is recommended for this project

## Setup in WSL

From the project directory:

```bash
cd /home/ceejay/Blockchain-Python
python3 -m venv venv
source venv/bin/activate
python -m pip install flask
```

If the virtual environment already exists, activate it instead:

```bash
source venv/bin/activate
```

## Start the Server

In the WSL terminal, run:

```bash
python main.py
```

The development server runs at:

```text
http://127.0.0.1:5000
```

Keep this terminal running while sending requests from another terminal.

## API Endpoints

### Check that the server is running

```http
GET /
```

PowerShell:

```powershell
curl.exe http://127.0.0.1:5000/
```

### View the blockchain

```http
GET /blocks
```

```powershell
curl.exe http://127.0.0.1:5000/blocks
```

### Submit a transaction

```http
POST /txion
```

The request body must contain `from`, `to`, and `amount`:

```powershell
Invoke-RestMethod `
	-Uri http://127.0.0.1:5000/txion `
	-Method Post `
	-ContentType "application/json" `
	-Body '{"from":"Alice","to":"Bob","amount":5}'
```

Transactions are stored in memory and are added to the next mined block.

### Mine a block

```http
GET /mine
```

```powershell
curl.exe http://127.0.0.1:5000/mine
```

Mining adds the waiting transactions and a reward transaction to a new block.

### Validate the blockchain

```http
GET /validate
```

```powershell
curl.exe http://127.0.0.1:5000/validate
```

The endpoint returns `{"valid": true}` for an intact chain. It returns a
conflict response if a block has been modified or its link is broken.

## Recommended Test Sequence

Use two terminals. Run the server in WSL, then run these commands from a second
PowerShell terminal:

```powershell
curl.exe http://127.0.0.1:5000/
curl.exe http://127.0.0.1:5000/blocks

Invoke-RestMethod `
	-Uri http://127.0.0.1:5000/txion `
	-Method Post `
	-ContentType "application/json" `
	-Body '{"from":"Alice","to":"Bob","amount":5}'

curl.exe http://127.0.0.1:5000/mine
curl.exe http://127.0.0.1:5000/blocks
curl.exe http://127.0.0.1:5000/validate
```

Stop the server with `Ctrl+C` in the WSL terminal.

## Project Files

```text
main.py       Compatibility entry point used to start the server
app.py        Flask routes and HTTP request handling
blockchain.py Blockchain models, mining, and chain state
README.md     Project documentation
.gitignore    Ignored local, generated, and experimental files
```

## Current Limitations

- The blockchain is stored only in memory and disappears when the server stops.
- There is no wallet, digital signature, or transaction validation.
- There is no database or persistent storage.
- The consensus code is educational and is not exposed as an HTTP route.
- Blocks are not fully validated before being accepted.
- The proof-of-work algorithm is intentionally simple and not secure.
- Flask's development server should not be used for production deployment.

## Learning Roadmap

1. Add a `validate_chain()` function.
2. Store blocks and transactions in a database or JSON file.
3. Add transaction validation and digital signatures.
4. Improve block serialization and chain synchronization.
5. Add tests for hashing, mining, transactions, and validation.
