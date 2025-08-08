# API Wrapper (`src/api/hyperledger_api.py`)

## Overview

The `hyperledger_api.py` file provides a simplified API wrapper for the HyperDB system. This module offers convenience methods and pre-built data models for common use cases, making it easier to use the database system without dealing with the complexity of the core implementation.

## Key Components

### HyperledgerAPI Class

```python
class HyperledgerAPI:
    def __init__(self, db_path: str = "hyperledger_api.db", blockchain_difficulty: int = 2):
        self.db = HyperledgerIntegratedDB(db_path, blockchain_difficulty)
```

**Purpose**: Provides a simplified interface to the core database system.

**Features**:
- Wraps core database functionality
- Provides convenience methods
- Pre-built data models for common use cases
- Simplified error handling

## Standard Data Models

### User Model

```python
def create_user_model(self) -> bool:
    """Create a standard user model"""
    fields = [
        {'name': 'username', 'type': 'text', 'required': True, 'description': 'Unique username'},
        {'name': 'email', 'type': 'text', 'required': True, 'description': 'Email address'},
        {'name': 'password_hash', 'type': 'text', 'required': True, 'description': 'Hashed password'},
        {'name': 'is_active', 'type': 'boolean', 'required': True, 'default': True, 'description': 'Account status'},
        {'name': 'created_at', 'type': 'datetime', 'required': True, 'description': 'Account creation time'},
        {'name': 'metadata', 'type': 'json', 'required': False, 'description': 'Additional user data'}
    ]
    return self.create_model("User", fields, "User account information")
```

**Fields**:
- `username`: Unique username for the user
- `email`: Email address
- `password_hash`: Hashed password for security
- `is_active`: Whether the account is active
- `created_at`: When the account was created
- `metadata`: Additional user data (JSON)

### Product Model

```python
def create_product_model(self) -> bool:
    """Create a standard product model"""
    fields = [
        {'name': 'name', 'type': 'text', 'required': True, 'description': 'Product name'},
        {'name': 'description', 'type': 'text', 'required': False, 'description': 'Product description'},
        {'name': 'price', 'type': 'real', 'required': True, 'description': 'Product price'},
        {'name': 'category', 'type': 'text', 'required': True, 'description': 'Product category'},
        {'name': 'in_stock', 'type': 'boolean', 'required': True, 'default': True, 'description': 'Stock status'},
        {'name': 'created_at', 'type': 'datetime', 'required': True, 'description': 'Product creation time'},
        {'name': 'tags', 'type': 'json', 'required': False, 'description': 'Product tags'}
    ]
    return self.create_model("Product", fields, "Product catalog information")
```

**Fields**:
- `name`: Product name
- `description`: Product description
- `price`: Product price
- `category`: Product category
- `in_stock`: Whether product is in stock
- `created_at`: When product was created
- `tags`: Product tags (JSON array)

### Order Model

```python
def create_order_model(self) -> bool:
    """Create a standard order model"""
    fields = [
        {'name': 'user_id', 'type': 'text', 'required': True, 'description': 'User ID'},
        {'name': 'items', 'type': 'json', 'required': True, 'description': 'Order items'},
        {'name': 'total_amount', 'type': 'real', 'required': True, 'description': 'Order total'},
        {'name': 'status', 'type': 'text', 'required': True, 'default': 'pending', 'description': 'Order status'},
        {'name': 'created_at', 'type': 'datetime', 'required': True, 'description': 'Order creation time'},
        {'name': 'shipping_address', 'type': 'json', 'required': False, 'description': 'Shipping address'}
    ]
    return self.create_model("Order", fields, "Order information")
```

**Fields**:
- `user_id`: Reference to user who placed order
- `items`: Order items (JSON array)
- `total_amount`: Total order amount
- `status`: Order status (pending, shipped, delivered, etc.)
- `created_at`: When order was created
- `shipping_address`: Shipping address (JSON object)

## Convenience Methods

### User Management

#### Adding Users

```python
def add_user(self, username: str, email: str, password_hash: str, metadata: Dict = None) -> Optional[str]:
    """Add a new user"""
    user_data = {
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'is_active': True,
        'created_at': time.time(),
        'metadata': metadata or {}
    }
    return self.add_record("User", user_data)
```

**Purpose**: Adds a new user with standard fields.
**Parameters**:
- `username`: Unique username
- `email`: Email address
- `password_hash`: Hashed password
- `metadata`: Additional user data
**Returns**: User ID if successful, None otherwise

#### Getting Users

```python
def get_users(self, active_only: bool = False) -> List[Dict[str, Any]]:
    """Get all users, optionally filtered by active status"""
    if active_only:
        return self.search_records("User", {'is_active': True})
    return self.get_all_records("User")
```

**Purpose**: Retrieves users with optional filtering.
**Parameters**:
- `active_only`: Only return active users
**Returns**: List of user records

#### Finding Specific Users

```python
def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
    """Get user by username"""
    users = self.search_records("User", {'username': username})
    return users[0] if users else None
```

**Purpose**: Finds a user by username.
**Parameters**:
- `username`: Username to search for
**Returns**: User record if found, None otherwise

#### Updating User Status

```python
def update_user_status(self, user_id: str, is_active: bool) -> bool:
    """Update user active status"""
    user_data = self.get_record(user_id)
    if user_data:
        user_data['data']['is_active'] = is_active
        return self.update_record(user_id, user_data['data'])
    return False
```

**Purpose**: Updates user active status.
**Parameters**:
- `user_id`: User ID to update
- `is_active`: New active status
**Returns**: True if successful, False otherwise

### Product Management

#### Adding Products

```python
def add_product(self, name: str, price: float, category: str, description: str = None, tags: List[str] = None) -> Optional[str]:
    """Add a new product"""
    product_data = {
        'name': name,
        'description': description or '',
        'price': price,
        'category': category,
        'in_stock': True,
        'created_at': time.time(),
        'tags': tags or []
    }
    return self.add_record("Product", product_data)
```

**Purpose**: Adds a new product with standard fields.
**Parameters**:
- `name`: Product name
- `price`: Product price
- `category`: Product category
- `description`: Product description
- `tags`: Product tags
**Returns**: Product ID if successful, None otherwise

#### Getting Products

```python
def get_products(self, in_stock_only: bool = False) -> List[Dict[str, Any]]:
    """Get all products, optionally filtered by stock status"""
    if in_stock_only:
        return self.search_records("Product", {'in_stock': True})
    return self.get_all_records("Product")
```

**Purpose**: Retrieves products with optional filtering.
**Parameters**:
- `in_stock_only`: Only return products in stock
**Returns**: List of product records

#### Finding Specific Products

```python
def get_product_by_name(self, name: str) -> Optional[Dict[str, Any]]:
    """Get product by name"""
    products = self.search_records("Product", {'name': name})
    return products[0] if products else None
```

**Purpose**: Finds a product by name.
**Parameters**:
- `name`: Product name to search for
**Returns**: Product record if found, None otherwise

#### Updating Product Stock

```python
def update_product_stock(self, product_id: str, in_stock: bool) -> bool:
    """Update product stock status"""
    product_data = self.get_record(product_id)
    if product_data:
        product_data['data']['in_stock'] = in_stock
        return self.update_record(product_id, product_data['data'])
    return False
```

**Purpose**: Updates product stock status.
**Parameters**:
- `product_id`: Product ID to update
- `in_stock`: New stock status
**Returns**: True if successful, False otherwise

### Order Management

#### Adding Orders

```python
def add_order(self, user_id: str, items: List[Dict], total_amount: float, shipping_address: Dict = None) -> Optional[str]:
    """Add a new order"""
    order_data = {
        'user_id': user_id,
        'items': items,
        'total_amount': total_amount,
        'status': 'pending',
        'created_at': time.time(),
        'shipping_address': shipping_address or {}
    }
    return self.add_record("Order", order_data)
```

**Purpose**: Adds a new order with standard fields.
**Parameters**:
- `user_id`: User who placed the order
- `items`: Order items list
- `total_amount`: Total order amount
- `shipping_address`: Shipping address
**Returns**: Order ID if successful, None otherwise

#### Getting Orders

```python
def get_orders(self, status: str = None) -> List[Dict[str, Any]]:
    """Get all orders, optionally filtered by status"""
    if status:
        return self.search_records("Order", {'status': status})
    return self.get_all_records("Order")
```

**Purpose**: Retrieves orders with optional filtering.
**Parameters**:
- `status`: Order status to filter by
**Returns**: List of order records

#### Updating Order Status

```python
def update_order_status(self, order_id: str, status: str) -> bool:
    """Update order status"""
    order_data = self.get_record(order_id)
    if order_data:
        order_data['data']['status'] = status
        return self.update_record(order_id, order_data['data'])
    return False
```

**Purpose**: Updates order status.
**Parameters**:
- `order_id`: Order ID to update
- `status`: New order status
**Returns**: True if successful, False otherwise

## Context Manager

### HyperledgerContext Class

```python
class HyperledgerContext:
    """Context manager for Hyperledger API"""
    
    def __init__(self, db_path: str = "hyperledger_context.db", blockchain_difficulty: int = 2):
        self.db_path = db_path
        self.blockchain_difficulty = blockchain_difficulty
        self.api = None
    
    def __enter__(self):
        self.api = HyperledgerAPI(self.db_path, self.blockchain_difficulty)
        return self.api
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.api:
            self.api.close()
```

**Purpose**: Provides automatic resource management for the API.

**Features**:
- Automatic database connection
- Automatic cleanup on exit
- Exception handling
- Simplified usage pattern

## Usage Examples

### Basic E-commerce System

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
    laptop_id = api.add_product("Laptop", 999.99, "Electronics", "High-performance laptop")
    shoes_id = api.add_product("Running Shoes", 89.99, "Sports", "Comfortable running shoes")
    
    # Mine block to commit users and products
    api.mine_block()
    
    # Add orders
    order1_items = [{"product_id": laptop_id, "quantity": 1, "price": 999.99}]
    api.add_order(user1_id, order1_items, 999.99, {"address": "123 Tech St"})
    
    order2_items = [{"product_id": shoes_id, "quantity": 2, "price": 89.99}]
    api.add_order(user2_id, order2_items, 179.98, {"address": "456 Sports Ave"})
    
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

### User Management System

```python
from src.api.hyperledger_api import HyperledgerContext

with HyperledgerContext("users.db") as api:
    # Create user model
    api.create_user_model()
    api.mine_block()
    
    # Add users
    user1_id = api.add_user("john_doe", "john@example.com", "password_hash_1", 
                           {"preferences": ["tech", "sports"]})
    user2_id = api.add_user("jane_smith", "jane@example.com", "password_hash_2", 
                           {"preferences": ["art", "music"]})
    user3_id = api.add_user("bob_wilson", "bob@example.com", "password_hash_3", 
                           {"preferences": ["cooking"]})
    
    api.mine_block()
    
    # Get all users
    all_users = api.get_users()
    print(f"Total users: {len(all_users)}")
    
    # Get active users only
    active_users = api.get_users(active_only=True)
    print(f"Active users: {len(active_users)}")
    
    # Find specific user
    john = api.get_user_by_username("john_doe")
    if john:
        print(f"Found user: {john['data']['username']} ({john['data']['email']})")
    
    # Update user status
    api.update_user_status(user3_id, is_active=False)
    api.mine_block()
    
    # Check updated status
    updated_active_users = api.get_users(active_only=True)
    print(f"Active users after update: {len(updated_active_users)}")
```

### Product Catalog System

```python
from src.api.hyperledger_api import HyperledgerContext

with HyperledgerContext("catalog.db") as api:
    # Create product model
    api.create_product_model()
    api.mine_block()
    
    # Add products
    products = [
        ("Laptop", 999.99, "Electronics", "High-performance laptop", ["gaming", "tech"]),
        ("Coffee Mug", 12.50, "Kitchen", "Ceramic coffee mug", ["kitchen", "drink"]),
        ("Running Shoes", 89.99, "Sports", "Comfortable running shoes", ["sports", "fitness"]),
        ("Book", 19.99, "Books", "Programming book", ["education", "tech"]),
        ("Headphones", 199.99, "Electronics", "Wireless headphones", ["audio", "tech"])
    ]
    
    for name, price, category, description, tags in products:
        api.add_product(name, price, category, description, tags)
    
    api.mine_block()
    
    # Get all products
    all_products = api.get_products()
    print(f"Total products: {len(all_products)}")
    
    # Get products in stock only
    in_stock_products = api.get_products(in_stock_only=True)
    print(f"Products in stock: {len(in_stock_products)}")
    
    # Find specific product
    laptop = api.get_product_by_name("Laptop")
    if laptop:
        print(f"Found product: {laptop['data']['name']} (${laptop['data']['price']})")
    
    # Update product stock
    if laptop:
        api.update_product_stock(laptop['id'], in_stock=False)
        api.mine_block()
        
        # Check updated stock
        updated_in_stock = api.get_products(in_stock_only=True)
        print(f"Products in stock after update: {len(updated_in_stock)}")
```

## Example Functions

### Quick Start Example

```python
def quick_start_example():
    """Quick start example showing basic usage"""
    with HyperledgerContext("quick_start.db") as api:
        # Create models
        api.create_user_model()
        api.create_product_model()
        
        # Mine block to commit models
        api.mine_block()
        
        # Add some data
        user_id = api.add_user("alice", "alice@example.com", "password_hash")
        product_id = api.add_product("Laptop", 999.99, "Electronics", "High-performance laptop")
        
        # Mine block to commit data
        api.mine_block()
        
        # Search data
        users = api.get_users(active_only=True)
        products = api.get_products(in_stock_only=True)
        
        print(f"Active users: {len(users)}")
        print(f"Products in stock: {len(products)}")
        
        # Get blockchain info
        info = api.get_blockchain_info()
        print(f"Blockchain blocks: {info['chain_length']}")
```

### E-commerce Example

```python
def ecommerce_example():
    """E-commerce example with users, products, and orders"""
    with HyperledgerContext("ecommerce.db") as api:
        # Create all models
        api.create_user_model()
        api.create_product_model()
        api.create_order_model()
        
        # Mine block for models
        api.mine_block()
        
        # Add users
        user1_id = api.add_user("alice", "alice@example.com", "hash1", {"preferences": ["tech"]})
        user2_id = api.add_user("bob", "bob@example.com", "hash2", {"preferences": ["sports"]})
        
        # Add products
        laptop_id = api.add_product("Laptop", 999.99, "Electronics", "Gaming laptop", ["gaming", "tech"])
        shoes_id = api.add_product("Running Shoes", 89.99, "Sports", "Comfortable running shoes", ["sports", "fitness"])
        
        # Mine block for users and products
        api.mine_block()
        
        # Add orders
        order1_items = [{"product_id": laptop_id, "quantity": 1, "price": 999.99}]
        api.add_order(user1_id, order1_items, 999.99, {"address": "123 Tech St"})
        
        order2_items = [{"product_id": shoes_id, "quantity": 2, "price": 89.99}]
        api.add_order(user2_id, order2_items, 179.98, {"address": "456 Sports Ave"})
        
        # Mine block for orders
        api.mine_block()
        
        # Query data
        print("=== E-commerce Data ===")
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
        
        # Export data
        api.export_data("ecommerce_export.json")
```

## Benefits of the API Wrapper

### 1. Simplified Usage
- Pre-built models for common use cases
- Convenience methods for common operations
- Reduced boilerplate code

### 2. Standardized Patterns
- Consistent data structures
- Common field definitions
- Standard validation rules

### 3. Automatic Resource Management
- Context manager for automatic cleanup
- Exception handling
- Connection management

### 4. Easy Integration
- Drop-in replacement for simple use cases
- Compatible with core database system
- Extensible for custom requirements

## Error Handling

The API wrapper includes comprehensive error handling:

### 1. Validation Errors
- Automatic field validation
- Clear error messages
- Graceful failure handling

### 2. Database Errors
- Connection error handling
- Transaction rollback
- Resource cleanup

### 3. Context Manager Errors
- Automatic cleanup on exceptions
- Proper resource disposal
- Exception propagation

## Performance Considerations

### 1. Connection Management
- Efficient connection reuse
- Automatic cleanup
- Connection pooling considerations

### 2. Batch Operations
- Group related operations
- Mine blocks efficiently
- Optimize transaction batching

### 3. Memory Usage
- Context manager prevents memory leaks
- Efficient data structures
- Proper resource disposal

This API wrapper provides a user-friendly interface to the HyperDB system, making it easy to implement common database operations while maintaining the power and flexibility of the core system. 