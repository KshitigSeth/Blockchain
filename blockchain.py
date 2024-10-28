import hashlib
import time

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index                  # Block number in the chain
        self.timestamp = timestamp          # Time when the block was created
        self.transactions = transactions    # Transaction data or other content
        self.previous_hash = previous_hash  # Hash of the previous block
        self.nonce = 0                      # Initial nonce value
        self.hash = self.calculate_hash()   # Current block’s hash, generated on creation

    def calculate_hash(self):
        # Converts block contents into a single unique hash string
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Initializes chain with the first block (genesis block)
        self.difficulty = 2  # Number of leading zeros required for proof of work

    def create_genesis_block(self):
        # Creates the first block with index 0 and arbitrary data
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        # Returns the last block in the chain
        return self.chain[-1]

    def add_block(self, new_block):
        # Adds a new block with reference to the previous block’s hash
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        # Adjust block's nonce to match difficulty
        block.nonce = 0
        while block.calculate_hash()[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
        return block.calculate_hash()

    def is_chain_valid(self):
        # Validates each block and hash continuity
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
