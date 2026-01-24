from backend.db import create_tables

if __name__ == "__main__":
    print("Initializing database...")
    create_tables()
    print("Database initialized successfully.")
