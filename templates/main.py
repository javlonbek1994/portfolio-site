from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "muzeylab_secret_key"

students = [
    {
        "id": 1,
        "name": "Aliyev Muhammad",
        "grade": "Tarix yo‘nalishi",
        "direction": "Pedagogik portfel",
        "works": 12,
        "score": 90,
        "image": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=80",
        "description": "Tarixiy tafakkur va muzey pedagogikasi bo‘yicha faol talaba."
    },
    {
        "id": 2,
        "name": "Karimova Madina",
        "grade": "Tarix yo‘nalishi",
        "direction": "Akademik yutuqlar",
        "works": 9,
        "score": 86,
        "image": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=900&q=80",
        "description": "Madaniy meros va tarixiy manbalar bilan ishlash bo‘yicha portfolio yuritadi."
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", students=students)


@app.route("/student")
def student_list():
    return render_template("portfolio.html", students=students)


@app.route("/student/<int:student_id>")
def student_detail(student_id):
    student = None

    for s in students:
        if s["id"] == student_id:
            student = s
            break

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
        else:
            error = "Login yoki parol noto‘g‘ri"

    return render_template("login.html", error=error)


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    total_students = len(students)
    total_works = sum(int(s["works"]) for s in students)

    if total_students > 0:
        avg = round(sum(int(s["score"]) for s in students) / total_students)
    else:
        avg = 0

    active = total_students

    return render_template(
        "admin.html",
        students=students,
        total_students=total_students,
        total_works=total_works,
        active=active,
        avg=avg
    )


@app.route("/admin/add", methods=["POST"])
def admin_add():
    if not session.get("admin"):
        return redirect("/login")

    new_id = 1
    if students:
        new_id = max(s["id"] for s in students) + 1

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

    students.append({
        "id": new_id,
        "name": name,
        "grade": grade,
        "direction": direction,
        "works": int(works),
        "score": int(score),
        "image": image,
        "description": description
    })

    return redirect("/admin")


@app.route("/admin/delete/<int:student_id>", methods=["POST"])
def admin_delete(student_id):
    if not session.get("admin"):
        return redirect("/login")

    global students
    students = [s for s in students if s["id"] != student_id]

    return redirect("/admin")


@app.route("/logout")
@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
