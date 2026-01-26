# database.py

import sqlite3
from config import settings
import json
from typing import List, Dict, Any


def get_connection():
    conn = sqlite3.connect(settings.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            raw_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sla_extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            sla_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (contract_id) REFERENCES contracts(id)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sla_contract_id
        ON sla_extractions(contract_id)
    """)

    conn.commit()
    conn.close()


def save_contract(file_name: str, raw_text: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contracts (file_name, raw_text) VALUES (?, ?)",
        (file_name, raw_text)
    )
    contract_id = cur.lastrowid
    conn.commit()
    conn.close()
    return contract_id


def save_sla(contract_id: int, sla_data: dict):
    conn = get_connection()
    conn.execute(
        "INSERT INTO sla_extractions (contract_id, sla_json) VALUES (?, ?)",
        (contract_id, json.dumps(sla_data))
    )
    conn.commit()
    conn.close()


def get_all_contracts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, file_name, created_at
        FROM contracts
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]


def get_contracts_with_sla(contract_ids: list[int]):
    conn = get_connection()
    cur = conn.cursor()

    placeholders = ",".join(["?"] * len(contract_ids))

    query = f"""
        SELECT 
            c.id,
            c.file_name,
            c.created_at,
            s.sla_json
        FROM contracts c
        LEFT JOIN sla_extractions s
            ON c.id = s.contract_id
        WHERE c.id IN ({placeholders})
        ORDER BY c.created_at DESC
    """

    cur.execute(query, contract_ids)
    rows = cur.fetchall()
    conn.close()

    results = []

    for r in rows:
        obj = dict(r)

        if obj["sla_json"]:
            parsed = json.loads(obj["sla_json"])

            obj["sla"] = parsed.get("sla", {})
            obj["fairness"] = parsed.get("fairness", {})
        else:
            obj["sla"] = {}
            obj["fairness"] = {}

        del obj["sla_json"]

        results.append(obj)

    return results
