import sqlite3
import os

# Ensuring the directory exists prevents "OperationalError: unable to open database file"
DB_DIR = "backend"
DB_PATH = os.path.join(DB_DIR, "database.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_contracts_table():
    # Using 'with' automatically closes the connection even if an error occurs
    with get_connection() as conn:
        cursor = conn.cursor()
        # Fixed syntax: Corrected AUTOINCREMENT placement and added missing commas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                file_name TEXT, 
                raw_text TEXT, 
                uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_contract(file_name: str, raw_text: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contracts (file_name, raw_text) VALUES (?, ?)", 
            (file_name, raw_text)
        )
        conn.commit()