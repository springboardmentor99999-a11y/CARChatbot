from backend.db import reset_contracts_table, reset_sla_table

reset_contracts_table()
reset_sla_table()

print("✅ Database tables reset and initialized successfully")
