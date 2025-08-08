# Hyperledger Integrated Database System

A Python-based database system that integrates blockchain storage with traditional database operations, inspired by Hyperledger Fabric's approach. This system allows you to create dynamic data models at runtime and automatically stores all database operations on a blockchain with timestamps.

## Features

- **Dynamic Schema Creation**: Create data models/schemas at runtime with custom fields
- **Automatic Blockchain Storage**: Every database operation is automatically stored on the blockchain
- **Single Node Architecture**: Simplified blockchain implementation (no distributed consensus)
- **Data Validation**: Automatic validation against defined schemas
- **Search and Query**: Powerful search capabilities across all data
- **Export/Import**: Full data export and import functionality
- **Transaction History**: Complete audit trail of all data changes
- **Type Safety**: Support for various data types (text, integer, real, boolean, datetime, json)

## Key Components

### 1. HyperledgerIntegratedDB
The main database class that handles:
- Dynamic schema creation
- Data storage and retrieval
- Automatic blockchain integration
- Data validation
- Search functionality

### 2. HyperledgerAPI
A simplified API wrapper that provides:
- Easy-to-use interface
- Pre-built models for common use cases
- Context manager for automatic resource management
- Convenience methods for common operations

### 3. Data Models
Support for various data types:
- `text`: String values
- `integer`: Whole numbers
- `real`: Decimal numbers
- `boolean`: True/false values
- `datetime`: Timestamp values
- `json`: Complex data structures

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from hyperledger_integrated_db import HyperledgerIntegratedDB

# Initialize the database
db = HyperledgerIntegratedDB("my_database.db")

# Create a data model
user_fields = [
    {'name': 'username', 'type': 'text', 'required': True},
    {'name': 'email', 'type': 'text', 'required': True},
    {'name': 'age', 'type': 'integer', 'required': False},
    {'name': 'is_active', 'type': 'boolean', 'required': True, 'default': True}
]

db.create_data_model("User", user_fields, "User account information")

# Add data
user_data = {
    'username': 'john_doe',
    'email': 'john@example.com',
    'age': 30,
    'is_active': True
}

record_id = db.add_data("User", user_data)

# Mine a block to commit transactions
db.mine_block()

# Search data
active_users = db.search_data("User", {'is_active': True})
print(f"Found {len(active_users)} active users")

# Close the database
db.disconnect()
```

### Using the API Wrapper

```python
from hyperledger_api import HyperledgerAPI

# Initialize the API
api = HyperledgerAPI("api_database.db")

# Create standard models
api.create_user_model()
api.create_product_model()

# Mine block to commit models
api.mine_block()

# Add data
user_id = api.add_user("alice", "alice@example.com", "hashed_password")
product_id = api.add_product("Laptop", 999.99, "Electronics", "High-performance laptop")

# Mine block to commit data
api.mine_block()

# Search data
users = api.get_users(active_only=True)
products = api.get_products(in_stock_only=True)

# Close the API
api.close()
```

### Using Context Manager

```python
from hyperledger_api import HyperledgerContext

with HyperledgerContext("context_database.db") as api:
    # Create models
    api.create_user_model()
    api.create_product_model()
    
    # Mine block
    api.mine_block()
    
    # Add data
    api.add_user("bob", "bob@example.com", "password_hash")
    api.add_product("Phone", 599.99, "Electronics")
    
    # Mine block
    api.mine_block()
    
    # Get blockchain info
    info = api.get_blockchain_info()
    print(f"Blockchain blocks: {info['chain_length']}")
```

## Advanced Usage

### Creating Custom Data Models

```python
# Define custom fields
custom_fields = [
    {
        'name': 'title',
        'type': 'text',
        'required': True,
        'description': 'Document title'
    },
    {
        'name': 'content',
        'type': 'text',
        'required': True,
        'description': 'Document content'
    },
    {
        'name': 'tags',
        'type': 'json',
        'required': False,
        'description': 'Document tags'
    },
    {
        'name': 'created_at',
        'type': 'datetime',
        'required': True,
        'description': 'Creation timestamp'
    }
]

# Create the model
db.create_data_model("Document", custom_fields, "Document storage model")
```

### Data Validation

The system automatically validates data against the defined schema:

```python
# This will raise a ValueError if validation fails
try:
    invalid_data = {
        'username': 'john',  # Missing required email field
        'age': 'not_a_number'  # Wrong type for age
    }
    db.add_data("User", invalid_data)
except ValueError as e:
    print(f"Validation error: {e}")
```

### Searching Data

```python
# Search by exact match
users = db.search_data("User", {'username': 'john_doe'})

# Search by boolean field
active_users = db.search_data("User", {'is_active': True})

# Search by numeric field
young_users = db.search_data("User", {'age': 25})

# Search across all models
all_records = db.search_data(criteria={'some_field': 'some_value'})
```

### Updating Data

```python
# Get existing record
record = db.get_data(record_id)

# Update the data
updated_data = record['data'].copy()
updated_data['email'] = 'new_email@example.com'
updated_data['age'] = 31

# Save the update
db.update_data(record_id, updated_data)
```

### Blockchain Information

```python
# Get blockchain status
info = db.get_blockchain_info()
print(f"Chain length: {info['chain_length']}")
print(f"Pending transactions: {info['pending_transactions']}")
print(f"Chain valid: {info['is_valid']}")
print(f"Latest block: {info['latest_block']}")
```

### Exporting Data

```python
# Export all data to JSON
db.export_data("export.json")

# The export includes:
# - All data models
# - All data records
# - Blockchain information
# - Blockchain blocks
```

## E-commerce Example

Here's a complete e-commerce example:

```python
from hyperledger_api import HyperledgerContext

with HyperledgerContext("ecommerce.db") as api:
    # Create models
    api.create_user_model()
    api.create_product_model()
    api.create_order_model()
    
    # Mine block for models
    api.mine_block()
    
    # Add users
    user1_id = api.add_user("alice", "alice@example.com", "hash1")
    user2_id = api.add_user("bob", "bob@example.com", "hash2")
    
    # Add products
    laptop_id = api.add_product("Laptop", 999.99, "Electronics")
    shoes_id = api.add_product("Running Shoes", 89.99, "Sports")
    
    # Mine block for users and products
    api.mine_block()
    
    # Add orders
    order1_items = [{"product_id": laptop_id, "quantity": 1, "price": 999.99}]
    api.add_order(user1_id, order1_items, 999.99)
    
    order2_items = [{"product_id": shoes_id, "quantity": 2, "price": 89.99}]
    api.add_order(user2_id, order2_items, 179.98)
    
    # Mine block for orders
    api.mine_block()
    
    # Query data
    users = api.get_users()
    products = api.get_products()
    orders = api.get_orders()
    
    print(f"Users: {len(users)}")
    print(f"Products: {len(products)}")
    print(f"Orders: {len(orders)}")
    
    # Search examples
    tech_products = api.search_records("Product", {"category": "Electronics"})
    pending_orders = api.search_records("Order", {"status": "pending"})
    
    print(f"Tech products: {len(tech_products)}")
    print(f"Pending orders: {len(pending_orders)}")
```

## Database Schema

The system creates the following tables:

### data_models
- `name`: Model name (primary key)
- `schema_data`: JSON schema definition
- `created_at`: Creation timestamp
- `version`: Schema version

### data_records
- `id`: Record ID (primary key)
- `model_name`: Associated model name
- `data`: JSON data
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `blockchain_transaction_id`: Associated blockchain transaction
- `blockchain_block_index`: Associated blockchain block

### blockchain_transactions
- `id`: Transaction ID (primary key)
- `transaction_type`: Type of transaction
- `data_id`: Associated data record ID
- `model_name`: Associated model name
- `transaction_data`: Full transaction data
- `timestamp`: Transaction timestamp
- `block_index`: Associated blockchain block

### blockchain_blocks
- `block_index`: Block index (primary key)
- `hash`: Block hash
- `previous_hash`: Previous block hash
- `timestamp`: Block timestamp
- `nonce`: Mining nonce
- `transactions_data`: Block transactions
- `created_at`: Block creation timestamp

## Blockchain Features

### Single Node Architecture
- Simplified blockchain implementation
- No distributed consensus required
- Perfect for single-organization use cases
- Fast transaction processing

### Transaction Types
- `model_creation`: When a new data model is created
- `data_creation`: When new data is added
- `data_update`: When existing data is updated

### Mining
- Manual block mining (no automatic mining)
- Configurable difficulty level
- Transaction batching for efficiency

### Audit Trail
- Complete history of all data changes
- Timestamped transactions
- Immutable blockchain records
- Full data lineage tracking

## Best Practices

1. **Mine Blocks Regularly**: Mine blocks after adding significant amounts of data to ensure transactions are committed.

2. **Validate Data**: Always validate data before adding it to ensure schema compliance.

3. **Use Meaningful Field Names**: Choose descriptive field names for better data organization.

4. **Handle Errors**: Always handle potential validation errors when adding or updating data.

5. **Export Regularly**: Export your data regularly for backup purposes.

6. **Monitor Blockchain**: Keep track of blockchain information to ensure system health.

## Limitations

1. **Single Node**: This is not a distributed blockchain - it's designed for single-organization use.
2. **No Smart Contracts**: Unlike Hyperledger Fabric, this system doesn't support smart contracts.
3. **Manual Mining**: Blocks must be mined manually - no automatic mining.
4. **SQLite Only**: Currently only supports SQLite database backend.

## Future Enhancements

- Support for other database backends (PostgreSQL, MongoDB)
- Distributed consensus mechanisms
- Smart contract support
- Automatic block mining
- Web interface
- REST API
- GraphQL support
- Advanced querying capabilities

## Troubleshooting

### Common Issues

1. **Validation Errors**: Ensure all required fields are provided and data types match the schema.

2. **Database Locked**: Close the database connection properly using `disconnect()` or the context manager.

3. **Blockchain Invalid**: Check if the blockchain is valid using `get_blockchain_info()`.

4. **Missing Models**: Ensure data models are created before adding data to them.

### Debug Information

```python
# Get detailed blockchain information
info = db.get_blockchain_info()
print(f"Chain valid: {info['is_valid']}")
print(f"Chain length: {info['chain_length']}")
print(f"Pending transactions: {info['pending_transactions']}")

# Get all data models
models = db.get_data_models()
for model in models:
    print(f"Model: {model['name']}")
    print(f"Fields: {len(model['fields'])}")

# Get all records
records = db.get_all_data()
print(f"Total records: {len(records)}")
```

## License

This project is open source and available under the MIT License. 