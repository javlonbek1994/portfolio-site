from flask import Flask, render_template, request, redirect
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

# ADMIN PANEL

@app.route("/admin", methods=["GET", "POST"])
def admin():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # STUDENT ADD

    if request.method == "POST":

        name = request.form["name"]
        faculty = request.form["faculty"]
        course = request.form["course"]

        cur.execute(
            "INSERT INTO students(name, faculty, course) VALUES(?,?,?)",
            (name, faculty, course)
        )

        conn.commit()

    # GET STUDENTS

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template("admin.html", students=students)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
