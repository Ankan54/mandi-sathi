import sqlite3
import os
from pathlib import Path

class DatabaseManager:
    """Manages SQLite database connections and initialization"""
    
    def __init__(self, db_path="mandi_saathi.db"):
        self.db_path = db_path
        self.initialize_database()
    
    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        """Initialize database with schema"""
        schema_path = Path(__file__).parent / "schema.sql"
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        conn = self.get_connection()
        try:
            conn.executescript(schema_sql)
            conn.commit()
        finally:
            conn.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.fetchall()
        finally:
            conn.close()
    
    def execute_insert(self, query, params):
        """Execute an insert query and return last row id"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
