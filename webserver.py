import datetime as date
import json
from urllib.request import urlopen

from flask import Flask, jsonify, request

from main import Block, blockchain

node = Flask(__name__)

# Store transactions until the next block is mined.
this_transactions = []
peer_nodes = []

@node.route('/transactions/new', methods=['POST'])
@node.route('/transcations/new', methods=['POST'])

def new_transaction():
  new_transaction_data = request.get_json()
  if not isinstance(new_transaction_data, dict):
    return jsonify({'message': 'Transaction must be a JSON object'}), 400

  required_fields = {'from', 'to', 'amount'}
  if not required_fields.issubset(new_transaction_data):
    return jsonify({'message': 'Transaction needs from, to, and amount'}), 400

  this_transactions.append(new_transaction_data)
  return jsonify({'message': 'Transaction submitted successfully'}), 201

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

def proof_of_work(last_proof):
    #create a variable that we will use to find the next proof of work
    last_proof = max(last_proof, 1)
    incrementor = last_proof + 1
    #keep incrementing the incrementor until it's equal to a number divisible by 9 and the proof of work of the previous block
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[-1]
    last_proof = last_block.data.get('proof-of-work', 0) if isinstance(last_block.data, dict) else 0
    
    proof = proof_of_work(last_proof)
    
    this_transactions.append(
        
        {
            'from': "network",
            'to': miner_address,
            'amount': 1
        }
    )
    
    #new block creation
    new_block_index = last_block.index + 1
    new_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    
    transactions_for_block = this_transactions.copy()
    new_block_data = {
        'transactions': transactions_for_block,
        'proof-of-work': proof
    }
    
    #create new block and add it to the blockchain
    mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
    blockchain.append(mined_block)
    this_transactions.clear()

    return jsonify({
        "message": "New Block Forged",
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": mined_block.hash
      })

@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = []
  for block in blockchain:
    chain_to_send.append({
      "index": block.index,
      "timestamp": str(block.timestamp),
      "data": block.data,
      "previous_hash": block.previous_hash,
      "hash": block.hash
    })
  return jsonify(chain_to_send)

def find_new_chains():
  # Get the blockchains of every
  # other node
  other_chains = []
  for node_url in peer_nodes:
    # Get their chains using a GET request
    with urlopen(node_url + "/blocks") as response:
      block = response.read()
    # Convert the JSON object to a Python dictionary
    block = json.loads(block)
    # Add it to our list
    other_chains.append(block)
  return other_chains

def consensus():
  global blockchain
  # Get the blocks from other nodes
  other_chains = find_new_chains()
  # If our chain isn't longest,
  # then we store the longest chain
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  # If the longest chain wasn't ours,
  # then we set our chain to the longest
  blockchain = longest_chain


if __name__ == '__main__':
  node.run()