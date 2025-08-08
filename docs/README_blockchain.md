# Blockchain Implementation (`blockchain.py`)

## Overview

The `blockchain.py` file contains the core blockchain implementation for HyperDB. This module provides a simplified blockchain system that stores database operations as transactions, ensuring data integrity and providing an immutable audit trail.

## Components

### Block Class

```python
class Block:
    def __init__(self, index: int, transactions: List[Dict], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
```

**Purpose**: Represents a single block in the blockchain.

**Properties**:
- `index`: Position of the block in the chain (0 for genesis block)
- `transactions`: List of database operations stored in this block
- `timestamp`: When the block was created
- `previous_hash`: Hash of the previous block (creates the chain)
- `nonce`: Proof-of-work value for mining
- `hash`: Cryptographic hash of the block contents

**Key Methods**:
- `calculate_hash()`: Generates SHA-256 hash of the block data

### Blockchain Class

```python
class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10
```

**Purpose**: Manages the entire blockchain and handles transaction processing.

**Properties**:
- `chain`: List of all blocks in the blockchain
- `difficulty`: Number of leading zeros required in block hash (mining difficulty)
- `pending_transactions`: Transactions waiting to be mined into a block
- `mining_reward`: Reward given to miners (not used in this implementation)

## Key Methods

### 1. Genesis Block Creation

```python
def create_genesis_block(self) -> None:
    """Create the first block in the chain"""
    genesis_block = Block(0, [], time.time(), "0")
    self.chain.append(genesis_block)
```

**Purpose**: Creates the first block in the blockchain.
**Parameters**: None
**Returns**: None
**Description**: Initializes the blockchain with a genesis block containing no transactions and a previous hash of "0".

### 2. Transaction Management

```python
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
    return len(self.chain) + 1
```

**Purpose**: Adds a new transaction to the pending transactions queue.
**Parameters**:
- `sender`: Address of the transaction sender
- `recipient`: Address of the transaction recipient
- `amount`: Transaction amount (not used in database operations)
- `data`: Additional transaction data (database operations)
**Returns**: Block index where the transaction will be added
**Description**: Creates a transaction object with timestamp and adds it to pending transactions.

### 3. Block Mining

```python
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
```

**Purpose**: Creates and mines a new block with all pending transactions.
**Parameters**:
- `miner_address`: Address of the miner (not used in this implementation)
**Returns**: The newly created block
**Description**: 
1. Creates a new block with all pending transactions
2. Mines the block by finding a valid nonce
3. Adds the block to the chain
4. Resets pending transactions
5. Adds mining reward transaction

### 4. Proof-of-Work Mining

```python
def mine_block(self, block: Block) -> Block:
    """Mine a block by finding a valid nonce"""
    target = "0" * self.difficulty
    
    while block.hash[:self.difficulty] != target:
        block.nonce += 1
        block.hash = block.calculate_hash()
    
    return block
```

**Purpose**: Performs proof-of-work mining to find a valid block hash.
**Parameters**:
- `block`: The block to mine
**Returns**: The mined block with valid hash
**Description**: 
1. Creates a target string with required leading zeros
2. Incrementally tries different nonce values
3. Recalculates block hash until it matches the target
4. Returns the block with valid hash

### 5. Chain Validation

```python
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
```

**Purpose**: Validates the integrity of the entire blockchain.
**Parameters**: None
**Returns**: True if chain is valid, False otherwise
**Description**:
1. Iterates through all blocks (except genesis)
2. Verifies each block's hash is correct
3. Verifies each block points to the correct previous block
4. Returns True only if all checks pass

### 6. Balance Calculation

```python
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
```

**Purpose**: Calculates the balance of a specific address.
**Parameters**:
- `address`: The address to calculate balance for
**Returns**: Current balance of the address
**Description**: 
1. Iterates through all blocks and transactions
2. Subtracts amounts sent from the address
3. Adds amounts received by the address
4. Returns the final balance

## Usage in HyperDB

### Integration with Database

The blockchain is integrated into the database system through the `HyperledgerIntegratedDB` class:

```python
# Initialize blockchain with database
self.blockchain = Blockchain(difficulty=blockchain_difficulty)

# Add database operations as transactions
def _add_to_blockchain(self, transaction_type: str, data: Dict[str, Any]) -> str:
    transaction_id = str(uuid.uuid4())
    transaction = {
        'id': transaction_id,
        'type': transaction_type,
        'data': data,
        'timestamp': time.time(),
        'sender': 'system',
        'recipient': 'system',
        'amount': 0.0
    }
    
    # Add to blockchain pending transactions
    self.blockchain.add_transaction(
        sender='system',
        recipient='system',
        amount=0.0,
        data=transaction
    )
    
    return transaction_id
```

### Transaction Types

The blockchain stores three types of database operations:

1. **`model_creation`**: When a new data model/schema is created
2. **`data_creation`**: When new data is added to a model
3. **`data_update`**: When existing data is updated

### Block Mining Process

```python
def mine_block(self) -> Optional[Dict[str, Any]]:
    """Mine a new block with pending transactions"""
    if not self.blockchain.pending_transactions:
        print("No pending transactions to mine")
        return None
    
    # Mine the block
    block = self.blockchain.mine_pending_transactions("system")
    
    # Save block to database
    cursor = self.connection.cursor()
    cursor.execute('''
        INSERT INTO blockchain_blocks (block_index, hash, previous_hash, timestamp, nonce, transactions_data)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        block.index,
        block.hash,
        block.previous_hash,
        block.timestamp,
        block.nonce,
        json.dumps(block.transactions)
    ))
    
    # Update transaction block indices
    for transaction in block.transactions:
        if transaction.get('id'):
            cursor.execute('''
                UPDATE blockchain_transactions 
                SET block_index = ?
                WHERE id = ?
            ''', (block.index, transaction['id']))
    
    self.connection.commit()
    return {
        'index': block.index,
        'hash': block.hash,
        'timestamp': block.timestamp,
        'transaction_count': len(block.transactions)
    }
```

## Security Features

### 1. Cryptographic Hashing
- Uses SHA-256 for block hashing
- Ensures data integrity
- Prevents tampering with block contents

### 2. Chain Linking
- Each block contains the hash of the previous block
- Creates an immutable chain
- Any modification breaks the chain

### 3. Proof-of-Work
- Requires computational work to mine blocks
- Prevents spam and ensures block creation is intentional
- Configurable difficulty level

### 4. Transaction Validation
- All transactions are timestamped
- Transaction data is immutable once mined
- Complete audit trail of all operations

## Configuration

### Difficulty Setting

The mining difficulty can be configured when creating the blockchain:

```python
# Easy mining (faster, less secure)
blockchain = Blockchain(difficulty=1)

# Standard mining (balanced)
blockchain = Blockchain(difficulty=2)

# Hard mining (slower, more secure)
blockchain = Blockchain(difficulty=4)
```

### Mining Reward

The mining reward can be adjusted:

```python
blockchain.mining_reward = 20  # Increase reward
```

## Performance Considerations

### Mining Speed
- Higher difficulty = slower mining
- More transactions = longer mining time
- Consider batch size for optimal performance

### Memory Usage
- All blocks are stored in memory
- Large chains may require optimization
- Consider pruning old blocks for long-running systems

### Storage
- Block data is stored in SQLite database
- Transaction data is duplicated in blockchain
- Consider compression for large datasets

## Error Handling

The blockchain implementation includes error handling for:

1. **Invalid Block Creation**: Ensures blocks have required fields
2. **Hash Calculation**: Handles hash generation errors
3. **Chain Validation**: Detects corrupted chains
4. **Transaction Processing**: Validates transaction format

## Testing

The blockchain can be tested independently:

```python
# Create blockchain
blockchain = Blockchain(difficulty=2)

# Add transactions
blockchain.add_transaction("alice", "bob", 10.0, {"type": "test"})
blockchain.add_transaction("bob", "charlie", 5.0, {"type": "test"})

# Mine block
block = blockchain.mine_pending_transactions("miner")

# Validate chain
is_valid = blockchain.is_chain_valid()
print(f"Chain valid: {is_valid}")

# Check balances
alice_balance = blockchain.get_balance("alice")
bob_balance = blockchain.get_balance("bob")
print(f"Alice: {alice_balance}, Bob: {bob_balance}")
```

## Future Enhancements

### Potential Improvements

1. **Consensus Mechanisms**: Add support for multiple nodes
2. **Smart Contracts**: Implement programmable transactions
3. **Privacy Features**: Add transaction privacy options
4. **Performance Optimization**: Implement faster mining algorithms
5. **Storage Optimization**: Add block pruning and compression

### Scalability Considerations

1. **Block Size**: Limit transactions per block
2. **Mining Frequency**: Adjust mining intervals
3. **Memory Management**: Implement block caching
4. **Database Optimization**: Index blockchain tables

This blockchain implementation provides a solid foundation for the HyperDB system, ensuring data integrity and providing a complete audit trail of all database operations. 