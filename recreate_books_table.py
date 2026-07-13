import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "database", "library.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Delete old books table
cursor.execute("DROP TABLE IF EXISTS books")

# Create new books table
cursor.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    total_count INTEGER NOT NULL,
    available_count INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Books table recreated successfully!")