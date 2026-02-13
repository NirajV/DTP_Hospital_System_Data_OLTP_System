"""
Database Connection Module for Hospital OLTP System
Handles MySQL database connections and basic operations
"""

import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '12345678'
}

DATABASE_NAME = 'hospital_OLTP_system'


class DatabaseConnection:
    """Database connection manager with context manager support"""
    
    def __init__(self, use_database=True):
        self.connection = None
        self.cursor = None
        self.use_database = use_database
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        return False
    
    def connect(self):
        """Establish database connection"""
        try:
            config = DB_CONFIG.copy()
            if self.use_database:
                config['database'] = DATABASE_NAME
            
            self.connection = mysql.connector.connect(**config)
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                db_info = self.connection.get_server_info()
                logger.info(f"Successfully connected to MySQL Server version {db_info}")
                return True
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query that doesn't return results (INSERT, UPDATE, DELETE)"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            logger.info(f"Query executed successfully: {self.cursor.rowcount} rows affected")
            return True
        except Error as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()
            return False
    
    def execute_select(self, query, params=None):
        """Execute a SELECT query and return results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Error as e:
            logger.error(f"Error executing SELECT query: {e}")
            return None
    
    def execute_many(self, query, data_list):
        """Execute multiple queries with different parameters"""
        try:
            self.cursor.executemany(query, data_list)
            self.connection.commit()
            logger.info(f"Batch executed successfully: {self.cursor.rowcount} rows affected")
            return True
        except Error as e:
            logger.error(f"Error executing batch query: {e}")
            self.connection.rollback()
            return False


def test_connection():
    """Test database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"Connected to database: {record}")
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return False


if __name__ == "__main__":
    # Test the connection
    test_connection()
