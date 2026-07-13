from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "library123"

# -----------------------------
# Database Connection
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database/library.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ===================================================
# ADMIN REGISTER
# ===================================================
@app.route("/admin-register", methods=["GET", "POST"])
def admin_register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO admin(username,password) VALUES(?,?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/admin-login")

    return render_template("admin_register.html")


# ===================================================
# ADMIN LOGIN
# ===================================================
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username, password)
        )

        admin = cursor.fetchone()

        conn.close()

        if admin:
            session["admin"] = username
            return redirect("/admin-dashboard")
        else:
            return "Invalid Username or Password"

    return render_template("admin_login.html")
# ===================================================
# USER REGISTER
# ===================================================
@app.route("/user-register", methods=["GET", "POST"])
def user_register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(full_name,username,password)
            VALUES(?,?,?)
            """,
            (fullname, username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/user-login")

    return render_template("user_register.html")


# ===================================================
# USER LOGIN
# ===================================================
@app.route("/user-login", methods=["GET", "POST"])
def user_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user"] = username

            return redirect("/user-dashboard")

        else:

            return "Invalid Username or Password"

    return render_template("user_login.html")




# ===================================================
# LOGOUT
# ===================================================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
#====================================================
#add book
@app.route("/add-book", methods=["GET", "POST"])
def add_book():

    if "admin" not in session:
        return redirect("/admin-login")

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        total_count = int(request.form["total_count"])

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO books
            (title, author, category, total_count, available_count)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, category, total_count, total_count))

        conn.commit()
        conn.close()

        return redirect(url_for("view_books"))

    return render_template("admin/add_book.html")
#====================================================
# ---------------- ADMIN VIEW BOOKS ----------------

@app.route("/view-books")
def view_books():

    if "admin" not in session:
        return redirect("/admin-login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,title,author,category,total_count,available_count
        FROM books
    """)

    books = cursor.fetchall()

    conn.close()

    return render_template("admin/view_books.html", books=books)


# ---------------- USER VIEW BOOKS ----------------

@app.route("/user-view-books")
def user_view_books():

    if "user" not in session:
        return redirect("/user-login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,title,author,category,total_count,available_count
        FROM books
    """)

    books = cursor.fetchall()

    conn.close()

    return render_template("user/view_books.html", books=books)
#====================================================
#search book
@app.route("/search-book", methods=["GET", "POST"])
def search_book():

    if "admin" not in session and "user" not in session:
        return redirect("/")

    if request.method == "POST":

        keyword = request.form["keyword"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
        """, ('%' + keyword + '%',
              '%' + keyword + '%',
              '%' + keyword + '%'))

        books = cursor.fetchall()
        conn.close()

        if "admin" in session:
            return render_template("admin/search_result1.html", books=books)
        else:
            return render_template("user/search_result.html", books=books)

    if "admin" in session:
        return render_template("admin/search_book.html")
    else:
        return render_template("user/search_book.html")
#====================================================
#issue book
@app.route("/issue-book", methods=["GET", "POST"])
def issue_book():

    if "user" not in session:
        return redirect("/user-login")

    if request.method == "POST":

        student_name = session["user"]
        book_title = request.form["book_title"]
        issue_date = request.form["issue_date"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT available_count
        FROM books
        WHERE title=?
        """, (book_title,))

        book = cursor.fetchone()

        if not book:
            conn.close()
            return "Book not found."

        if book["available_count"] <= 0:
            conn.close()
            return "Book is not available."

        cursor.execute("""
        INSERT INTO issued_books
        (student_name, book_title, issue_date)
        VALUES (?, ?, ?)
        """, (student_name, book_title, issue_date))

        cursor.execute("""
        UPDATE books
        SET available_count = available_count - 1
        WHERE title=?
        """, (book_title,))

        conn.commit()
        conn.close()

        return render_template("issue_success.html")

    return render_template("user/issue_book.html")
#====================================================
#return book
@app.route("/return-book", methods=["GET", "POST"])
def return_book():

    if "user" not in session:
        return redirect("/user-login")

    if request.method == "POST":

        student_name = request.form["student_name"]
        book_title = request.form["book_title"]
        return_date = request.form["return_date"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO returned_books
        (student_name, book_title, return_date)
        VALUES (?, ?, ?)
        """, (student_name, book_title, return_date))

        cursor.execute("""
        UPDATE books
        SET available_count = available_count + 1
        WHERE title=?
          AND available_count < total_count
        """, (book_title,))

        conn.commit()
        conn.close()

        return render_template("return_success.html")

    return render_template("user/return_book.html")
#====================================================
# ===================================================
# VIEW ISSUED BOOKS
# ===================================================
@app.route("/view-issued-books")
def view_issued_books():

    if "admin" not in session:
        return redirect("/admin-login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM issued_books")

    books = cursor.fetchall()

    conn.close()

   
    return render_template("admin/view_issued_books.html", books=books)
# ===================================================
# VIEW RETURNED BOOKS
# ===================================================
@app.route("/view-returned-books")
def view_returned_books():

    if "admin" not in session:
        return redirect("/admin-login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM returned_books")

    books = cursor.fetchall()

    conn.close()

    
    return render_template("admin/view_returned_books.html", books=books)
# ===================================================
# ADMIN DASHBOARD
# ===================================================
@app.route("/admin-dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin-login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(available_count) FROM books")
    available_books = cursor.fetchone()[0]

    if available_books is None:
        available_books = 0

    cursor.execute("SELECT COUNT(*) FROM issued_books")
    issued_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM returned_books")
    returned_books = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books,
        returned_books=returned_books
    )
# ===================================================
# USER DASHBOARD
# ===================================================
@app.route("/user-dashboard")
def user_dashboard():

    if "user" not in session:
        return redirect("/user-login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(available_count) FROM books")
    available_books = cursor.fetchone()[0]

    if available_books is None:
        available_books = 0

    conn.close()
    return render_template(
    "user_dashboard.html",
    available_books=available_books
)
# ===================================================
# DELETE BOOK
# ===================================================
@app.route("/delete-book/<int:id>")
def delete_book(id):

    if "admin" not in session:
        return redirect("/admin-login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/view-books")
# ===================================================

# =====================================
# MY ISSUED BOOKS (User)
# =====================================
@app.route("/my-issued-books")
def my_issued_books():

    if "user" not in session:
        return redirect("/user-login")

    username = session["user"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM issued_books
        WHERE student_name = ?
    """, (username,))

    books = cursor.fetchall()

    conn.close()

    return render_template(
        "user/my_issued_books.html",
        books=books
    )
# ===================================================
# RUN APP
# ===================================================
if __name__ == "__main__":
    app.run(debug=True)