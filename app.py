from flask import Flask, jsonify, request

import blockchain


node = Flask(__name__)


@node.route("/", methods=["GET"])
def home():
    return "SnakeCoin blockchain is running"


@node.route("/txion", methods=["POST"])
@node.route("/transactions/new", methods=["POST"])
def transaction():
    new_transaction = request.get_json()
    if not isinstance(new_transaction, dict):
        return jsonify({"message": "Transaction must be a JSON object"}), 400

    required_fields = {"from", "to", "amount"}
    if not required_fields.issubset(new_transaction):
        return jsonify({"message": "Transaction needs from, to, and amount"}), 400

    blockchain.this_nodes_transactions.append(new_transaction)
    return jsonify({"message": "Transaction submission successful"}), 201


@node.route("/blocks", methods=["GET"])
def get_blocks():
    return jsonify(blockchain.get_chain())


@node.route("/validate", methods=["GET"])
def validate():
    valid = blockchain.validate_chain()
    return jsonify({"valid": valid}), 200 if valid else 409


@node.route("/mine", methods=["GET"])
def mine():
    mined_block = blockchain.mine_block()
    return jsonify(
        {
            "index": mined_block.index,
            "timestamp": str(mined_block.timestamp),
            "data": mined_block.data,
            "hash": mined_block.hash,
        }
    )


@node.route("/consensus", methods=["GET"])
def run_consensus():
    chain = blockchain.consensus()
    return jsonify({"message": "Consensus completed", "blocks": len(chain)})


if __name__ == "__main__":
    node.run()
