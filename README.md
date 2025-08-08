# HyperDB - Database with Built-in Blockchain

**A Python-based database system that integrates blockchain storage with traditional database operations, inspired by Hyperledger Fabric's approach.**

## 🚀 Overview

HyperDB is a revolutionary database system that combines the reliability of traditional databases with the immutability and audit trail of blockchain technology. Every database operation is automatically stored on a blockchain, providing complete transparency and data integrity.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Component Documentation](#component-documentation)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## ✨ Features

### 🔧 Core Features
- **Dynamic Schema Creation**: Create data models/schemas at runtime
- **Automatic Blockchain Storage**: Every operation stored on blockchain with timestamps
- **Single Node Architecture**: Simplified blockchain implementation (no distributed consensus)
- **Data Validation**: Automatic validation against defined schemas
- **Complete Audit Trail**: Full history of all data changes
- **Search and Query**: Powerful search capabilities with complex criteria
- **Export/Import**: Full data export functionality

### 🛡️ Data Integrity
- **Type Safety**: Automatic type validation for all fields
- **Required Field Enforcement**: Ensures all required data is provided
- **Immutable Records**: Once committed to blockchain, data cannot be altered
- **Transaction History**: Complete audit trail of all operations

### 🔍 Advanced Features
- **Multiple Data Types**: Support for text, integer, real, boolean, datetime, and JSON
- **Flexible Schemas**: Create custom data models with any field combination
- **Block Mining**: Manual control over when transactions are committed
- **Context Managers**: Automatic resource management with context managers

## 🏗️ Architecture

### System Components

```
HyperDB/
├── blockchain.py                    # Core blockchain implementation
├── src/
│   ├── core/
│   │   └── hyperledger_integrated_db.py  # Main database system
│   ├── api/
│   │   └── hyperledger_api.py            # Simplified API wrapper
│   ├── examples/
│   │   └── example_hyperledger_usage.py  # Usage examples
│   └── tests/
│       └── test_validation.py            # Validation tests
├── docs/                           # Documentation
├── main.py                         # Main entry point
└── requirements.txt                # Dependencies
```

### Database Schema

The system creates 4 main tables:

1. **`data_models`** - Stores schema definitions
2. **`data_records`** - Stores actual data records
3. **`blockchain_transactions`** - Stores all blockchain transactions
4. **`blockchain_blocks`** - Stores mined blockchain blocks

### Blockchain Integration

Every database operation creates a blockchain transaction with:
- **Transaction ID**: Unique identifier for each operation
- **Transaction Type**: `model_creation`, `data_creation`, `data_update`
- **Timestamp**: When the operation occurred
- **Data**: Complete operation details
- **Block Index**: Which block contains the transaction

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd HyperDB

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Dependencies
- `cryptography>=3.0` - For cryptographic operations
- `sqlite3` - Built-in Python database (no installation needed)

## 🎯 Quick Start

### Basic Usage

```python
from src.core.hyperledger_integrated_db import HyperledgerIntegratedDB

# Initialize the database
db = HyperledgerIntegratedDB("my_database.db")

# Create a data model
fields = [
    {'name': 'username', 'type': 'text', 'required': True},
    {'name': 'email', 'type': 'text', 'required': True},
    {'name': 'age', 'type': 'integer', 'required': False}
]
db.create_data_model("User", fields, "User account information")

# Add data
user_data = {'username': 'john_doe', 'email': 'john@example.com', 'age': 30}
record_id = db.add_data("User", user_data)

# Mine block to commit transactions
db.mine_block()

# Search data
users = db.search_data("User", {'age': 30})
print(f"Found {len(users)} users aged 30")
```

### Using the API Wrapper

```python
from src.api.hyperledger_api import HyperledgerContext

# Use context manager for automatic cleanup
with HyperledgerContext("api_database.db") as api:
    # Create standard models
    api.create_user_model()
    api.create_product_model()
    
    # Mine block to commit models
    api.mine_block()
    
    # Add data
    user_id = api.add_user("alice", "alice@example.com", "password_hash")
    product_id = api.add_product("Laptop", 999.99, "Electronics")
    
    # Mine block to commit data
    api.mine_block()
    
    # Search data
    users = api.get_users(active_only=True)
    products = api.get_products(in_stock_only=True)
```

## 📚 Component Documentation

For detailed information about each component, see the individual README files:

### Core Components

- **[Blockchain Implementation](docs/README_blockchain.md)** - Core blockchain system with proof-of-work mining
- **[Core Database System](docs/README_core_database.md)** - Main database with dynamic schema creation and validation
- **[API Wrapper](docs/README_api_wrapper.md)** - Simplified interface with pre-built models and convenience methods
- **[Examples](docs/README_examples.md)** - Comprehensive usage examples and demonstrations
- **[Validation Tests](docs/README_tests.md)** - Data validation testing and error handling
- **[Main Entry Point](docs/README_main.md)** - Project structure and main demo

### Key Features by Component

#### Blockchain System (`blockchain.py`)
- **Block Class**: Represents individual blocks with transactions
- **Blockchain Class**: Manages the entire blockchain
- **Proof-of-Work Mining**: Configurable difficulty levels
- **Chain Validation**: Ensures blockchain integrity
- **Transaction Management**: Handles pending transactions

#### Core Database (`src/core/hyperledger_integrated_db.py`)
- **Dynamic Schema Creation**: Create models at runtime
- **Data Validation**: Automatic type checking and required field enforcement
- **Blockchain Integration**: Every operation creates a transaction
- **Search Functionality**: Query data with complex criteria
- **Data Export**: Complete database export to JSON

#### API Wrapper (`src/api/hyperledger_api.py`)
- **Pre-built Models**: User, Product, Order models
- **Convenience Methods**: Helper functions for common operations
- **Context Management**: Automatic resource cleanup
- **Simplified Interface**: Easy-to-use API methods

#### Examples (`src/examples/example_hyperledger_usage.py`)
- **Complete System Demo**: Shows all major features
- **Data Model Creation**: Dynamic schema examples
- **Data Operations**: Add, update, search operations
- **Blockchain Integration**: Mining and transaction examples

#### Tests (`src/tests/test_validation.py`)
- **Type Validation**: Tests all data types
- **Required Field Testing**: Ensures required fields are enforced
- **Error Handling**: Validates error messages and recovery
- **Update Validation**: Tests data update validation

## 📖 Usage Examples

### E-commerce System

```python
from src.api.hyperledger_api import HyperledgerContext

with HyperledgerContext("ecommerce.db") as api:
    # Create models
    api.create_user_model()
    api.create_product_model()
    api.create_order_model()
    
    # Mine block to commit models
    api.mine_block()
    
    # Add users
    user1_id = api.add_user("alice", "alice@example.com", "hash1")
    user2_id = api.add_user("bob", "bob@example.com", "hash2")
    
    # Add products
    laptop_id = api.add_product("Laptop", 999.99, "Electronics")
    shoes_id = api.add_product("Running Shoes", 89.99, "Sports")
    
    # Mine block to commit users and products
    api.mine_block()
    
    # Add orders
    order1_items = [{"product_id": laptop_id, "quantity": 1, "price": 999.99}]
    api.add_order(user1_id, order1_items, 999.99)
    
    order2_items = [{"product_id": shoes_id, "quantity": 2, "price": 89.99}]
    api.add_order(user2_id, order2_items, 179.98)
    
    # Mine block to commit orders
    api.mine_block()
    
    # Query data
    users = api.get_users()
    products = api.get_products()
    orders = api.get_orders()
    
    print(f"Users: {len(users)}")
    print(f"Products: {len(products)}")
    print(f"Orders: {len(orders)}")
```

### Blog System

```python
from src.core.hyperledger_integrated_db import HyperledgerIntegratedDB
import time

db = HyperledgerIntegratedDB("blog.db")

# Create blog post model
post_fields = [
    {'name': 'title', 'type': 'text', 'required': True},
    {'name': 'content', 'type': 'text', 'required': True},
    {'name': 'author', 'type': 'text', 'required': True},
    {'name': 'published', 'type': 'boolean', 'required': True, 'default': False},
    {'name': 'tags', 'type': 'json', 'required': False},
    {'name': 'created_at', 'type': 'datetime', 'required': True}
]

db.create_data_model("BlogPost", post_fields, "Blog post data")
db.mine_block()

# Add blog posts
posts = [
    {
        'title': 'Introduction to HyperDB',
        'content': 'HyperDB is a revolutionary database system...',
        'author': 'John Doe',
        'published': True,
        'tags': ['database', 'blockchain'],
        'created_at': time.time()
    },
    {
        'title': 'Advanced Blockchain Features',
        'content': 'Learn about advanced blockchain features...',
        'author': 'Jane Smith',
        'published': False,
        'tags': ['blockchain', 'advanced'],
        'created_at': time.time()
    }
]

for post in posts:
    db.add_data("BlogPost", post)

db.mine_block()

# Search published posts
published_posts = db.search_data("BlogPost", {'published': True})
print(f"Published posts: {len(published_posts)}")

# Search by author
john_posts = db.search_data("BlogPost", {'author': 'John Doe'})
print(f"John's posts: {len(john_posts)}")
```

## 🧪 Testing

### Running Tests

```bash
# Run validation tests
python src/tests/test_validation.py

# Run examples
python src/examples/example_hyperledger_usage.py

# Run main demo
python main.py
```

### Test Coverage

The test suite covers:

1. **Data Validation**
   - Valid data types
   - Required field enforcement
   - Type checking
   - Error handling

2. **Schema Creation**
   - Dynamic model creation
   - Field definition
   - Model persistence

3. **Data Operations**
   - Adding data
   - Updating data
   - Retrieving data
   - Searching data

4. **Blockchain Operations**
   - Transaction creation
   - Block mining
   - Chain validation

### Example Test Output

```
=== Validation Test ===

1. Testing valid data...
✓ Valid data added successfully: bae5bd67-9cda-4b86-a0d9-9d3082b93770

2. Testing missing required field...
✓ Correctly caught validation error: Required field 'age' is missing

3. Testing wrong data type...
✓ Correctly caught validation error: Field 'age' must be an integer

4. Testing boolean field with wrong type...
✓ Correctly caught validation error: Field 'is_active' must be a boolean

5. Testing JSON field with wrong type...
✓ Correctly caught validation error: Field 'metadata' must be a JSON object or array
```

## 📁 Project Structure

```
HyperDB/
├── blockchain.py                    # Core blockchain implementation
├── main.py                         # Main entry point
├── setup.py                        # Package setup
├── requirements.txt                 # Dependencies
├── src/                           # Source code
│   ├── core/                      # Core database functionality
│   │   ├── __init__.py
│   │   └── hyperledger_integrated_db.py
│   ├── api/                       # API wrapper and convenience methods
│   │   ├── __init__.py
│   │   └── hyperledger_api.py
│   ├── examples/                  # Usage examples
│   │   ├── __init__.py
│   │   └── example_hyperledger_usage.py
│   └── tests/                     # Test scripts
│       ├── __init__.py
│       └── test_validation.py
├── docs/                          # Documentation
│   ├── README_blockchain.md       # Blockchain documentation
│   ├── README_core_database.md    # Core database documentation
│   ├── README_api_wrapper.md      # API wrapper documentation
│   ├── README_examples.md         # Examples documentation
│   ├── README_tests.md            # Tests documentation
│   └── README_main.md             # Main entry point documentation
├── README.md                      # This file
├── BRANDING.md                    # Project branding
└── PROJECT_STRUCTURE.md           # Project structure documentation
```

## 🔧 Development

### Adding New Features

1. **Core Features**: Add to `src/core/`
2. **API Wrappers**: Add to `src/api/`
3. **Examples**: Add to `src/examples/`
4. **Tests**: Add to `src/tests/`

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all functions
- Include error handling

### Testing Guidelines

- Test all data types
- Test validation scenarios
- Test blockchain operations
- Test error conditions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For questions, issues, or contributions:

1. Check the component documentation in the individual README files in the `docs/` folder
2. Run the examples in `src/examples/`
3. Review the test cases in `src/tests/`
4. Open an issue on GitHub

## 🎯 Roadmap

### Planned Features
- [ ] Web interface
- [ ] REST API
- [ ] Multi-node support
- [ ] Advanced query language
- [ ] Real-time notifications
- [ ] Data encryption
- [ ] Backup and restore
- [ ] Performance optimization

### Current Status
- ✅ Core database functionality
- ✅ Blockchain integration
- ✅ Data validation
- ✅ Search capabilities
- ✅ API wrapper
- ✅ Examples and tests
- ✅ Documentation

## 📚 Additional Resources

### Component-Specific Documentation

- **[Blockchain Implementation](docs/README_blockchain.md)** - Detailed blockchain system documentation
- **[Core Database System](docs/README_core_database.md)** - Main database functionality and API
- **[API Wrapper](docs/README_api_wrapper.md)** - Simplified interface and convenience methods
- **[Examples](docs/README_examples.md)** - Comprehensive usage examples and demonstrations
- **[Validation Tests](docs/README_tests.md)** - Testing framework and validation scenarios
- **[Main Entry Point](docs/README_main.md)** - Project structure and main demo

### Key Concepts

1. **Dynamic Schema Creation**: Create data models at runtime with custom fields
2. **Blockchain Integration**: Every database operation creates an immutable transaction
3. **Data Validation**: Automatic type checking and required field enforcement
4. **Search and Query**: Powerful search capabilities with complex criteria
5. **Export/Import**: Complete data export functionality with blockchain information

---

**HyperDB** - Where traditional databases meet blockchain technology for ultimate data integrity and transparency. 