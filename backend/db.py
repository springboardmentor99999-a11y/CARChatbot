import sqlite3

DB_PATH = "backend/database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_contracts_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            raw_text TEXT,
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_contract(file_name: str, raw_text: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contracts (file_name, raw_text)
        VALUES (?, ?)
    """, (file_name, raw_text))

    conn.commit()
    conn.close()