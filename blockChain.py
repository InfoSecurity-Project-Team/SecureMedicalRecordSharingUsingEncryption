import json
import hashlib
import os
from time import time
from typing import List, Dict, Any
from crypto import encrypt_data , decrypt_data

# Path to store the blockchain data
CHAIN_FILE = 'chain.json'

class Block:
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], prev_hash: str):
        """
        Initialize a new block.
        :param index: Position of the block in the chain.
        :param timestamp: Time of block creation.
        :param data: Encrypted medical record data.
        :param prev_hash: Hash of the previous block.
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Assume data is already encrypted
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Generate SHA-256 hash of the block's contents.
        :return: Hash string.
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'prev_hash': self.prev_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert block instance to a dictionary for serialization.
        :return: Dictionary representation of the block.
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'prev_hash': self.prev_hash,
            'hash': self.hash
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """
        Reconstruct a Block instance from a dictionary.
        :param data: Dictionary with block information.
        :return: Block instance.
        """
        block = Block(
            index=data['index'],
            timestamp=data['timestamp'],
            data=data['data'],
            prev_hash=data['prev_hash']
        )
        block.hash = data['hash']  # Use stored hash
        return block


class Blockchain:
    def __init__(self):
        """
        Initialize the blockchain. Load existing chain or create a genesis block.
        """
        self.chain: List[Block] = []
        self.load_chain()

    def create_genesis_block(self):
        """
        Create the first block in the blockchain with default values.
        """
        genesis_data = {"record_id": "0", "note": "Genesis Block"}
        genesis_block = Block(0, time(), genesis_data, "0")
        self.chain.append(genesis_block)
        self.save_chain()

    def add_block(self, record_data: Dict[str, Any]):
        """
        Add a new block with medical record data to the chain.
        Encrypt sensitive fields before saving.
        :param record_data: Dictionary containing plain patient and doctor data.
        """
        # Encrypt 'data' and 'address' fields
        record_data['data'] = encrypt_data(record_data['data']).decode()
        if 'address' in record_data and record_data['address']:
            record_data['address'] = encrypt_data(record_data['address']).decode()

        last_block = self.chain[-1]
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time(),
            data=record_data,
            prev_hash=last_block.hash
        )
        self.chain.append(new_block)
        self.save_chain()

    def get_block(self, index: int) -> Dict[str, Any]:
        """
        Retrieve a specific block by index.
        :param index: Index of the block to retrieve.
        :return: Block data as dictionary or error message.
        """
        if 0 <= index < len(self.chain):
            return self.chain[index].to_dict()
        return {"error": "Block not found."}

    def list_blocks(self) -> List[Dict[str, Any]]:
        """
        Get all blocks in the blockchain with decrypted medical data (except Genesis block).

        :return: List of dictionaries representing the blockchain.
        """
        blocks = []
        for block in self.chain:
            block_dict = block.to_dict()
            data = block_dict.get('data', {})

            # Skip decryption for Genesis block
            if block_dict['index'] == 0:
                blocks.append(block_dict)
                continue

            # Decrypt sensitive fields safely
            if 'data' in data and isinstance(data['data'], str):
                try:
                    decrypted_details = decrypt_data(data['data'])
                    data['data'] = decrypted_details
                except Exception:
                    data['data'] = "[Decryption Failed]"

            if 'address' in data and isinstance(data['address'], str):
                try:
                    decrypted_address = decrypt_data(data['address'])
                    data['address'] = decrypted_address
                except Exception:
                    data['address'] = "[Decryption Failed]"

            blocks.append(block_dict)

        return blocks

    def save_chain(self):
        """
        Save the blockchain to a JSON file.
        """
        with open(CHAIN_FILE, 'w') as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_chain(self):
        """
        Load blockchain from a JSON file, or create a genesis block if file not found.
        """
        if not os.path.exists(CHAIN_FILE):
            self.create_genesis_block()
        else:
            with open(CHAIN_FILE, 'r') as f:
                data = json.load(f)
                self.chain = [Block.from_dict(block) for block in data]


# Example usage
if __name__ == '__main__':
    blockchain = Blockchain()

    # This data should be encrypted in actual implementation
    new_record = {
        "record_id": "001",
        "patient_id": "P123",
        "pname": "John Doe",
        "address": "123 Elm Street",
        "phone": "+123456789",
        "doctor_id": "D456",
        "doctor_name": "Dr. Alice",
        "date": "2025-04-24",
        "data": "gAAAAABkX"  # Mock encrypted data
    }

    # Add a new block with the encrypted data
    blockchain.add_block(new_record)

    # Print all blocks
    for blk in blockchain.list_blocks():
        print(blk)

    # Print a specific block by index
    print(blockchain.get_block(1))
