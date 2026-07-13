import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database/library.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Delete the old table if it exists
cursor.execute("DROP TABLE IF EXISTS returned_books")

# Create a new table
cursor.execute("""
CREATE TABLE returned_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    book_title TEXT NOT NULL,
    return_date TEXT NOT NULL
)
""")

cursor.execute("PRAGMA table_info(returned_books)")

for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()

print("returned_books table created successfully!")