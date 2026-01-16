
# backend/db.py
import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


# ---------------- CONNECTION ---------------- #

def get_connection():
    return sqlite3.connect(DB_PATH)


# ---------------- CONTRACT TABLE ---------------- #

def create_contracts_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            raw_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


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


def get_contract_text(contract_id: int) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT raw_text FROM contracts WHERE id = ?",
        (contract_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


# ---------------- SLA TABLE ---------------- #

def create_sla_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sla_extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            sla_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (contract_id) REFERENCES contracts(id)
        )
    """)
    conn.commit()
    conn.close()


def save_sla(contract_id: int, sla_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sla_extractions (contract_id, sla_json) VALUES (?, ?)",
        (contract_id, json.dumps(sla_data))
    )
    conn.commit()
    conn.close()