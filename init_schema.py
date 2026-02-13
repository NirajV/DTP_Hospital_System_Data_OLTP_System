#!/usr/bin/env python3
"""
Initialize Database Schema
Executes create_schema.sql to create all 52 tables with FK management
"""

import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Connection config
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'database': 'hospital_OLTP_system'
}

def execute_schema_file(sql_file_path):
    """Execute SQL schema file"""
    try:
        # Read schema file
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Connect to MySQL
        connection = mysql.connector.connect(**{k: v for k, v in config.items() if k != 'database'})
        cursor = connection.cursor()
        
        # Execute script
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    connection.commit()
                except Error as e:
                    if 'already exists' not in str(e):
                        logger.error(f"Error: {e}")
        
        cursor.close()
        connection.close()
        logger.info("[SUCCESS] Database schema initialized successfully!")
        return True
        
    except FileNotFoundError:
        logger.error(f"File not found: {sql_file_path}")
        return False
    except Error as e:
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == '__main__':
    sql_file = 'create_schema.sql'
    logger.info(f"Initializing schema from {sql_file}...")
    execute_schema_file(sql_file)
