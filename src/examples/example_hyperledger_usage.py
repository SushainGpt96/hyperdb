#!/usr/bin/env python3
"""
Example usage of Hyperledger Integrated Database System

This example demonstrates:
1. Creating dynamic data models/schemas at runtime
2. Adding data to the database with automatic blockchain storage
3. Mining blocks to commit transactions
4. Searching and retrieving data
5. Viewing blockchain information
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.hyperledger_integrated_db import HyperledgerIntegratedDB
import json
import time


def main():
    """Main example function"""
    print("=== Hyperledger Integrated Database System Example ===\n")
    
    # Initialize the integrated database system
    db = HyperledgerIntegratedDB(db_path="example_hyperledger.db")
    
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
    
    # Mine the first block to commit the model creation transactions
    print("\n3. Mining first block to commit model creation...")
    block_info = db.mine_block()
    if block_info:
        print(f"Block {block_info['index']} mined with {block_info['transaction_count']} transactions")
    
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
    
    # Mine another block to commit the data creation transactions
    print("\n6. Mining second block to commit data creation...")
    block_info = db.mine_block()
    if block_info:
        print(f"Block {block_info['index']} mined with {block_info['transaction_count']} transactions")
    
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
    
    # Example 10: Export data
    print("\n12. Exporting data...")
    if db.export_data("hyperledger_export.json"):
        print("Data exported successfully to hyperledger_export.json")
    
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
    
    # Close the database connection
    db.disconnect()
    print("\n=== Example completed successfully! ===")


if __name__ == "__main__":
    main() 