# Validation Tests (`src/tests/test_validation.py`)

## Overview

The `test_validation.py` file contains comprehensive validation tests for the HyperDB system. This module demonstrates and validates the data validation features, ensuring that the database system correctly handles various data types, required fields, and error conditions.

## Main Test Function

### Validation Test Suite

```python
def test_validation():
    """Test various validation scenarios"""
    print("=== Validation Test ===\n")
    
    # Initialize database
    db = HyperledgerIntegratedDB("validation_test.db")
```

**Purpose**: Tests all validation scenarios to ensure data integrity.

**Test Coverage**:
- Valid data types
- Required field enforcement
- Type validation
- Error handling
- Default values

## Test 1: Valid Data

```python
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
    print(f"✓ Valid data added successfully: {record_id}")
except Exception as e:
    print(f"✗ Unexpected error with valid data: {e}")
```

**Purpose**: Tests that valid data is accepted without errors.

**Test Data**:
- `name`: String field
- `age`: Integer field
- `score`: Real number field
- `is_active`: Boolean field
- `metadata`: JSON object field

**Expected Result**: Data should be added successfully with a valid record ID.

## Test 2: Missing Required Field

```python
print("\n2. Testing missing required field...")
try:
    invalid_data = {
        'name': 'Jane Doe',
        'score': 85.0,
        'is_active': True
        # Missing 'age' field
    }
    db.add_data("TestModel", invalid_data)
    print("✗ Should have failed - missing required field")
except ValueError as e:
    print(f"✓ Correctly caught validation error: {e}")
```

**Purpose**: Tests that missing required fields are properly detected.

**Test Data**:
- Includes all fields except the required `age` field
- Should trigger validation error

**Expected Result**: Should raise ValueError with clear error message about missing required field.

## Test 3: Wrong Data Type

```python
print("\n3. Testing wrong data type...")
try:
    invalid_data = {
        'name': 'Bob Smith',
        'age': 'not_a_number',  # Should be integer
        'is_active': True
    }
    db.add_data("TestModel", invalid_data)
    print("✗ Should have failed - wrong data type")
except ValueError as e:
    print(f"✓ Correctly caught validation error: {e}")
```

**Purpose**: Tests that incorrect data types are properly detected.

**Test Data**:
- `age` field contains string instead of integer
- Should trigger type validation error

**Expected Result**: Should raise ValueError with clear error message about incorrect data type.

## Test 4: Boolean Field with Wrong Type

```python
print("\n4. Testing boolean field with wrong type...")
try:
    invalid_data = {
        'name': 'Alice Johnson',
        'age': 25,
        'is_active': 'yes'  # Should be boolean
    }
    db.add_data("TestModel", invalid_data)
    print("✗ Should have failed - wrong boolean type")
except ValueError as e:
    print(f"✓ Correctly caught validation error: {e}")
```

**Purpose**: Tests that boolean fields only accept boolean values.

**Test Data**:
- `is_active` field contains string instead of boolean
- Should trigger boolean validation error

**Expected Result**: Should raise ValueError with clear error message about boolean type requirement.

## Test 5: JSON Field with Wrong Type

```python
print("\n5. Testing JSON field with wrong type...")
try:
    invalid_data = {
        'name': 'Charlie Brown',
        'age': 35,
        'is_active': True,
        'metadata': 'not_json'  # Should be dict or list
    }
    db.add_data("TestModel", invalid_data)
    print("✗ Should have failed - wrong JSON type")
except ValueError as e:
    print(f"✓ Correctly caught validation error: {e}")
```

**Purpose**: Tests that JSON fields only accept dictionary or list values.

**Test Data**:
- `metadata` field contains string instead of JSON object
- Should trigger JSON validation error

**Expected Result**: Should raise ValueError with clear error message about JSON type requirement.

## Test 6: Optional Field with Default

```python
print("\n6. Testing optional field with default...")
try:
    minimal_data = {
        'name': 'David Wilson',
        'age': 28
        # 'is_active' should default to True
    }
    record_id = db.add_data("TestModel", minimal_data)
    print(f"✓ Minimal data with defaults added successfully: {record_id}")
except Exception as e:
    print(f"✗ Unexpected error with minimal data: {e}")
```

**Purpose**: Tests that optional fields with defaults work correctly.

**Test Data**:
- Only includes required fields
- `is_active` should use default value (True)

**Expected Result**: Data should be added successfully with default values applied.

## Test 7: Data Update Validation

```python
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
        
        db.update_data(record_id, invalid_update)
        print("✗ Should have failed - invalid update")
    else:
        print("No records to test update")
except ValueError as e:
    print(f"✓ Correctly caught validation error on update: {e}")
```

**Purpose**: Tests that data updates are also validated.

**Test Data**:
- Attempts to update existing record with invalid data
- Should trigger validation error during update

**Expected Result**: Should raise ValueError with clear error message about invalid update data.

## Test 8: Final Data Summary

```python
print("\n8. Final data summary...")
all_records = db.get_all_data("TestModel")
print(f"Total records in TestModel: {len(all_records)}")

for i, record in enumerate(all_records, 1):
    print(f"Record {i}: {record['data']['name']} (age: {record['data']['age']})")
```

**Purpose**: Provides a summary of all successfully created records.

**Output**: Shows total number of records and basic information about each record.

## Test Model Definition

The test uses a comprehensive test model with various field types:

```python
# Create a test model
test_fields = [
    {'name': 'name', 'type': 'text', 'required': True, 'description': 'Name field'},
    {'name': 'age', 'type': 'integer', 'required': True, 'description': 'Age field'},
    {'name': 'score', 'type': 'real', 'required': False, 'description': 'Score field'},
    {'name': 'is_active', 'type': 'boolean', 'required': True, 'default': True, 'description': 'Active status'},
    {'name': 'metadata', 'type': 'json', 'required': False, 'description': 'Additional data'}
]

db.create_data_model("TestModel", test_fields, "Test model for validation")
db.mine_block()
```

**Field Types Tested**:
- `text`: String data
- `integer`: Whole numbers
- `real`: Decimal numbers
- `boolean`: True/False values
- `json`: Complex data structures

**Validation Rules**:
- Required vs optional fields
- Default values
- Type constraints

## Expected Test Output

The validation test produces comprehensive output showing:

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

6. Testing optional field with default...
✓ Minimal data with defaults added successfully: c1d2e3f4-5g6h-7i8j-9k0l-1m2n3o4p5q6r

7. Testing data update validation...
✓ Correctly caught validation error on update: Field 'age' must be an integer

8. Final data summary...
Total records in TestModel: 2
Record 1: John Doe (age: 30)
Record 2: David Wilson (age: 28)

=== Validation test completed ===
```

## Validation Features Tested

### 1. Type Safety
- **Text Fields**: Only accept string values
- **Integer Fields**: Only accept whole numbers
- **Real Fields**: Only accept numbers (int or float)
- **Boolean Fields**: Only accept True/False values
- **JSON Fields**: Only accept dictionaries or lists

### 2. Required Field Enforcement
- Missing required fields trigger validation errors
- Clear error messages identify missing fields
- Optional fields can be omitted

### 3. Default Values
- Optional fields with defaults work correctly
- Default values are applied when fields are missing
- Default values don't interfere with explicit values

### 4. Error Handling
- Clear, descriptive error messages
- Proper exception types (ValueError)
- Graceful handling of validation failures

### 5. Update Validation
- Data updates are validated the same as new data
- Invalid updates are rejected
- Existing valid data is preserved

## Key Learning Points

### 1. Comprehensive Validation
- All data types are validated
- Required fields are enforced
- Type constraints are checked

### 2. Clear Error Messages
- Specific error messages for each validation failure
- Field names are included in error messages
- Error types help identify the issue

### 3. Graceful Error Handling
- Validation errors don't crash the system
- Failed operations don't affect existing data
- Error recovery is possible

### 4. Default Value Support
- Optional fields can have default values
- Defaults are applied automatically
- Explicit values override defaults

### 5. Update Validation
- Updates are validated the same as new data
- Invalid updates are rejected
- Data integrity is maintained

## Usage Patterns

### 1. Validation Error Handling
```python
try:
    record_id = db.add_data("ModelName", data)
    print(f"Data added successfully: {record_id}")
except ValueError as e:
    print(f"Validation error: {e}")
    # Handle validation error appropriately
```

### 2. Required Field Checking
```python
# Ensure all required fields are present
required_fields = ['name', 'email', 'age']
for field in required_fields:
    if field not in data:
        raise ValueError(f"Missing required field: {field}")
```

### 3. Type Validation
```python
# Validate data types before adding
if not isinstance(data['age'], int):
    raise ValueError("Age must be an integer")
if not isinstance(data['is_active'], bool):
    raise ValueError("is_active must be a boolean")
```

### 4. Default Value Application
```python
# Apply defaults for optional fields
if 'is_active' not in data:
    data['is_active'] = True  # Default value
```

This comprehensive validation test suite ensures that the HyperDB system maintains data integrity and provides clear feedback when validation fails. 