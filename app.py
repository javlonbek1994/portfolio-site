from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "muzeylab_super_secret_key"

students = [
    {
        "id": 1,
        "name": "Aliyev Muhammad",
        "grade": "7-sinf",
        "direction": "Pedagogik portfel",
        "status": "Faol",
        "works": 12,
        "score": 94,
        "image": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1000&q=80",
        "description": "O‘quv faoliyati, loyiha ishlari, refleksiya va akademik natijalari jamlangan elektron portfel.",
        "projects": ["Dars ishlanmasi", "Ijodiy loyiha", "Refleksiya kundaligi"]
    },
    {
        "id": 2,
        "name": "Karimova Madina",
        "grade": "8-sinf",
        "direction": "Akademik yutuqlar",
        "status": "Faol",
        "works": 9,
        "score": 88,
        "image": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1000&q=80",
        "description": "Akademik yutuqlar, sertifikatlar, ijodiy ishlar va raqamli artefaktlar portfeli.",
        "projects": ["Sertifikatlar", "Tanlov natijalari", "Taqdimot ishlari"]
    },
    {
        "id": 3,
        "name": "Saidov Javohir",
        "grade": "9-sinf",
        "direction": "Refleksiya",
        "status": "Ko‘rib chiqilmoqda",
        "works": 7,
        "score": 81,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1000&q=80",
        "description": "O‘zini baholash, refleksiya, o‘quv natijalari va kompetensiyalar rivoji bo‘yicha portfel.",
        "projects": ["O‘zini baholash", "Reflektiv esse", "Kompetensiya tahlili"]
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/portfolio")
def portfolio():
    q = request.args.get("q", "").lower().strip()

    if q:
        filtered = [
            s for s in students
            if q in s["name"].lower()
            or q in s["direction"].lower()
            or q in s["grade"].lower()
        ]
    else:
        filtered = students

    return render_template("portfolio.html", students=filtered, q=q)


@app.route("/student/<int:student_id>")
def student(student_id):
    s = next((x for x in students if x["id"] == student_id), None)

    if not s:
        return redirect(url_for("portfolio"))

    return render_template("student.html", s=s)


@app.route("/personal")
def personal():
    return render_template(
        "simple.html",
        title="Shaxsiy ma’lumotlar",
        text="Bu bo‘limda talabaning shaxsiy ma’lumotlari, ta’lim yo‘nalishi va umumiy portfel ma’lumotlari joylashtiriladi."
    )


@app.route("/achievements")
def achievements():
    return render_template(
        "simple.html",
        title="Akademik yutuqlar",
        text="Bu bo‘limda talabaning sertifikatlari, tanlov natijalari, ilmiy va ijodiy yutuqlari jamlanadi."
    )


@app.route("/reflection")
def reflection():
    return render_template(
        "simple.html",
        title="Refleksiya va o‘zini baholash",
        text="Bu bo‘limda talabaning o‘zini baholashi, reflektiv yozuvlari va rivojlanish monitoringi keltiriladi."
    )


@app.route("/about")
def about():
    return render_template(
        "simple.html",
        title="Biz haqimizda",
        text="Muzey Lab platformasi muzey pedagogikasi, raqamli portfolio va tarixiy tafakkurni rivojlantirishga xizmat qiladi."
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "12345":
            session["admin"] = True
            return redirect(url_for("admin"))
        error = "Login yoki parol noto‘g‘ri"

    return render_template("login.html", error=error)


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    total_students = len(students)
    total_works = sum(s["works"] for s in students)
    active = len([s for s in students if s["status"] == "Faol"])
    avg = round(sum(s["score"] for s in students) / len(students)) if students else 0

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
        return redirect(url_for("admin_login"))

    name = request.form.get("name", "").strip()
    grade = request.form.get("grade", "").strip()
    direction = request.form.get("direction", "").strip()
    works = request.form.get("works", "0")
    score = request.form.get("score", "80")
    image = request.form.get("image", "").strip()
    description = request.form.get("description", "").strip()

    if not image:
        image = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1000&q=80"

    if not description:
        description = f"{name}ning elektron portfel materiallari ushbu sahifada jamlanadi."

    try:
        works = int(works)
    except ValueError:
        works = 0

    try:
        score = int(score)
    except ValueError:
        score = 80

    new_id = max([s["id"] for s in students]) + 1 if students else 1

    students.append({
        "id": new_id,
        "name": name,
        "grade": grade,
        "direction": direction,
        "status": "Faol",
        "works": works,
        "score": score,
        "image": image,
        "description": description,
        "projects": ["Raqamli artefakt", "Refleksiya", "Akademik natija"]
    })

    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:student_id>", methods=["POST"])
def admin_delete(student_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    global students
    students = [s for s in students if s["id"] != student_id]

    return redirect(url_for("admin"))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
