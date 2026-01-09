import sqlite3
import os
<<<<<<< HEAD
=======
import json
>>>>>>> df82d99 (3rd Milestone is Completed)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

<<<<<<< HEAD
def get_connection():
    return sqlite3.connect(DB_PATH)

=======

# ---------------- CONNECTION ---------------- #

def get_connection():
    return sqlite3.connect(DB_PATH)


# ---------------- CONTRACT TABLE ---------------- #

>>>>>>> df82d99 (3rd Milestone is Completed)
def create_contracts_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
<<<<<<< HEAD
            raw_text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_contract(file_name: str, raw_text: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contracts (file_name, raw_text) VALUES (?, ?)",
        (file_name, raw_text)
    )
    conn.commit()
    conn.close()


def create_sla_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sla_extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER,
            sla_json TEXT NOT NULL,
=======
            raw_text TEXT NOT NULL,
>>>>>>> df82d99 (3rd Milestone is Completed)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


<<<<<<< HEAD
def save_sla(contract_id: int, sla_json: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sla_extractions (contract_id, sla_json) VALUES (?, ?)",
        (contract_id, sla_json)
    )
    conn.commit()
    conn.close()
=======
def save_contract(file_name: str, raw_text: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contracts (file_name, raw_text) VALUES (?, ?)",
        (file_name, raw_text)
    )
    contract_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return contract_id


# ---------------- SLA TABLE ---------------- #

>>>>>>> df82d99 (3rd Milestone is Completed)
def create_sla_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sla_extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
<<<<<<< HEAD
            contract_id INTEGER,
            sla_json TEXT,
=======
            contract_id INTEGER NOT NULL,
            sla_json TEXT NOT NULL,
>>>>>>> df82d99 (3rd Milestone is Completed)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (contract_id) REFERENCES contracts(id)
        )
    """)
    conn.commit()
    conn.close()


<<<<<<< HEAD
def save_sla(contract_id: int, sla_json: str):
=======
def save_sla(contract_id: int, sla_data: dict):
>>>>>>> df82d99 (3rd Milestone is Completed)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sla_extractions (contract_id, sla_json) VALUES (?, ?)",
<<<<<<< HEAD
        (contract_id, sla_json)
    )
    conn.commit()
    conn.close()

def create_sla_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sla_extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER,
            sla_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
=======
        (contract_id, json.dumps(sla_data))
    )
    conn.commit()
>>>>>>> df82d99 (3rd Milestone is Completed)
    conn.close()