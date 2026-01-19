import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def save_contract(file_name: str, contract_text: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contracts (file_name, contract_text) VALUES (?, ?)",
        (file_name, contract_text)
    )

    contract_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return contract_id


def save_sla(contract_id: int, sla_data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE contracts SET extracted_json = ? WHERE id = ?",
        (json.dumps(sla_data), contract_id)
    )

    conn.commit()
    conn.close()
