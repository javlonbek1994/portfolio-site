from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "muzeylab_secret_key"

DB_NAME = "database.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade TEXT NOT NULL,
            direction TEXT NOT NULL,
            works INTEGER DEFAULT 0,
            score INTEGER DEFAULT 80,
            image TEXT,
            description TEXT
        )
    """)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if count == 0:
        conn.execute("""
            INSERT INTO students (name, grade, direction, works, score, image, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "Aliyev Muhammad",
            "Tarix yo‘nalishi",
            "Pedagogik portfel",
            12,
            90,
            "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=80",
            "Tarixiy tafakkur va muzey pedagogikasi bo‘yicha faol talaba."
        ))

        conn.execute("""
            INSERT INTO students (name, grade, direction, works, score, image, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "Karimova Madina",
            "Tarix yo‘nalishi",
            "Akademik yutuqlar",
            9,
            86,
            "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=900&q=80",
            "Madaniy meros va tarixiy manbalar bilan ishlash bo‘yicha portfolio yuritadi."
        ))

        conn.commit()

    conn.close()


@app.before_request
def before_request():
    init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/portfolio")
def portfolio():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("portfolio.html", students=students)


@app.route("/student")
def student_list():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("portfolio.html", students=students)


@app.route("/student/<int:student_id>")
def student_detail(student_id):
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()

    if student is None:
        return "Talaba topilmadi", 404

    return render_template("student.html", student=student)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "12345":
            session["admin"] = True
            return redirect("/admin")

        error = "Login yoki parol noto‘g‘ri"

    return render_template("login.html", error=error)


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_works = conn.execute("SELECT COALESCE(SUM(works), 0) FROM students").fetchone()[0]
    avg = conn.execute("SELECT COALESCE(ROUND(AVG(score)), 0) FROM students").fetchone()[0]
    conn.close()

    return render_template(
        "admin.html",
        students=students,
        total_students=total_students,
        total_works=total_works,
        active=total_students,
        avg=avg
    )


@app.route("/admin/add", methods=["POST"])
def admin_add():
    if not session.get("admin"):
        return redirect("/login")

    name = request.form.get("name")
    grade = request.form.get("grade")
    direction = request.form.get("direction")
    works = request.form.get("works", 0)
    score = request.form.get("score", 80)
    image = request.form.get("image")
    description = request.form.get("description")

    if not image:
        image = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=80"

    if not description:
        description = "Talabaning pedagogik portfeli va o‘quv faoliyati haqida ma’lumot."

    conn = get_db()
    conn.execute("""
        INSERT INTO students (name, grade, direction, works, score, image, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        grade,
        direction,
        int(works),
        int(score),
        image,
        description
    ))
    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/admin/delete/<int:student_id>", methods=["POST"])
def admin_delete(student_id):
    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/logout")
@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
