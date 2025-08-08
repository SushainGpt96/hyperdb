#!/usr/bin/env python3
"""
Main entry point for HyperDB - Database with Built-in Blockchain

This script demonstrates the reorganized project structure and provides
easy access to the main functionality.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.hyperledger_integrated_db import HyperledgerIntegratedDB
from api.hyperledger_api import HyperledgerAPI, HyperledgerContext


def main():
    """Main function demonstrating the reorganized project structure"""
    print("=== HyperDB - Database with Built-in Blockchain ===\n")
    print("Project Structure:")
    print("├── src/")
    print("│   ├── core/           # Core database functionality")
    print("│   │   ├── __init__.py")
    print("│   │   └── hyperledger_integrated_db.py")
    print("│   ├── api/            # API wrapper and convenience methods")
    print("│   │   ├── __init__.py")
    print("│   │   └── hyperledger_api.py")
    print("│   ├── examples/       # Usage examples")
    print("│   │   ├── __init__.py")
    print("│   │   └── example_hyperledger_usage.py")
    print("│   └── tests/          # Test scripts")
    print("│       ├── __init__.py")
    print("│       └── test_validation.py")
    print("├── docs/               # Documentation")
    print("│   ├── README_HYPERLEDGER.md")
    print("│   └── SYSTEM_SUMMARY.md")
    print("└── main.py             # This file")
    print()
    
    # Demonstrate core functionality
    print("1. Testing Core Functionality:")
    db = HyperledgerIntegratedDB("main_demo.db")
    
    # Create a simple model
    fields = [
        {'name': 'name', 'type': 'text', 'required': True},
        {'name': 'value', 'type': 'integer', 'required': True}
    ]
    
    db.create_data_model("Demo", fields, "Demo model")
    db.mine_block()
    
    # Add some data
    demo_data = {'name': 'Test Item', 'value': 42}
    record_id = db.add_data("Demo", demo_data)
    db.mine_block()
    
    print(f"✓ Created model and added data (ID: {record_id})")
    
    # Demonstrate API wrapper
    print("\n2. Testing API Wrapper:")
    with HyperledgerContext("api_demo.db") as api:
        api.create_user_model()
        api.mine_block()
        
        user_id = api.add_user("demo_user", "demo@example.com", "password_hash")
        api.mine_block()
        
        users = api.get_users()
        print(f"✓ API wrapper working - {len(users)} users created")
    
    # Clean up
    db.disconnect()
    
    print("\n3. Project Structure Benefits:")
    print("✓ Organized by functionality")
    print("✓ Clear separation of concerns")
    print("✓ Easy to import and use")
    print("✓ Proper Python package structure")
    print("✓ Scalable for future additions")
    
    print("\n=== HyperDB project reorganization completed successfully! ===")


if __name__ == "__main__":
    main() 