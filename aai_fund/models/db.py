# models/db.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Update credentials below as needed.
    For production use environment variables or a secret manager.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="120623104",
            database="aai_funds"
        )
        return conn
    except Error as e:
        raise RuntimeError(f"Database connection error: {e}")
