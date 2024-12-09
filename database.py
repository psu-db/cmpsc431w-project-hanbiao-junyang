import mysql.connector
from mysql.connector import Error
import sys

# Database connection 
DB_CONFIG = {
    'host': 'localhost',
    'user': 'project_user',
    'password': '1234',
    'database': '431project'
}

def connect_db():
    """Establish connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)