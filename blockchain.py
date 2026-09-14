import datetime as date
import hashlib as hasher
import json
from urllib.request import urlopen


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        block_contents = (
            str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
        )
        return hasher.sha256(block_contents.encode()).hexdigest()


def create_genesis_block():
    return Block(
        0,
        date.datetime.now(),
        {"proof-of-work": 9, "transactions": None},
        "0",
    )


miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
blockchain = [create_genesis_block()]
this_nodes_transactions = []
peer_nodes = []


def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor


def mine_block():
    last_block = blockchain[-1]
    last_proof = last_block.data["proof-of-work"]
    proof = proof_of_work(last_proof)

    this_nodes_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions),
    }
    this_nodes_transactions.clear()

    mined_block = Block(
        last_block.index + 1,
        date.datetime.now(),
        new_block_data,
        last_block.hash,
    )
    blockchain.append(mined_block)
    return mined_block


def block_to_dict(block):
    return {
        "index": block.index,
        "timestamp": str(block.timestamp),
        "data": block.data,
        "previous_hash": block.previous_hash,
        "hash": block.hash,
    }


def get_chain():
    return [block_to_dict(block) for block in blockchain]


def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        with urlopen(node_url + "/blocks") as response:
            other_chains.append(json.loads(response.read()))
    return other_chains


def consensus():
    global blockchain
    longest_chain = blockchain
    for chain in find_new_chains():
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain
    return blockchain
