import sqlite3

conn = sqlite3.connect("backend/database.db")
cursor = conn.cursor()

print("Contracts:")
for row in cursor.execute("SELECT id, file_name FROM contracts"):
    print(row)

print("\nSLA Extractions:")
for row in cursor.execute("SELECT id, contract_id FROM sla_extractions"):
    print(row)

conn.close()