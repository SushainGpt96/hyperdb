#!/usr/bin/env python3
"""
Simple API wrapper for Hyperledger Integrated Database System

This provides a clean, easy-to-use interface for the integrated database system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.hyperledger_integrated_db import HyperledgerIntegratedDB, DataField
from typing import Dict, List, Any, Optional, Union
import json
import time


class HyperledgerAPI:
    """Simple API wrapper for the Hyperledger Integrated Database System"""
    
    def __init__(self, db_path: str = "hyperledger_api.db", blockchain_difficulty: int = 2):
        """Initialize the API with database connection"""
        self.db = HyperledgerIntegratedDB(db_path, blockchain_difficulty)
    
    def create_model(self, name: str, fields: List[Dict[str, Any]], description: str = "") -> bool:
        """
        Create a new data model/schema
        
        Args:
            name: Model name
            fields: List of field definitions
            description: Model description
        
        Returns:
            bool: True if successful, False otherwise
        """
        return self.db.create_data_model(name, fields, description)
    
    def add_record(self, model_name: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Add a record to a specific model
        
        Args:
            model_name: Name of the model to add data to
            data: Data dictionary to add
        
        Returns:
            str: Record ID if successful, None otherwise
        """
        return self.db.add_data(model_name, data)
    
    def update_record(self, record_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing record
        
        Args:
            record_id: ID of the record to update
            data: New data dictionary
        
        Returns:
            bool: True if successful, False otherwise
        """
        return self.db.update_data(record_id, data)
    
    def get_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific record by ID
        
        Args:
            record_id: ID of the record to retrieve
        
        Returns:
            dict: Record data if found, None otherwise
        """
        return self.db.get_data(record_id)
    
    def search_records(self, model_name: str = None, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for records based on criteria
        
        Args:
            model_name: Optional model name to filter by
            criteria: Search criteria dictionary
        
        Returns:
            list: List of matching records
        """
        return self.db.search_data(model_name, criteria)
    
    def get_all_records(self, model_name: str = None) -> List[Dict[str, Any]]:
        """
        Get all records, optionally filtered by model
        
        Args:
            model_name: Optional model name to filter by
        
        Returns:
            list: List of all records
        """
        return self.db.get_all_data(model_name)
    
    def get_models(self) -> List[Dict[str, Any]]:
        """
        Get all data models
        
        Returns:
            list: List of all data models
        """
        return self.db.get_data_models()
    
    def mine_block(self) -> Optional[Dict[str, Any]]:
        """
        Mine a new block with pending transactions
        
        Returns:
            dict: Block information if successful, None otherwise
        """
        return self.db.mine_block()
    
    def get_blockchain_info(self) -> Dict[str, Any]:
        """
        Get blockchain information
        
        Returns:
            dict: Blockchain information
        """
        return self.db.get_blockchain_info()
    
    def export_data(self, filepath: str) -> bool:
        """
        Export all data to JSON file
        
        Args:
            filepath: Path to export file
        
        Returns:
            bool: True if successful, False otherwise
        """
        return self.db.export_data(filepath)
    
    def close(self) -> None:
        """Close the database connection"""
        self.db.disconnect()
    
    # Convenience methods for common operations
    
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
    
    def get_users(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Get all users, optionally filtered by active status"""
        if active_only:
            return self.search_records("User", {'is_active': True})
        return self.get_all_records("User")
    
    def get_products(self, in_stock_only: bool = False) -> List[Dict[str, Any]]:
        """Get all products, optionally filtered by stock status"""
        if in_stock_only:
            return self.search_records("Product", {'in_stock': True})
        return self.get_all_records("Product")
    
    def get_orders(self, status: str = None) -> List[Dict[str, Any]]:
        """Get all orders, optionally filtered by status"""
        if status:
            return self.search_records("Order", {'status': status})
        return self.get_all_records("Order")
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        users = self.search_records("User", {'username': username})
        return users[0] if users else None
    
    def get_product_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get product by name"""
        products = self.search_records("Product", {'name': name})
        return products[0] if products else None
    
    def update_user_status(self, user_id: str, is_active: bool) -> bool:
        """Update user active status"""
        user_data = self.get_record(user_id)
        if user_data:
            user_data['data']['is_active'] = is_active
            return self.update_record(user_id, user_data['data'])
        return False
    
    def update_product_stock(self, product_id: str, in_stock: bool) -> bool:
        """Update product stock status"""
        product_data = self.get_record(product_id)
        if product_data:
            product_data['data']['in_stock'] = in_stock
            return self.update_record(product_id, product_data['data'])
        return False
    
    def update_order_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        order_data = self.get_record(order_id)
        if order_data:
            order_data['data']['status'] = status
            return self.update_record(order_id, order_data['data'])
        return False


# Context manager for easy usage
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


# Example usage functions
def quick_start_example():
    """Quick start example showing basic usage"""
    with HyperledgerContext("quick_start.db") as api:
        # Create models
        api.create_user_model()
        api.create_product_model()
        
        # Mine block to commit models
        api.mine_block()
        
        # Add some data
        user_id = api.add_user("john_doe", "john@example.com", "hashed_password_123")
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


if __name__ == "__main__":
    print("=== Hyperledger API Examples ===\n")
    
    print("1. Quick Start Example:")
    quick_start_example()
    
    print("\n2. E-commerce Example:")
    ecommerce_example()
    
    print("\nExamples completed!") 