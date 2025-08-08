# HyperDB - Project Structure

## Overview

The project has been reorganized into a well-structured Python package with clear separation of concerns and proper organization by functionality.

## Project Structure

```
hyperdb/
├── src/                          # Source code package
│   ├── __init__.py              # Package initialization
│   ├── core/                    # Core database functionality
│   │   ├── __init__.py         # Core package initialization
│   │   └── hyperledger_integrated_db.py  # Main database system
│   ├── api/                     # API wrapper and convenience methods
│   │   ├── __init__.py         # API package initialization
│   │   └── hyperledger_api.py  # Simplified API wrapper
│   ├── examples/                # Usage examples and demonstrations
│   │   ├── __init__.py         # Examples package initialization
│   │   └── example_hyperledger_usage.py  # Comprehensive usage examples
│   └── tests/                   # Test scripts and validation
│       ├── __init__.py         # Tests package initialization
│       └── test_validation.py  # Validation testing examples
├── docs/                        # Documentation
│   ├── README_HYPERLEDGER.md   # Complete documentation
│   └── SYSTEM_SUMMARY.md       # System summary
├── main.py                      # Main entry point
├── setup.py                     # Package setup and installation
├── requirements.txt             # Dependencies
├── README.md                    # Project overview
└── PROJECT_STRUCTURE.md         # This file
```

## Package Organization

### 1. `src/` - Source Code Package
The main source code is organized into logical packages:

#### `src/core/` - Core Functionality
- **Purpose**: Contains the main database system with blockchain integration
- **Key Files**:
  - `hyperledger_integrated_db.py`: Main database class with blockchain integration
  - `__init__.py`: Exports main classes for easy importing

#### `src/api/` - API Wrapper
- **Purpose**: Provides simplified interfaces and convenience methods
- **Key Files**:
  - `hyperledger_api.py`: Simplified API wrapper with context managers
  - `__init__.py`: Exports API classes

#### `src/examples/` - Usage Examples
- **Purpose**: Contains comprehensive examples and demonstrations
- **Key Files**:
  - `example_hyperledger_usage.py`: Complete usage examples
  - `__init__.py`: Package initialization

#### `src/tests/` - Test Scripts
- **Purpose**: Contains validation and testing scripts
- **Key Files**:
  - `test_validation.py`: Validation testing examples
  - `__init__.py`: Package initialization

### 2. `docs/` - Documentation
- **Purpose**: Contains all project documentation
- **Key Files**:
  - `README_HYPERLEDGER.md`: Complete documentation and usage guide
  - `SYSTEM_SUMMARY.md`: System overview and summary

### 3. Root Level Files
- **`main.py`**: Main entry point demonstrating the reorganized structure
- **`setup.py`**: Package setup for installation
- **`requirements.txt`**: Project dependencies
- **`README.md`**: Project overview and quick start guide

## Benefits of This Structure

### 1. **Clear Separation of Concerns**
- Core functionality is isolated in `src/core/`
- API wrappers are separate in `src/api/`
- Examples are organized in `src/examples/`
- Tests are in their own package `src/tests/`

### 2. **Easy Importing**
```python
# Import core functionality
from src.core.hyperledger_integrated_db import HyperledgerIntegratedDB

# Import API wrapper
from src.api.hyperledger_api import HyperledgerAPI, HyperledgerContext
```

### 3. **Scalable Architecture**
- Easy to add new features to appropriate packages
- Clear organization for future development
- Proper Python package structure

### 4. **Development Workflow**
- Core development: Work in `src/core/`
- API development: Work in `src/api/`
- Examples: Add to `src/examples/`
- Tests: Add to `src/tests/`

## Usage Examples

### Basic Usage
```python
# Import core functionality
from src.core.hyperledger_integrated_db import HyperledgerIntegratedDB

# Initialize database
db = HyperledgerIntegratedDB("my_database.db")

# Create model and add data
fields = [{'name': 'username', 'type': 'text', 'required': True}]
db.create_data_model("User", fields)
db.add_data("User", {'username': 'john'})
db.mine_block()
```

### API Wrapper Usage
```python
# Import API wrapper
from src.api.hyperledger_api import HyperledgerContext

# Use context manager
with HyperledgerContext("api_database.db") as api:
    api.create_user_model()
    api.mine_block()
    user_id = api.add_user("alice", "alice@example.com", "password_hash")
    api.mine_block()
```

### Running Examples
```bash
# Run main demo
python main.py

# Run comprehensive example
python src/examples/example_hyperledger_usage.py

# Run validation tests
python src/tests/test_validation.py
```

## Installation and Setup

### Development Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Package Installation
```bash
# Install the package
pip install .
```

## File Dependencies

### Import Dependencies
- `src/api/hyperledger_api.py` imports from `src/core/hyperledger_integrated_db.py`
- `src/examples/example_hyperledger_usage.py` imports from `src/core/hyperledger_integrated_db.py`
- `src/tests/test_validation.py` imports from `src/core/hyperledger_integrated_db.py`
- `main.py` imports from both `src/core/` and `src/api/`

### External Dependencies
- `blockchain.py`: Core blockchain implementation
- `cryptography`: For cryptographic operations
- `sqlite3`: For database operations (built-in)

## Future Enhancements

This structure makes it easy to add:

1. **New Core Features**: Add to `src/core/`
2. **New API Methods**: Add to `src/api/`
3. **New Examples**: Add to `src/examples/`
4. **New Tests**: Add to `src/tests/`
5. **New Documentation**: Add to `docs/`

## Testing the Structure

All components have been tested and work correctly:

✅ **Core Functionality**: `src/core/hyperledger_integrated_db.py` works
✅ **API Wrapper**: `src/api/hyperledger_api.py` works
✅ **Examples**: `src/examples/example_hyperledger_usage.py` works
✅ **Tests**: `src/tests/test_validation.py` works
✅ **Main Entry**: `main.py` demonstrates the structure
✅ **Imports**: All import statements work correctly

The project is now properly organized and ready for development and deployment! 