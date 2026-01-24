#!/usr/bin/env python3
"""
Command line utility to view database contents.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def view_database():
    """View all data in the database."""
    if not os.path.exists(DB_PATH):
        print("Database not found. Run init_db.py first.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 50)
    print("CONTRACTS TABLE")
    print("=" * 50)
    for row in cursor.execute("SELECT id, file_name, created_at FROM contracts"):
        print(f"  ID: {row[0]}, File: {row[1]}, Date: {row[2]}")

    print("\n" + "=" * 50)
    print("SLA EXTRACTIONS TABLE")
    print("=" * 50)
    for row in cursor.execute("SELECT id, contract_id, created_at FROM sla_extractions"):
        print(f"  ID: {row[0]}, Contract ID: {row[1]}, Date: {row[2]}")

    conn.close()

if __name__ == "__main__":
    view_database()