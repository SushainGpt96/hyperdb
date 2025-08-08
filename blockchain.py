#!/usr/bin/env python3
"""
Minimal Blockchain implementation for HyperDB
"""

import hashlib
import json
import time
from typing import List, Dict, Any


class Block:
    """Represents a block in the blockchain"""
    
    def __init__(self, index: int, transactions: List[Dict], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    """Simple blockchain implementation"""
    
    def __init__(self, difficulty: int = 2):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10
        
        # Create the genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the first block in the chain"""
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, sender: str, recipient: str, amount: float, data: Dict = None) -> int:
        """Add a new transaction to pending transactions"""
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'data': data or {},
            'timestamp': time.time()
        }
        self.pending_transactions.append(transaction)
        return len(self.chain) + 1  # Return the block index where this transaction will be added
    
    def mine_pending_transactions(self, miner_address: str) -> Block:
        """Mine a new block with pending transactions"""
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.get_latest_block().hash
        )
        
        # Mine the block
        block = self.mine_block(block)
        
        # Add the block to the chain
        self.chain.append(block)
        
        # Reset pending transactions and add mining reward
        self.pending_transactions = [
            {
                'sender': "system",
                'recipient': miner_address,
                'amount': self.mining_reward,
                'data': {},
                'timestamp': time.time()
            }
        ]
        
        return block
    
    def mine_block(self, block: Block) -> Block:
        """Mine a block by finding a valid nonce"""
        target = "0" * self.difficulty
        
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
        
        return block
    
    def is_chain_valid(self) -> bool:
        """Check if the blockchain is valid"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """Calculate the balance of an address"""
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction['sender'] == address:
                    balance -= transaction['amount']
                if transaction['recipient'] == address:
                    balance += transaction['amount']
        
        return balance 