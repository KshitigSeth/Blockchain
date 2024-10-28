import hashlib  # For generating hashes for blocks
import time     # For timestamps

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index                # Block number in the chain
        self.timestamp = timestamp        # Time when the block was created
        self.data = data                  # Transaction data or other content
        self.previous_hash = previous_hash  # Hash of the previous block
        self.hash = self.calculate_hash() # Current block’s hash, generated on creation

    def calculate_hash(self):
        # Converts block contents into a single unique hash string
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Initializes chain with the first block (genesis block)

    def create_genesis_block(self):
        # Creates the first block with index 0 and arbitrary data
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        # Returns the last block in the chain
        return self.chain[-1]

    def add_block(self, new_block):
        # Adds a new block with reference to the previous block’s hash
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)