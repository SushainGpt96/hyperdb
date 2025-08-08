import json
import sqlite3
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from blockchain import Blockchain, Block


@dataclass
class DataField:
    """Represents a data field in the schema"""
    name: str
    type: str  # 'text', 'integer', 'real', 'boolean', 'datetime', 'json'
    required: bool = True
    default: Any = None
    description: str = ""


@dataclass
class DataModel:
    """Represents a data model/schema"""
    name: str
    fields: List[DataField]
    description: str = ""
    created_at: float = None
    version: str = "1.0"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for blockchain storage"""
        return {
            'name': self.name,
            'fields': [asdict(field) for field in self.fields],
            'description': self.description,
            'created_at': self.created_at,
            'version': self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataModel':
        """Create from dictionary"""
        fields = [DataField(**field_data) for field_data in data['fields']]
        return cls(
            name=data['name'],
            fields=fields,
            description=data.get('description', ''),
            created_at=data.get('created_at'),
            version=data.get('version', '1.0')
        )


class HyperledgerIntegratedDB:
    """Database system with integrated blockchain storage, inspired by Hyperledger Fabric"""
    
    def __init__(self, db_path: str = "hyperledger_integrated.db", blockchain_difficulty: int = 2):
        self.db_path = db_path
        self.connection = None
        self.blockchain = Blockchain(difficulty=blockchain_difficulty)
        self.data_models: Dict[str, DataModel] = {}
        self.setup_database()
        self._load_existing_data()
    
    def setup_database(self) -> None:
        """Create database tables"""
        self.connect()
        cursor = self.connection.cursor()
        
        # Create data models table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_models (
                name TEXT PRIMARY KEY,
                schema_data TEXT NOT NULL,
                created_at REAL NOT NULL,
                version TEXT NOT NULL
            )
        ''')
        
        # Create data records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_records (
                id TEXT PRIMARY KEY,
                model_name TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                blockchain_transaction_id TEXT,
                blockchain_block_index INTEGER,
                FOREIGN KEY (model_name) REFERENCES data_models (name)
            )
        ''')
        
        # Create blockchain transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blockchain_transactions (
                id TEXT PRIMARY KEY,
                transaction_type TEXT NOT NULL,
                data_id TEXT,
                model_name TEXT,
                transaction_data TEXT NOT NULL,
                timestamp REAL NOT NULL,
                block_index INTEGER,
                FOREIGN KEY (data_id) REFERENCES data_records (id)
            )
        ''')
        
        # Create blockchain blocks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blockchain_blocks (
                block_index INTEGER PRIMARY KEY,
                hash TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                timestamp REAL NOT NULL,
                nonce INTEGER NOT NULL,
                transactions_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.connection.commit()
    
    def connect(self) -> None:
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
    
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def _load_existing_data(self) -> None:
        """Load existing data models and blockchain data"""
        try:
            # Load data models
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM data_models')
            for row in cursor.fetchall():
                schema_data = json.loads(row['schema_data'])
                self.data_models[row['name']] = DataModel.from_dict(schema_data)
            
            # Load blockchain data
            cursor.execute('SELECT * FROM blockchain_blocks ORDER BY block_index')
            for row in cursor.fetchall():
                transactions = json.loads(row['transactions_data']) if row['transactions_data'] else []
                block = Block(
                    index=row['block_index'],
                    transactions=transactions,
                    timestamp=row['timestamp'],
                    previous_hash=row['previous_hash'],
                    nonce=row['nonce']
                )
                block.hash = row['hash']
                self.blockchain.chain.append(block)
            
            print(f"Loaded {len(self.data_models)} data models and {len(self.blockchain.chain)} blockchain blocks")
        except Exception as e:
            print(f"Error loading existing data: {e}")
    
    def create_data_model(self, name: str, fields: List[Dict[str, Any]], description: str = "") -> bool:
        """Create a new data model/schema"""
        try:
            # Convert field dictionaries to DataField objects
            data_fields = []
            for field_data in fields:
                data_fields.append(DataField(
                    name=field_data['name'],
                    type=field_data['type'],
                    required=field_data.get('required', True),
                    default=field_data.get('default'),
                    description=field_data.get('description', '')
                ))
            
            # Create data model
            data_model = DataModel(
                name=name,
                fields=data_fields,
                description=description
            )
            
            # Save to database
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO data_models (name, schema_data, created_at, version)
                VALUES (?, ?, ?, ?)
            ''', (
                name,
                json.dumps(data_model.to_dict()),
                data_model.created_at,
                data_model.version
            ))
            
            # Store in memory
            self.data_models[name] = data_model
            
            # Add to blockchain
            self._add_to_blockchain(
                transaction_type="model_creation",
                data={
                    'model_name': name,
                    'schema': data_model.to_dict(),
                    'description': description
                }
            )
            
            self.connection.commit()
            print(f"Data model '{name}' created successfully")
            return True
            
        except Exception as e:
            print(f"Error creating data model: {e}")
            return False
    
    def add_data(self, model_name: str, data: Dict[str, Any]) -> Optional[str]:
        """Add data to a specific model"""
        try:
            if model_name not in self.data_models:
                raise ValueError(f"Data model '{model_name}' does not exist")
            
            data_model = self.data_models[model_name]
            
            # Validate data against schema
            self._validate_data(data, data_model)
            
            # Generate unique ID
            record_id = str(uuid.uuid4())
            current_time = time.time()
            
            # Save to database
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO data_records (id, model_name, data, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                record_id,
                model_name,
                json.dumps(data),
                current_time,
                current_time
            ))
            
            # Add to blockchain
            transaction_id = self._add_to_blockchain(
                transaction_type="data_creation",
                data={
                    'record_id': record_id,
                    'model_name': model_name,
                    'data': data,
                    'created_at': current_time
                }
            )
            
            # Update record with blockchain info
            cursor.execute('''
                UPDATE data_records 
                SET blockchain_transaction_id = ?
                WHERE id = ?
            ''', (transaction_id, record_id))
            
            self.connection.commit()
            print(f"Data added to model '{model_name}' with ID: {record_id}")
            return record_id
            
        except Exception as e:
            print(f"Error adding data: {e}")
            return None
    
    def update_data(self, record_id: str, data: Dict[str, Any]) -> bool:
        """Update existing data"""
        try:
            # Get current record
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM data_records WHERE id = ?', (record_id,))
            row = cursor.fetchone()
            
            if not row:
                raise ValueError(f"Record with ID '{record_id}' not found")
            
            current_data = json.loads(row['data'])
            model_name = row['model_name']
            
            # Validate updated data
            if model_name in self.data_models:
                self._validate_data(data, self.data_models[model_name])
            
            # Update database
            current_time = time.time()
            cursor.execute('''
                UPDATE data_records 
                SET data = ?, updated_at = ?
                WHERE id = ?
            ''', (
                json.dumps(data),
                current_time,
                record_id
            ))
            
            # Add to blockchain
            self._add_to_blockchain(
                transaction_type="data_update",
                data={
                    'record_id': record_id,
                    'model_name': model_name,
                    'previous_data': current_data,
                    'new_data': data,
                    'updated_at': current_time
                }
            )
            
            self.connection.commit()
            print(f"Data updated for record: {record_id}")
            return True
            
        except Exception as e:
            print(f"Error updating data: {e}")
            return False
    
    def get_data(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Get data by record ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM data_records WHERE id = ?', (record_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row['id'],
                    'model_name': row['model_name'],
                    'data': json.loads(row['data']),
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'blockchain_transaction_id': row['blockchain_transaction_id'],
                    'blockchain_block_index': row['blockchain_block_index']
                }
            return None
            
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return None
    
    def get_all_data(self, model_name: str = None) -> List[Dict[str, Any]]:
        """Get all data records, optionally filtered by model"""
        try:
            cursor = self.connection.cursor()
            
            if model_name:
                cursor.execute('SELECT * FROM data_records WHERE model_name = ? ORDER BY created_at', (model_name,))
            else:
                cursor.execute('SELECT * FROM data_records ORDER BY created_at')
            
            records = []
            for row in cursor.fetchall():
                records.append({
                    'id': row['id'],
                    'model_name': row['model_name'],
                    'data': json.loads(row['data']),
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'blockchain_transaction_id': row['blockchain_transaction_id'],
                    'blockchain_block_index': row['blockchain_block_index']
                })
            
            return records
            
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return []
    
    def get_data_models(self) -> List[Dict[str, Any]]:
        """Get all data models"""
        return [model.to_dict() for model in self.data_models.values()]
    
    def _validate_data(self, data: Dict[str, Any], model: DataModel) -> None:
        """Validate data against the model schema"""
        for field in model.fields:
            if field.required and field.name not in data:
                raise ValueError(f"Required field '{field.name}' is missing")
            
            # Apply default value if field is missing and has a default
            if field.name not in data and field.default is not None:
                data[field.name] = field.default
            
            if field.name in data:
                value = data[field.name]
                
                # Type validation
                if field.type == 'text' and not isinstance(value, str):
                    raise ValueError(f"Field '{field.name}' must be a string")
                elif field.type == 'integer' and not isinstance(value, int):
                    raise ValueError(f"Field '{field.name}' must be an integer")
                elif field.type == 'real' and not isinstance(value, (int, float)):
                    raise ValueError(f"Field '{field.name}' must be a number")
                elif field.type == 'boolean' and not isinstance(value, bool):
                    raise ValueError(f"Field '{field.name}' must be a boolean")
                elif field.type == 'datetime':
                    # Accept timestamp or datetime string
                    if not isinstance(value, (int, float, str)):
                        raise ValueError(f"Field '{field.name}' must be a datetime")
                elif field.type == 'json' and not isinstance(value, (dict, list)):
                    raise ValueError(f"Field '{field.name}' must be a JSON object or array")
    
    def _add_to_blockchain(self, transaction_type: str, data: Dict[str, Any]) -> str:
        """Add transaction to blockchain"""
        transaction_id = str(uuid.uuid4())
        current_time = time.time()
        
        # Create blockchain transaction
        transaction = {
            'id': transaction_id,
            'type': transaction_type,
            'data': data,
            'timestamp': current_time,
            'sender': 'system',
            'recipient': 'system',
            'amount': 0.0
        }
        
        # Add to blockchain pending transactions
        self.blockchain.add_transaction(
            sender='system',
            recipient='system',
            amount=0.0,
            data=transaction
        )
        
        # Save to database
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO blockchain_transactions (id, transaction_type, data_id, model_name, transaction_data, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            transaction_id,
            transaction_type,
            data.get('record_id'),
            data.get('model_name'),
            json.dumps(transaction),
            current_time
        ))
        
        return transaction_id
    
    def mine_block(self) -> Optional[Dict[str, Any]]:
        """Mine a new block with pending transactions"""
        try:
            if not self.blockchain.pending_transactions:
                print("No pending transactions to mine")
                return None
            
            # Mine the block
            block = self.blockchain.mine_pending_transactions("system")
            
            # Save block to database
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO blockchain_blocks (block_index, hash, previous_hash, timestamp, nonce, transactions_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                block.index,
                block.hash,
                block.previous_hash,
                block.timestamp,
                block.nonce,
                json.dumps(block.transactions)
            ))
            
            # Update transaction block indices
            for transaction in block.transactions:
                if transaction.get('id'):
                    cursor.execute('''
                        UPDATE blockchain_transactions 
                        SET block_index = ?
                        WHERE id = ?
                    ''', (block.index, transaction['id']))
                    
                    # Also update data records
                    if transaction.get('data', {}).get('record_id'):
                        cursor.execute('''
                            UPDATE data_records 
                            SET blockchain_block_index = ?
                            WHERE id = ?
                        ''', (block.index, transaction['data']['record_id']))
            
            self.connection.commit()
            
            print(f"Block {block.index} mined successfully with {len(block.transactions)} transactions")
            return {
                'index': block.index,
                'hash': block.hash,
                'timestamp': block.timestamp,
                'transaction_count': len(block.transactions)
            }
            
        except Exception as e:
            print(f"Error mining block: {e}")
            return None
    
    def get_blockchain_info(self) -> Dict[str, Any]:
        """Get blockchain information"""
        return {
            'chain_length': len(self.blockchain.chain),
            'pending_transactions': len(self.blockchain.pending_transactions),
            'difficulty': self.blockchain.difficulty,
            'is_valid': self.blockchain.is_chain_valid(),
            'latest_block': {
                'index': self.blockchain.get_latest_block().index,
                'hash': self.blockchain.get_latest_block().hash,
                'timestamp': self.blockchain.get_latest_block().timestamp
            } if self.blockchain.chain else None
        }
    
    def search_data(self, model_name: str = None, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search data records based on criteria"""
        all_data = self.get_all_data(model_name)
        
        if not criteria:
            return all_data
        
        results = []
        for record in all_data:
            match = True
            record_data = record['data']
            
            for key, value in criteria.items():
                if key not in record_data:
                    match = False
                    break
                
                if isinstance(value, str) and isinstance(record_data[key], str):
                    if value.lower() not in record_data[key].lower():
                        match = False
                        break
                elif record_data[key] != value:
                    match = False
                    break
            
            if match:
                results.append(record)
        
        return results
    
    def export_data(self, filepath: str) -> bool:
        """Export all data to JSON file"""
        try:
            data = {
                'data_models': self.get_data_models(),
                'data_records': self.get_all_data(),
                'blockchain_info': self.get_blockchain_info(),
                'blockchain_blocks': []
            }
            
            # Get blockchain blocks
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM blockchain_blocks ORDER BY block_index')
            for row in cursor.fetchall():
                data['blockchain_blocks'].append(dict(row))
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"Data exported to {filepath}")
            return True
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False 