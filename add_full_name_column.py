import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "database", "library.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE users
    ADD COLUMN full_name TEXT
    """)

    conn.commit()
    print("full_name column added successfully.")

except Exception as e:
    print("Error:", e)

conn.close()