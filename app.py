from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = "muzeylab_secret_key"

DB_NAME = "database.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
conn = get_db()

```
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

conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT NOT NULL
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS reflections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        reflection_type TEXT NOT NULL,
        text TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS diagnostic_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        total_score INTEGER,
        percent INTEGER,
        level TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()

user_count = conn.execute(
    "SELECT COUNT(*) FROM users"
).fetchone()[0]

if user_count == 0:
    conn.execute("""
        INSERT INTO users
        (username, password, role, full_name)
        VALUES (?, ?, ?, ?)
    """, ("admin", "12345", "admin", "Administrator"))

    conn.execute("""
        INSERT INTO users
        (username, password, role, full_name)
        VALUES (?, ?, ?, ?)
    """, ("teacher", "12345", "teacher", "O‘qituvchi"))

    conn.commit()

conn.close()
```


        conn.execute("""
            INSERT INTO users
            (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        """, ("student", "12345", "student", "Talaba"))

        conn.commit()

    count = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    if count == 0:
        conn.execute("""
            INSERT INTO students
            (name, grade, direction, works, score, image, description)
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
            INSERT INTO students
            (name, grade, direction, works, score, image, description)
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

    return render_template("student_list.html", students=students)


@app.route("/student/<int:student_id>")
def student_detail(student_id):
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()
    conn.close()

    if student is None:
        return "Talaba topilmadi", 404

    return render_template("student.html", student=student)


@app.route("/student-dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect("/login")

    return render_template("student_dashboard.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/museum")
def museum():
    return render_template("museum.html")


@app.route("/achievements")
def achievements():
    return render_template("achievements.html")


@app.route("/reflection", methods=["GET", "POST"])
def reflection():
    score = None

    if request.method == "POST":
        student_name = request.form.get("student_name")
        reflection_type = request.form.get("reflection_type")
        text = request.form.get("text", "")

        reflection_score = 0
        text_lower = text.lower()

        if len(text) >= 300:
            reflection_score += 5

        if "tajriba" in text_lower or "xulosa" in text_lower:
            reflection_score += 5

        if "muammo" in text_lower or "yechim" in text_lower:
            reflection_score += 5

        if "reja" in text_lower or "rivojlanish" in text_lower:
            reflection_score += 5

        conn = get_db()

        conn.execute("""
            INSERT INTO reflections
            (student_name, reflection_type, text, score)
            VALUES (?, ?, ?, ?)
        """, (
            student_name,
            reflection_type,
            text,
            reflection_score
        ))

        conn.commit()
        conn.close()

        score = reflection_score

    return render_template("reflection.html", score=score)


@app.route("/diagnostic")
def diagnostic():
    return render_template("diagnostic.html")


@app.route("/diagnostic/source")
def diagnostic_source():
    return render_template("diagnostic_source.html")


@app.route("/diagnostic/thinking")
def diagnostic_thinking():
    return render_template("diagnostic_thinking.html")


@app.route("/diagnostic/reflection")
def diagnostic_reflection():
    return render_template("diagnostic_reflection.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["full_name"] = user["full_name"]

            if user["role"] == "admin":
                return redirect("/admin")

            if user["role"] == "teacher":
                return redirect("/teacher")

            return redirect("/student-dashboard")

        error = "Login yoki parol noto‘g‘ri"

    return render_template("login.html", error=error)


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_works = conn.execute(
        "SELECT COALESCE(SUM(works), 0) FROM students"
    ).fetchone()[0]

    avg = conn.execute(
        "SELECT COALESCE(ROUND(AVG(score)), 0) FROM students"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        students=students,
        total_students=total_students,
        total_works=total_works,
        active=total_students,
        avg=avg
    )


@app.route("/teacher")
def teacher():
    if session.get("role") != "teacher":
        return redirect("/login")

    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("teacher.html", students=students)

@app.route("/admin/import", methods=["POST"])
def admin_import():
    if session.get("role") != "admin":
        return redirect("/login")

    file = request.files.get("excel_file")

    if not file:
        return redirect("/admin")

    df = pd.read_excel(file)

    conn = get_db()

    for index, row in df.iterrows():
        full_name = str(row.iloc[0]).strip()
        group_name = str(row.iloc[1]).strip()
        direction = str(row.iloc[2]).strip()

        username = f"talaba{index + 1:03d}"
        password = "123456"

        conn.execute("""
            INSERT INTO students
            (name, grade, direction, works, score, image, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            group_name,
            direction,
            0,
            80,
            "",
            f"Login: {username}"
        ))

        conn.execute("""
            INSERT OR IGNORE INTO users
            (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        """, (
            username,
            password,
            "student",
            full_name
        ))

    conn.commit()
    conn.close()

    return redirect("/admin")
    
@app.route("/admin/add", methods=["POST"])
def admin_add():
    if session.get("role") != "admin":
        return redirect("/login")

    name = request.form.get("name")
    grade = request.form.get("grade")
    direction = request.form.get("direction")
    works = request.form.get("works", 0)

    historical = int(request.form.get("historical", 0))
    museum = int(request.form.get("museum", 0))
    reflection = int(request.form.get("reflection", 0))
    portfolio = int(request.form.get("portfolio", 0))

    score = historical + museum + reflection + portfolio

    image = request.form.get("image")
    description = request.form.get("description")

    if not image:
        image = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=80"

    if not description:
        description = "Talabaning pedagogik portfeli va o‘quv faoliyati haqida ma’lumot."

    conn = get_db()

    conn.execute("""
        INSERT INTO students
        (name, grade, direction, works, score, image, description)
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
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

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

    app.run(
        host="0.0.0.0",
        port=port
    )
