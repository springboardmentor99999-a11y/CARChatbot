#!/usr/bin/env python3
"""
Initialize the database for Car Loan Assistant.
Run this script once to create the necessary tables.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import create_contracts_table, create_sla_table

def init_database():
    """Create all required database tables."""
    print("Initializing database...")
    create_contracts_table()
    print("  ✓ Contracts table created")
    create_sla_table()
    print("  ✓ SLA extractions table created")
    print("\nDatabase initialized successfully!")

if __name__ == "__main__":
    init_database()
