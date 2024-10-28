from flask import Flask, jsonify, request
from blockchain import Block, Blockchain
import time

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
        })
    return jsonify({'chain': chain_data, 'length': len(chain_data)}), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["sender", "recipient", "amount"]

    if not all(field in tx_data for field in required_fields):
        return "Invalid transaction data", 400

    blockchain.pending_transactions.append(tx_data)
    return jsonify({"message": "Transaction added successfully"}), 201

@app.route('/mine', methods=['POST'])
def mine_block():
    if not blockchain.pending_transactions:
        return jsonify({'message': 'No transactions to mine'}), 400

    last_block = blockchain.get_latest_block()
    new_block = Block(last_block.index + 1, time.time(), blockchain.pending_transactions, last_block.hash)
    blockchain.add_block(new_block)
    blockchain.pending_transactions = []
    
    return jsonify({
        'message': 'Block mined successfully!',
        'index': new_block.index,
        'timestamp': new_block.timestamp,
        'transactions': new_block.transactions,
        'previous_hash': new_block.previous_hash,
        'hash': new_block.hash,
        'nonce': new_block.nonce
    }), 201

@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({'is_valid': is_valid}), 200

@app.route('/transactions/pending', methods=['GET'])
def get_pending_transactions():
    return jsonify({'pending_transactions': blockchain.pending_transactions}), 200

if __name__ == '__main__':
    app.run(debug=True)