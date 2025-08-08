#!/usr/bin/env python3
"""
Test script to demonstrate validation features of the Hyperledger Integrated Database System
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.hyperledger_integrated_db import HyperledgerIntegratedDB


def test_validation():
    """Test various validation scenarios"""
    print("=== Validation Test ===\n")
    
    # Initialize database
    db = HyperledgerIntegratedDB("validation_test.db")
    
    # Create a test model
    test_fields = [
        {'name': 'name', 'type': 'text', 'required': True, 'description': 'Name field'},
        {'name': 'age', 'type': 'integer', 'required': True, 'description': 'Age field'},
        {'name': 'score', 'type': 'real', 'required': False, 'description': 'Score field'},
        {'name': 'is_active', 'type': 'boolean', 'required': False, 'default': True, 'description': 'Active status'},
        {'name': 'metadata', 'type': 'json', 'required': False, 'description': 'Additional data'}
    ]
    
    db.create_data_model("TestModel", test_fields, "Test model for validation")
    db.mine_block()
    
    print("1. Testing valid data...")
    try:
        valid_data = {
            'name': 'John Doe',
            'age': 30,
            'score': 95.5,
            'is_active': True,
            'metadata': {'department': 'IT', 'skills': ['Python', 'Java']}
        }
        record_id = db.add_data("TestModel", valid_data)
        if record_id:
            print(f"✓ Valid data added successfully: {record_id}")
        else:
            print("✗ Failed to add valid data")
    except Exception as e:
        print(f"✗ Unexpected error with valid data: {e}")
    
    print("\n2. Testing missing required field...")
    try:
        invalid_data = {
            'name': 'Jane Doe',
            'score': 85.0,
            'is_active': True
            # Missing 'age' field
        }
        record_id = db.add_data("TestModel", invalid_data)
        if record_id is None:
            print("✓ Correctly caught validation error: Required field 'age' is missing")
        else:
            print("✗ Should have failed - missing required field")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print("\n3. Testing wrong data type...")
    try:
        invalid_data = {
            'name': 'Bob Smith',
            'age': 'not_a_number',  # Should be integer
            'is_active': True
        }
        record_id = db.add_data("TestModel", invalid_data)
        if record_id is None:
            print("✓ Correctly caught validation error: Field 'age' must be an integer")
        else:
            print("✗ Should have failed - wrong data type")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print("\n4. Testing boolean field with wrong type...")
    try:
        invalid_data = {
            'name': 'Alice Johnson',
            'age': 25,
            'is_active': 'yes'  # Should be boolean
        }
        record_id = db.add_data("TestModel", invalid_data)
        if record_id is None:
            print("✓ Correctly caught validation error: Field 'is_active' must be a boolean")
        else:
            print("✗ Should have failed - wrong boolean type")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print("\n5. Testing JSON field with wrong type...")
    try:
        invalid_data = {
            'name': 'Charlie Brown',
            'age': 35,
            'is_active': True,
            'metadata': 'not_json'  # Should be dict or list
        }
        record_id = db.add_data("TestModel", invalid_data)
        if record_id is None:
            print("✓ Correctly caught validation error: Field 'metadata' must be a JSON object or array")
        else:
            print("✗ Should have failed - wrong JSON type")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print("\n6. Testing optional field with default...")
    try:
        minimal_data = {
            'name': 'David Wilson',
            'age': 28
            # 'is_active' should default to True
        }
        record_id = db.add_data("TestModel", minimal_data)
        if record_id:
            print(f"✓ Minimal data with defaults added successfully: {record_id}")
        else:
            print("✗ Failed to add minimal data with defaults")
    except Exception as e:
        print(f"✗ Unexpected error with minimal data: {e}")
    
    print("\n7. Testing data update validation...")
    try:
        # Get the first record
        records = db.get_all_data("TestModel")
        if records:
            record_id = records[0]['id']
            current_data = records[0]['data']
            
            # Try to update with invalid data
            invalid_update = current_data.copy()
            invalid_update['age'] = 'invalid_age'
            
            success = db.update_data(record_id, invalid_update)
            if not success:
                print("✓ Correctly caught validation error on update: Field 'age' must be an integer")
            else:
                print("✗ Should have failed - invalid update")
        else:
            print("No records to test update")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Mine block to commit any successful transactions
    db.mine_block()
    
    print("\n8. Final data summary...")
    all_records = db.get_all_data("TestModel")
    print(f"Total records in TestModel: {len(all_records)}")
    
    for i, record in enumerate(all_records, 1):
        print(f"Record {i}: {record['data']['name']} (age: {record['data']['age']})")
    
    # Close database
    db.disconnect()
    print("\n=== Validation test completed ===")


if __name__ == "__main__":
    test_validation() 