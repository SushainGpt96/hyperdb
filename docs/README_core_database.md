# Core Database System (`src/core/hyperledger_integrated_db.py`)

## Overview

The `hyperledger_integrated_db.py` file contains the main database system that integrates SQLite with blockchain storage. This is the core component of HyperDB that provides dynamic schema creation, data validation, and automatic blockchain integration.

## Key Components

### DataField Class
```python
@dataclass
class DataField:
    name: str
    type: str  # 'text', 'integer', 'real', 'boolean', 'datetime', 'json'
    required: bool = True
    default: Any = None
    description: str = ""
```

**Purpose**: Represents a single field in a data model/schema.

**Supported Types**:
- `text`: String data
- `integer`: Whole numbers
- `real`: Decimal numbers
- `boolean`: True/False values
- `datetime`: Timestamp data
- `json`: Complex data structures

### DataModel Class
```python
@dataclass
class DataModel:
    name: str
    fields: List[DataField]
    description: str = ""
    created_at: float = None
    version: str = "1.0"
```

**Purpose**: Represents a complete data model/schema with multiple fields.

### HyperledgerIntegratedDB Class

The main database class that provides all core functionality:

**Key Methods**:

1. **Schema Management:**
   ```python
   def create_data_model(self, name: str, fields: List[Dict], description: str = "") -> bool
   def get_data_models(self) -> List[Dict[str, Any]]
   ```

2. **Data Operations:**
   ```python
   def add_data(self, model_name: str, data: Dict[str, Any]) -> Optional[str]
   def update_data(self, record_id: str, data: Dict[str, Any]) -> bool
   def get_data(self, record_id: str) -> Optional[Dict[str, Any]]
   def get_all_data(self, model_name: str = None) -> List[Dict[str, Any]]
   ```

3. **Search and Query:**
   ```python
   def search_data(self, model_name: str = None, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]
   ```

4. **Blockchain Operations:**
   ```python
   def mine_block(self) -> Optional[Dict[str, Any]]
   def get_blockchain_info(self) -> Dict[str, Any]
   ```

5. **Data Export:**
   ```python
   def export_data(self, filepath: str) -> bool
   ```

## Database Schema

The system creates 4 main tables:

1. **`data_models`** - Stores schema definitions
2. **`data_records`** - Stores actual data records
3. **`blockchain_transactions`** - Stores all blockchain transactions
4. **`blockchain_blocks`** - Stores mined blockchain blocks

## Usage Examples

### Creating a Data Model
```python
from src.core.hyperledger_integrated_db import HyperledgerIntegratedDB

db = HyperledgerIntegratedDB("my_database.db")

# Create a user model
fields = [
    {'name': 'username', 'type': 'text', 'required': True},
    {'name': 'email', 'type': 'text', 'required': True},
    {'name': 'age', 'type': 'integer', 'required': False},
    {'name': 'is_active', 'type': 'boolean', 'required': True, 'default': True}
]

db.create_data_model("User", fields, "User account information")
db.mine_block()
```

### Adding Data
```python
# Add user data
user_data = {
    'username': 'john_doe',
    'email': 'john@example.com',
    'age': 30,
    'is_active': True
}

record_id = db.add_data("User", user_data)
db.mine_block()
```

### Searching Data
```python
# Search active users
active_users = db.search_data("User", {'is_active': True})
print(f"Active users: {len(active_users)}")

# Search by age
young_users = db.search_data("User", {'age': 30})
print(f"Users aged 30: {len(young_users)}")
```

### Updating Data
```python
# Update user data
updated_data = {
    'username': 'john_doe_updated',
    'email': 'john.updated@example.com',
    'age': 31,
    'is_active': True
}

db.update_data(record_id, updated_data)
db.mine_block()
```

### Getting Blockchain Information
```python
# Get blockchain status
info = db.get_blockchain_info()
print(f"Chain length: {info['chain_length']}")
print(f"Pending transactions: {info['pending_transactions']}")
print(f"Chain valid: {info['is_valid']}")
```

### Exporting Data
```python
# Export all data
db.export_data("database_export.json")
```

## Data Validation

The system automatically validates data against schemas:

### Type Validation
- Ensures data types match field definitions
- Validates required fields are present
- Checks JSON field format

### Error Handling
- Clear error messages for validation failures
- Graceful handling of invalid data
- Transaction rollback on errors

## Blockchain Integration

Every database operation creates a blockchain transaction:

### Transaction Types
1. **`model_creation`**: When a new data model is created
2. **`data_creation`**: When new data is added
3. **`data_update`**: When existing data is updated

### Block Mining
- Manual control over when transactions are committed
- Configurable mining difficulty
- Complete audit trail of all operations

## Security Features

### Data Integrity
- Automatic validation against schemas
- Immutable transaction history
- Cryptographic hashing of blocks

### Audit Trail
- Complete history of all operations
- Timestamped transactions
- Blockchain verification

This core database system provides a robust foundation for the HyperDB platform, combining traditional database functionality with blockchain security and immutability.