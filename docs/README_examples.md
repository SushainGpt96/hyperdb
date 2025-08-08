# Examples (`src/examples/example_hyperledger_usage.py`)

## Overview

The `example_hyperledger_usage.py` file contains comprehensive examples demonstrating how to use the HyperDB system. This file showcases all major features including dynamic schema creation, data operations, blockchain integration, and search functionality.

## Main Example Function

### Complete System Demonstration

```python
def main():
    """Main example function"""
    print("=== Hyperledger Integrated Database System Example ===\n")
    
    # Initialize the integrated database system
    db = HyperledgerIntegratedDB(db_path="example_hyperledger.db")
```

**Purpose**: Demonstrates the complete HyperDB system functionality.

**Features Demonstrated**:
- Dynamic schema creation
- Data addition and validation
- Blockchain integration
- Search and query operations
- Data export functionality

## Example 1: User Data Model Creation

```python
# Example 1: Create a User data model
print("1. Creating User data model...")
user_fields = [
    {
        'name': 'username',
        'type': 'text',
        'required': True,
        'description': 'Unique username for the user'
    },
    {
        'name': 'email',
        'type': 'text',
        'required': True,
        'description': 'User email address'
    },
    {
        'name': 'age',
        'type': 'integer',
        'required': False,
        'description': 'User age'
    },
    {
        'name': 'is_active',
        'type': 'boolean',
        'required': True,
        'default': True,
        'description': 'Whether the user account is active'
    },
    {
        'name': 'metadata',
        'type': 'json',
        'required': False,
        'description': 'Additional user metadata'
    }
]

db.create_data_model(
    name="User",
    fields=user_fields,
    description="User account information"
)
```

**Demonstrates**:
- Dynamic field definition
- Multiple data types (text, integer, boolean, json)
- Required vs optional fields
- Default values
- Field descriptions

## Example 2: Product Data Model Creation

```python
# Example 2: Create a Product data model
print("\n2. Creating Product data model...")
product_fields = [
    {
        'name': 'name',
        'type': 'text',
        'required': True,
        'description': 'Product name'
    },
    {
        'name': 'price',
        'type': 'real',
        'required': True,
        'description': 'Product price'
    },
    {
        'name': 'category',
        'type': 'text',
        'required': True,
        'description': 'Product category'
    },
    {
        'name': 'in_stock',
        'type': 'boolean',
        'required': True,
        'default': True,
        'description': 'Whether product is in stock'
    },
    {
        'name': 'created_at',
        'type': 'datetime',
        'required': True,
        'description': 'Product creation timestamp'
    }
]

db.create_data_model(
    name="Product",
    fields=product_fields,
    description="Product catalog information"
)
```

**Demonstrates**:
- Real number fields for prices
- Boolean fields for stock status
- Datetime fields for timestamps
- Category-based organization

## Example 3: Block Mining for Model Creation

```python
# Mine the first block to commit the model creation transactions
print("\n3. Mining first block to commit model creation...")
block_info = db.mine_block()
if block_info:
    print(f"Block {block_info['index']} mined with {block_info['transaction_count']} transactions")
```

**Demonstrates**:
- Manual block mining
- Transaction commitment
- Blockchain integration
- Block information retrieval

## Example 4: Adding User Data

```python
# Example 3: Add user data
print("\n4. Adding user data...")
users = [
    {
        'username': 'john_doe',
        'email': 'john@example.com',
        'age': 30,
        'is_active': True,
        'metadata': {'preferences': ['tech', 'sports'], 'last_login': '2024-01-15'}
    },
    {
        'username': 'jane_smith',
        'email': 'jane@example.com',
        'age': 25,
        'is_active': True,
        'metadata': {'preferences': ['art', 'music']}
    },
    {
        'username': 'bob_wilson',
        'email': 'bob@example.com',
        'is_active': False,
        'metadata': {'notes': 'Inactive account'}
    }
]

user_ids = []
for user_data in users:
    user_id = db.add_data("User", user_data)
    if user_id:
        user_ids.append(user_id)
        print(f"Added user: {user_data['username']} (ID: {user_id})")
```

**Demonstrates**:
- Adding multiple records
- JSON metadata fields
- Optional field handling
- Record ID generation
- Error handling

## Example 5: Adding Product Data

```python
# Example 4: Add product data
print("\n5. Adding product data...")
products = [
    {
        'name': 'Laptop',
        'price': 999.99,
        'category': 'Electronics',
        'in_stock': True,
        'created_at': time.time()
    },
    {
        'name': 'Coffee Mug',
        'price': 12.50,
        'category': 'Kitchen',
        'in_stock': True,
        'created_at': time.time()
    },
    {
        'name': 'Running Shoes',
        'price': 89.99,
        'category': 'Sports',
        'in_stock': False,
        'created_at': time.time()
    }
]

product_ids = []
for product_data in products:
    product_id = db.add_data("Product", product_data)
    if product_id:
        product_ids.append(product_id)
        print(f"Added product: {product_data['name']} (ID: {product_id})")
```

**Demonstrates**:
- Real number handling
- Boolean field usage
- Timestamp creation
- Category organization

## Example 6: Block Mining for Data Creation

```python
# Mine another block to commit the data creation transactions
print("\n6. Mining second block to commit data creation...")
block_info = db.mine_block()
if block_info:
    print(f"Block {block_info['index']} mined with {block_info['transaction_count']} transactions")
```

**Demonstrates**:
- Batch transaction processing
- Multiple operations per block
- Transaction counting

## Example 7: Updating Data

```python
# Example 5: Update some data
print("\n7. Updating user data...")
if user_ids:
    # Update the first user
    updated_user_data = {
        'username': 'john_doe_updated',
        'email': 'john.updated@example.com',
        'age': 31,
        'is_active': True,
        'metadata': {'preferences': ['tech', 'sports', 'cooking'], 'last_login': '2024-01-20'}
    }
    
    if db.update_data(user_ids[0], updated_user_data):
        print(f"Updated user: {updated_user_data['username']}")
```

**Demonstrates**:
- Data modification
- Field updates
- JSON field modification
- Update validation

## Example 8: Search Functionality

```python
# Example 6: Search data
print("\n8. Searching for data...")

# Search for active users
active_users = db.search_data("User", {'is_active': True})
print(f"Found {len(active_users)} active users:")
for user in active_users:
    print(f"  - {user['data']['username']} ({user['data']['email']})")

# Search for products in stock
in_stock_products = db.search_data("Product", {'in_stock': True})
print(f"\nFound {len(in_stock_products)} products in stock:")
for product in in_stock_products:
    print(f"  - {product['data']['name']} (${product['data']['price']})")

# Search for electronics
electronics = db.search_data("Product", {'category': 'Electronics'})
print(f"\nFound {len(electronics)} electronics products:")
for product in electronics:
    print(f"  - {product['data']['name']} (${product['data']['price']})")
```

**Demonstrates**:
- Boolean field searching
- Exact match searching
- Multiple search criteria
- Result iteration
- Data formatting

## Example 9: Retrieving Specific Data

```python
# Example 7: Get specific data
print("\n9. Retrieving specific data...")
if user_ids:
    user_data = db.get_data(user_ids[0])
    if user_data:
        print(f"User data for {user_data['data']['username']}:")
        print(f"  Email: {user_data['data']['email']}")
        print(f"  Age: {user_data['data'].get('age', 'N/A')}")
        print(f"  Active: {user_data['data']['is_active']}")
        print(f"  Blockchain Transaction ID: {user_data['blockchain_transaction_id']}")
        print(f"  Blockchain Block Index: {user_data['blockchain_block_index']}")
```

**Demonstrates**:
- Individual record retrieval
- Blockchain transaction tracking
- Optional field handling
- Data formatting

## Example 10: Blockchain Information

```python
# Example 8: View blockchain information
print("\n10. Blockchain Information:")
blockchain_info = db.get_blockchain_info()
print(f"Chain Length: {blockchain_info['chain_length']}")
print(f"Pending Transactions: {blockchain_info['pending_transactions']}")
print(f"Difficulty: {blockchain_info['difficulty']}")
print(f"Chain Valid: {blockchain_info['is_valid']}")

if blockchain_info['latest_block']:
    latest = blockchain_info['latest_block']
    print(f"Latest Block: #{latest['index']} (Hash: {latest['hash'][:16]}...)")
```

**Demonstrates**:
- Blockchain status checking
- Chain validation
- Block information retrieval
- Hash display

## Example 11: Data Models Information

```python
# Example 9: View all data models
print("\n11. Data Models:")
models = db.get_data_models()
for model in models:
    print(f"Model: {model['name']}")
    print(f"  Description: {model['description']}")
    print(f"  Version: {model['version']}")
    print(f"  Fields: {len(model['fields'])}")
    for field in model['fields']:
        required = "required" if field['required'] else "optional"
        print(f"    - {field['name']} ({field['type']}, {required})")
    print()
```

**Demonstrates**:
- Model enumeration
- Field information display
- Schema inspection
- Metadata retrieval

## Example 12: Data Export

```python
# Example 10: Export data
print("\n12. Exporting data...")
if db.export_data("hyperledger_export.json"):
    print("Data exported successfully to hyperledger_export.json")
```

**Demonstrates**:
- Complete data export
- JSON file creation
- Export validation

## Example 13: Complete Data Summary

```python
# Example 11: Get all data
print("\n13. All Data Records:")
all_data = db.get_all_data()
print(f"Total records: {len(all_data)}")

# Group by model
by_model = {}
for record in all_data:
    model = record['model_name']
    if model not in by_model:
        by_model[model] = []
    by_model[model].append(record)

for model_name, records in by_model.items():
    print(f"\n{model_name} records ({len(records)}):")
    for record in records:
        data = record['data']
        if model_name == "User":
            print(f"  - {data['username']} ({data['email']})")
        elif model_name == "Product":
            print(f"  - {data['name']} (${data['price']})")
```

**Demonstrates**:
- Complete data retrieval
- Data grouping
- Model-specific formatting
- Record counting

## Expected Output

The example produces comprehensive output showing:

```
=== Hyperledger Integrated Database System Example ===

1. Creating User data model...
Data model 'User' created successfully

2. Creating Product data model...
Data model 'Product' created successfully

3. Mining first block to commit model creation...
Block 1 mined successfully with 3 transactions

4. Adding user data...
Data added to model 'User' with ID: bcc4e1ee-76fb-43bb-91f6-020588d891e0
Added user: john_doe (ID: bcc4e1ee-76fb-43bb-91f6-020588d891e0)
Data added to model 'User' with ID: 01f6ced1-2eb3-4980-b11c-0d66aff63f73
Added user: jane_smith (ID: 01f6ced1-2eb3-4980-b11c-0d66aff63f73)
Data added to model 'User' with ID: 7a8b9c0d-1e2f-3g4h-5i6j-7k8l9m0n1o2p
Added user: bob_wilson (ID: 7a8b9c0d-1e2f-3g4h-5i6j-7k8l9m0n1o2p)

5. Adding product data...
Data added to model 'Product' with ID: 9o8i7u6y5t4r3e2w1q
Added product: Laptop (ID: 9o8i7u6y5t4r3e2w1q)
Data added to model 'Product' with ID: 1q2w3e4r5t6y7u8i9o
Added product: Coffee Mug (ID: 1q2w3e4r5t6y7u8i9o)
Data added to model 'Product' with ID: 0p9o8i7u6y5t4r3e2w
Added product: Running Shoes (ID: 0p9o8i7u6y5t4r3e2w)

6. Mining second block to commit data creation...
Block 2 mined successfully with 7 transactions

7. Updating user data...
Data updated for record: bcc4e1ee-76fb-43bb-91f6-020588d891e0
Updated user: john_doe_updated

8. Searching for data...
Found 2 active users:
  - john_doe_updated (john.updated@example.com)
  - jane_smith (jane@example.com)

Found 2 products in stock:
  - Laptop ($999.99)
  - Coffee Mug ($12.5)

Found 1 electronics products:
  - Laptop ($999.99)

9. Retrieving specific data...
User data for john_doe_updated:
  Email: john.updated@example.com
  Age: 31
  Active: True
  Blockchain Transaction ID: abc123-def456-ghi789
  Blockchain Block Index: 2

10. Blockchain Information:
Chain Length: 3
Pending Transactions: 1
Difficulty: 2
Chain Valid: True
Latest Block: #2 (Hash: 00cb4c47aba9699e...)

11. Data Models:
Model: User
  Description: User account information
  Version: 1.0
  Fields: 5
    - username (text, required)
    - email (text, required)
    - age (integer, optional)
    - is_active (boolean, required)
    - metadata (json, optional)

Model: Product
  Description: Product catalog information
  Version: 1.0
  Fields: 5
    - name (text, required)
    - price (real, required)
    - category (text, required)
    - in_stock (boolean, required)
    - created_at (datetime, required)

12. Exporting data...
Data exported successfully to hyperledger_export.json

13. All Data Records:
Total records: 6

User records (3):
  - john_doe_updated (john.updated@example.com)
  - jane_smith (jane@example.com)
  - bob_wilson (bob@example.com)

Product records (3):
  - Laptop ($999.99)
  - Coffee Mug ($12.5)
  - Running Shoes ($89.99)

=== Example completed successfully! ===
```

## Key Learning Points

### 1. Dynamic Schema Creation
- Create data models at runtime
- Define custom fields with types
- Set validation rules and defaults

### 2. Data Operations
- Add data with automatic validation
- Update existing records
- Handle optional fields gracefully

### 3. Blockchain Integration
- Every operation creates a transaction
- Manual block mining for control
- Complete audit trail

### 4. Search and Query
- Search by exact field matches
- Filter by model type
- Handle multiple search criteria

### 5. Data Export
- Export complete database state
- JSON format for portability
- Include blockchain information

### 6. Error Handling
- Graceful handling of validation errors
- Clear error messages
- Transaction rollback on failures

## Usage Patterns

### 1. Model Creation Pattern
```python
# Define fields
fields = [
    {'name': 'field_name', 'type': 'text', 'required': True},
    # ... more fields
]

# Create model
db.create_data_model("ModelName", fields, "Description")

# Mine block to commit
db.mine_block()
```

### 2. Data Addition Pattern
```python
# Add data
data = {'field1': 'value1', 'field2': 'value2'}
record_id = db.add_data("ModelName", data)

# Mine block to commit
db.mine_block()
```

### 3. Search Pattern
```python
# Search with criteria
results = db.search_data("ModelName", {'field': 'value'})

# Process results
for record in results:
    print(record['data'])
```

### 4. Update Pattern
```python
# Get current data
record = db.get_data(record_id)
current_data = record['data']

# Update data
updated_data = current_data.copy()
updated_data['field'] = 'new_value'

# Save update
db.update_data(record_id, updated_data)
db.mine_block()
```

This comprehensive example demonstrates all major features of the HyperDB system and provides a solid foundation for understanding how to use the database effectively. 