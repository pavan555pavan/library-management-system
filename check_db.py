import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "database", "library.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(books)")
print("Books table columns:")

for row in cursor.fetchall():
    print(row)

conn.close()