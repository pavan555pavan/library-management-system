import sqlite3

conn = sqlite3.connect("database/library.db")
cursor = conn.cursor()

# Admin Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
#users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
name TEXT
);
""")
# Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    total_count INTEGER NOT NULL,
    
)
""")

# Students Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    department TEXT,
    email TEXT
)
""")

# Issued Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    book_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(book_id) REFERENCES books(id)
)
""")

# Returned Books Table
# Returned Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS returned_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    book_title TEXT NOT NULL,
    return_date TEXT NOT NULL
)
""")

# Search History Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history (
    search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    search_date TEXT
)
""")

conn.commit()
conn.close()

print("All tables created successfully!")