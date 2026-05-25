from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# DATABASE

def init_db():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        faculty TEXT,
        course TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# HOME

@app.route("/")
def home():
    return render_template("index.html")

# LOGIN

@app.route("/login")
def login():
    return render_template("login.html")

# ADMIN

@app.route("/admin")
def admin():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template("admin.html", students=students)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
