from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "muzeylab_super_secret_key"


students = [
    {
        "id": 1,
        "name": "Aliyev Muhammad",
        "grade": "7-sinf",
        "direction": "Tarix va muzeyshunoslik",
        "status": "Faol",
        "works": 12,
        "image": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=900&q=80",
        "description": "Tarixiy tafakkur, muzey eksponatlari va ijodiy loyiha ishlari bo‘yicha faol o‘quvchi."
    },
    {
        "id": 2,
        "name": "Karimova Madina",
        "grade": "8-sinf",
        "direction": "Madaniy meros",
        "status": "Faol",
        "works": 9,
        "image": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=80",
        "description": "Madaniy meros, mahalliy tarix va muzey pedagogikasi yo‘nalishida portfolioga ega."
    },
    {
        "id": 3,
        "name": "Saidov Javohir",
        "grade": "9-sinf",
        "direction": "Ilmiy loyiha",
        "status": "Ko‘rib chiqilmoqda",
        "works": 7,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=900&q=80",
        "description": "Tarixiy manbalar bilan ishlash va mustaqil tadqiqot olib borish ko‘nikmalarini shakllantirmoqda."
    }
]


BASE_CSS = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}

body {
    min-height: 100vh;
    background: #0f172a;
    color: #e5e7eb;
    overflow-x: hidden;
}

.bg-animation {
    position: fixed;
    inset: 0;
    z-index: -1;
    background:
        radial-gradient(circle at 15% 20%, rgba(59, 130, 246, 0.30), transparent 30%),
        radial-gradient(circle at 85% 10%, rgba(168, 85, 247, 0.25), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(14, 165, 233, 0.22), transparent 30%),
        linear-gradient(135deg, #020617, #0f172a, #1e293b);
    animation: bgMove 13s ease-in-out infinite alternate;
}

@keyframes bgMove {
    from { transform: scale(1); }
    to { transform: scale(1.08); }
}

a {
    color: inherit;
    text-decoration: none;
}

.navbar {
    height: 76px;
    width: 100%;
    background: rgba(15, 23, 42, 0.88);
    border-bottom: 1px solid rgba(148, 163, 184, 0.18);
    backdrop-filter: blur(18px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 42px;
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo {
    font-size: 25px;
    font-weight: 900;
    letter-spacing: .4px;
    background: linear-gradient(90deg, #38bdf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 24px;
}

.nav-links a {
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 600;
    transition: .25s;
}

.nav-links a:hover {
    color: #38bdf8;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    border: none;
    cursor: pointer;
    border-radius: 14px;
    padding: 13px 20px;
    font-weight: 800;
    font-size: 14px;
    transition: .28s;
}

.btn-primary {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    box-shadow: 0 14px 34px rgba(37, 99, 235, .32);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 44px rgba(124, 58, 237, .36);
}

.btn-secondary {
    background: rgba(51, 65, 85, .85);
    border: 1px solid rgba(148, 163, 184, .25);
    color: #e2e8f0;
}

.btn-danger {
    background: rgba(239, 68, 68, .18);
    color: #fecaca;
    border: 1px solid rgba(239, 68, 68, .32);
}

.hero {
    padding: 90px 42px 55px;
    max-width: 1260px;
    margin: auto;
    display: grid;
    grid-template-columns: 1.15fr .85fr;
    gap: 34px;
    align-items: center;
}

.hero-badge {
    display: inline-block;
    padding: 9px 14px;
    border-radius: 999px;
    background: rgba(56, 189, 248, .13);
    color: #7dd3fc;
    border: 1px solid rgba(56, 189, 248, .26);
    margin-bottom: 22px;
    font-size: 14px;
    font-weight: 800;
}

.hero h1 {
    font-size: 58px;
    line-height: 1.06;
    color: #fff;
    margin-bottom: 20px;
    letter-spacing: -1.5px;
}

.hero h1 span {
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #cbd5e1;
    font-size: 18px;
    line-height: 1.8;
    margin-bottom: 30px;
}

.hero-actions {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}

.hero-card {
    background: rgba(30, 41, 59, .78);
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 30px;
    padding: 28px;
    box-shadow: 0 25px 70px rgba(0, 0, 0, .30);
    backdrop-filter: blur(20px);
}

.hero-card img {
    width: 100%;
    height: 310px;
    object-fit: cover;
    border-radius: 24px;
    margin-bottom: 20px;
}

.hero-card h3 {
    color: #fff;
    font-size: 24px;
    margin-bottom: 10px;
}

.hero-card p {
    margin-bottom: 0;
    font-size: 15px;
    color: #94a3b8;
}

.section {
    max-width: 1260px;
    margin: auto;
    padding: 52px 42px;
}

.section-title {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 26px;
}

.section-title h2 {
    color: #fff;
    font-size: 36px;
    letter-spacing: -.7px;
}

.section-title p {
    color: #94a3b8;
    max-width: 620px;
    line-height: 1.7;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 22px;
}

.feature-card,
.portfolio-card,
.panel,
.stat-card {
    background: rgba(30, 41, 59, .78);
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 24px;
    box-shadow: 0 20px 45px rgba(0, 0, 0, .22);
    backdrop-filter: blur(18px);
    transition: .3s;
}

.feature-card:hover,
.portfolio-card:hover,
.stat-card:hover {
    transform: translateY(-6px);
    border-color: rgba(56, 189, 248, .46);
}

.feature-card {
    padding: 24px;
}

.feature-icon {
    width: 50px;
    height: 50px;
    border-radius: 16px;
    background: linear-gradient(135deg, #2563eb, #9333ea);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    font-size: 24px;
}

.feature-card h3 {
    color: #fff;
    font-size: 19px;
    margin-bottom: 10px;
}

.feature-card p {
    color: #94a3b8;
    line-height: 1.7;
    font-size: 14px;
}

.portfolio-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 22px;
}

.portfolio-card {
    overflow: hidden;
}

.portfolio-card img {
    width: 100%;
    height: 210px;
    object-fit: cover;
}

.card-body {
    padding: 22px;
}

.card-body h3 {
    color: #fff;
    font-size: 21px;
    margin-bottom: 8px;
}

.card-body p {
    color: #94a3b8;
    line-height: 1.7;
    font-size: 14px;
    margin-bottom: 15px;
}

.meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 14px;
}

.badge {
    display: inline-block;
    padding: 7px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
}

.badge-blue {
    background: rgba(59, 130, 246, .16);
    color: #93c5fd;
}

.badge-green {
    background: rgba(34, 197, 94, .16);
    color: #86efac;
}

.badge-yellow {
    background: rgba(245, 158, 11, .16);
    color: #fbbf24;
}

.footer {
    margin-top: 40px;
    padding: 28px 42px;
    border-top: 1px solid rgba(148, 163, 184, .16);
    color: #94a3b8;
    text-align: center;
    background: rgba(15, 23, 42, .65);
}

.login-wrap {
    min-height: calc(100vh - 76px);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 34px;
}

.login-card {
    width: 100%;
    max-width: 440px;
    background: rgba(30, 41, 59, .84);
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 28px;
    padding: 34px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, .30);
    backdrop-filter: blur(20px);
}

.login-card h2 {
    color: #fff;
    font-size: 31px;
    text-align: center;
    margin-bottom: 8px;
}

.login-card p {
    color: #94a3b8;
    text-align: center;
    margin-bottom: 24px;
    line-height: 1.6;
}

.form-group {
    margin-bottom: 18px;
}

.form-group label {
    display: block;
    color: #cbd5e1;
    margin-bottom: 8px;
    font-size: 14px;
    font-weight: 700;
}

input,
select,
textarea {
    width: 100%;
    padding: 14px 16px;
    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, .25);
    outline: none;
    background: rgba(15, 23, 42, .82);
    color: #fff;
    font-size: 15px;
}

input:focus,
select:focus,
textarea:focus {
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, .15);
}

.alert {
    padding: 13px 15px;
    border-radius: 14px;
    margin-bottom: 18px;
    font-size: 14px;
}

.alert-danger {
    background: rgba(239, 68, 68, .14);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, .24);
}

.alert-success {
    background: rgba(34, 197, 94, .14);
    color: #86efac;
    border: 1px solid rgba(34, 197, 94, .24);
}

.dashboard {
    display: flex;
    min-height: calc(100vh - 76px);
}

.sidebar {
    width: 286px;
    padding: 28px 20px;
    background: rgba(15, 23, 42, .80);
    border-right: 1px solid rgba(148, 163, 184, .15);
    backdrop-filter: blur(18px);
}

.sidebar h2 {
    color: #fff;
    font-size: 21px;
    margin-bottom: 26px;
}

.sidebar a {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #cbd5e1;
    padding: 14px 16px;
    border-radius: 15px;
    margin-bottom: 10px;
    font-weight: 700;
    transition: .25s;
}

.sidebar a:hover,
.sidebar a.active {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: #fff;
    box-shadow: 0 12px 28px rgba(37, 99, 235, .28);
}

.content {
    flex: 1;
    padding: 34px;
}

.content-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 18px;
    margin-bottom: 28px;
}

.content-header h1 {
    color: #fff;
    font-size: 34px;
    letter-spacing: -.7px;
}

.content-header p {
    color: #94a3b8;
    margin-top: 6px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 22px;
    margin-bottom: 28px;
}

.stat-card {
    padding: 24px;
}

.stat-icon {
    width: 50px;
    height: 50px;
    border-radius: 16px;
    background: linear-gradient(135deg, #2563eb, #9333ea);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
    font-size: 23px;
}

.stat-card h3 {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 8px;
}

.stat-card .number {
    color: #fff;
    font-size: 34px;
    font-weight: 900;
}

.stat-card span {
    display: block;
    color: #4ade80;
    margin-top: 8px;
    font-size: 13px;
}

.panel {
    padding: 26px;
    margin-bottom: 26px;
}

.panel h2 {
    color: #fff;
    font-size: 23px;
    margin-bottom: 18px;
}

.table-wrapper {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
}

thead {
    background: rgba(15, 23, 42, .78);
}

th,
td {
    padding: 16px;
    text-align: left;
    border-bottom: 1px solid rgba(148, 163, 184, .14);
    font-size: 14px;
}

th {
    color: #93c5fd;
}

td {
    color: #e2e8f0;
}

tr:hover {
    background: rgba(51, 65, 85, .46);
}

.admin-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
}

.form-box {
    background: rgba(15, 23, 42, .35);
    border: 1px solid rgba(148, 163, 184, .16);
    border-radius: 20px;
    padding: 20px;
}

.form-box h3 {
    color: #fff;
    margin-bottom: 16px;
}

textarea {
    min-height: 120px;
    resize: vertical;
}

.action-form {
    display: inline;
}

@media (max-width: 1100px) {
    .hero {
        grid-template-columns: 1fr;
    }

    .features-grid,
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .portfolio-grid,
    .admin-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 760px) {
    .navbar {
        padding: 0 20px;
    }

    .nav-links {
        gap: 12px;
    }

    .nav-links a {
        font-size: 13px;
    }

    .hero,
    .section {
        padding-left: 22px;
        padding-right: 22px;
    }

    .hero h1 {
        font-size: 39px;
    }

    .features-grid,
    .stats-grid,
    .portfolio-grid {
        grid-template-columns: 1fr;
    }

    .dashboard {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        border-right: none;
        border-bottom: 1px solid rgba(148, 163, 184, .15);
    }

    .content {
        padding: 22px;
    }

    .content-header {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
"""


def navbar():
    return """
    <div class="navbar">
        <a class="logo" href="/">MuzeyLab Portfolio</a>
        <div class="nav-links">
            <a href="/">Bosh sahifa</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/admin/login">Admin</a>
        </div>
    </div>
    """


@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MuzeyLab Portfolio</title>
        {{ css|safe }}
    </head>
    <body>
        <div class="bg-animation"></div>
        {{ navbar|safe }}

        <section class="hero">
            <div>
                <div class="hero-badge">Premium o‘quvchi portfolio platformasi</div>
                <h1>O‘quvchilar yutuqlarini <span>zamonaviy portfolio</span> shaklida namoyish qiling</h1>
                <p>
                    MuzeyLab Portfolio — o‘qituvchi tomonidan boshqariladigan, o‘quvchilar esa ko‘ra oladigan
                    zamonaviy elektron portfolio platformasi. Unda ilmiy ishlar, ijodiy topshiriqlar,
                    tarixiy loyihalar va o‘quv natijalari tartibli ko‘rinishda jamlanadi.
                </p>
                <div class="hero-actions">
                    <a class="btn btn-primary" href="/portfolio">Portfoliolarni ko‘rish</a>
                    <a class="btn btn-secondary" href="/admin/login">Admin panel</a>
                </div>
            </div>

            <div class="hero-card">
                <img src="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=80">
                <h3>Yillik o‘quv portfolio</h3>
                <p>
                    Har bir o‘quvchining faoliyati, loyiha ishlari, baholash natijalari va ijodiy ishlari
                    yagona tizimda saqlanadi.
                </p>
            </div>
        </section>

        <section class="section">
            <div class="section-title">
                <div>
                    <h2>Platforma imkoniyatlari</h2>
                    <p>Sayt o‘qituvchi uchun boshqaruv, o‘quvchi va ota-onalar uchun esa qulay ko‘rish imkoniyatini beradi.</p>
                </div>
            </div>

            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🎓</div>
                    <h3>O‘quvchi profili</h3>
                    <p>Har bir o‘quvchi uchun alohida sahifa, sinf, yo‘nalish va faoliyat tavsifi.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📚</div>
                    <h3>Loyiha ishlari</h3>
                    <p>Tarix, muzeyshunoslik va madaniy meros bo‘yicha ijodiy ishlarni joylash imkoniyati.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔐</div>
                    <h3>Admin boshqaruvi</h3>
                    <p>Oddiy foydalanuvchilar faqat ko‘radi, admin esa kontentni boshqaradi.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Statistika</h3>
                    <p>O‘quvchilar, ishlar, faol portfolio va umumiy ko‘rsatkichlar dashboardda chiqadi.</p>
                </div>
            </div>
        </section>

        <div class="footer">
            © 2026 MuzeyLab Portfolio. O‘quvchilar yillik portfolio platformasi.
        </div>
    </body>
    </html>
    """
    return render_template_string(html, css=BASE_CSS, navbar=navbar())


@app.route("/portfolio")
def portfolio():
    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portfolio</title>
        {{ css|safe }}
    </head>
    <body>
        <div class="bg-animation"></div>
        {{ navbar|safe }}

        <section class="section">
            <div class="section-title">
                <div>
                    <h2>O‘quvchilar portfoliolari</h2>
                    <p>Bu sahifada o‘quvchilarning yillik faoliyati, loyiha ishlari va ta’limiy natijalari ko‘rsatiladi.</p>
                </div>
                <a class="btn btn-primary" href="/admin/login">Admin kirish</a>
            </div>

            <div class="portfolio-grid">
                {% for s in students %}
                <div class="portfolio-card">
                    <img src="{{ s.image }}" alt="{{ s.name }}">
                    <div class="card-body">
                        <h3>{{ s.name }}</h3>
                        <div class="meta">
                            <span class="badge badge-blue">{{ s.grade }}</span>
                            <span class="badge badge-green">{{ s.direction }}</span>
                        </div>
                        <p>{{ s.description }}</p>
                        <span class="badge badge-yellow">{{ s.works }} ta ish</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <div class="footer">
            © 2026 MuzeyLab Portfolio.
        </div>
    </body>
    </html>
    """
    return render_template_string(html, css=BASE_CSS, navbar=navbar(), students=students)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "12345":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Login yoki parol noto‘g‘ri. Login: admin, parol: 12345"

    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Login</title>
        {{ css|safe }}
    </head>
    <body>
        <div class="bg-animation"></div>
        {{ navbar|safe }}

        <div class="login-wrap">
            <form class="login-card" method="POST">
                <h2>Admin panel</h2>
                <p>Portfolio ma’lumotlarini boshqarish uchun tizimga kiring.</p>

                {% if error %}
                <div class="alert alert-danger">{{ error }}</div>
                {% endif %}

                <div class="form-group">
                    <label>Login</label>
                    <input type="text" name="username" placeholder="admin" required>
                </div>

                <div class="form-group">
                    <label>Parol</label>
                    <input type="password" name="password" placeholder="12345" required>
                </div>

                <button class="btn btn-primary" style="width:100%;" type="submit">Kirish</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, css=BASE_CSS, navbar=navbar(), error=error)


@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    total_students = len(students)
    total_works = sum(s["works"] for s in students)
    active_students = len([s for s in students if s["status"] == "Faol"])

    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard</title>
        {{ css|safe }}
    </head>
    <body>
        <div class="bg-animation"></div>
        {{ navbar|safe }}

        <div class="dashboard">
            <aside class="sidebar">
                <h2>Admin boshqaruvi</h2>
                <a class="active" href="/admin">📊 Dashboard</a>
                <a href="/portfolio">🎓 Portfoliolar</a>
                <a href="#add-student">➕ O‘quvchi qo‘shish</a>
                <a href="#">📁 Loyiha ishlari</a>
                <a href="#">⚙️ Sozlamalar</a>
                <a href="/admin/logout">🚪 Chiqish</a>
            </aside>

            <main class="content">
                <div class="content-header">
                    <div>
                        <h1>Dashboard</h1>
                        <p>O‘quvchilar portfolio tizimining umumiy boshqaruv oynasi.</p>
                    </div>
                    <a class="btn btn-primary" href="/portfolio">Saytni ko‘rish</a>
                </div>

                {% if request.args.get('success') %}
                <div class="alert alert-success">Yangi o‘quvchi muvaffaqiyatli qo‘shildi.</div>
                {% endif %}

                {% if request.args.get('deleted') %}
                <div class="alert alert-success">O‘quvchi ro‘yxatdan o‘chirildi.</div>
                {% endif %}

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">👥</div>
                        <h3>Jami o‘quvchilar</h3>
                        <div class="number">{{ total_students }}</div>
                        <span>portfolio tizimida</span>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon">📚</div>
                        <h3>Jami ishlar</h3>
                        <div class="number">{{ total_works }}</div>
                        <span>loyiha va ijodiy ishlar</span>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon">✅</div>
                        <h3>Faol portfoliolar</h3>
                        <div class="number">{{ active_students }}</div>
                        <span>faol kuzatuvda</span>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon">🏛️</div>
                        <h3>Yo‘nalishlar</h3>
                        <div class="number">3</div>
                        <span>tarix, muzey, meros</span>
                    </div>
                </div>

                <div class="panel">
                    <h2>O‘quvchilar ro‘yxati</h2>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Ism-familiya</th>
                                    <th>Sinf</th>
                                    <th>Yo‘nalish</th>
                                    <th>Ishlar</th>
                                    <th>Status</th>
                                    <th>Amal</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for s in students %}
                                <tr>
                                    <td>{{ s.name }}</td>
                                    <td>{{ s.grade }}</td>
                                    <td>{{ s.direction }}</td>
                                    <td>{{ s.works }}</td>
                                    <td>
                                        {% if s.status == "Faol" %}
                                        <span class="badge badge-green">{{ s.status }}</span>
                                        {% else %}
                                        <span class="badge badge-yellow">{{ s.status }}</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <form class="action-form" method="POST" action="/admin/delete/{{ s.id }}">
                                            <button class="btn btn-danger" type="submit">O‘chirish</button>
                                        </form>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="admin-grid" id="add-student">
                    <div class="panel">
                        <h2>Yangi o‘quvchi qo‘shish</h2>
                        <form class="form-box" method="POST" action="/admin/add">
                            <h3>Portfolio ma’lumotlari</h3>

                            <div class="form-group">
                                <label>Ism-familiya</label>
                                <input name="name" placeholder="Masalan: Ahmedov Sarvar" required>
                            </div>

                            <div class="form-group">
                                <label>Sinf</label>
                                <input name="grade" placeholder="Masalan: 8-sinf" required>
                            </div>

                            <div class="form-group">
                                <label>Yo‘nalish</label>
                                <select name="direction">
                                    <option>Tarix va muzeyshunoslik</option>
                                    <option>Madaniy meros</option>
                                    <option>Ilmiy loyiha</option>
                                </select>
                            </div>

                            <div class="form-group">
                                <label>Ishlar soni</label>
                                <input name="works" type="number" min="0" value="0">
                            </div>

                            <div class="form-group">
                                <label>Status</label>
                                <select name="status">
                                    <option>Faol</option>
                                    <option>Ko‘rib chiqilmoqda</option>
                                </select>
                            </div>

                            <div class="form-group">
                                <label>Rasm URL</label>
                                <input name="image" placeholder="Rasm linki. Bo‘sh qolsa standart rasm chiqadi.">
                            </div>

                            <button class="btn btn-primary" style="width:100%;" type="submit">Saqlash</button>
                        </form>
                    </div>

                    <div class="panel">
                        <h2>Portfolio tavsifi</h2>
                        <div class="form-box">
                            <h3>Tezkor eslatma</h3>

                            <div class="form-group">
                                <label>Tavsif</label>
                                <textarea readonly>Yangi o‘quvchi qo‘shish formasida ism, sinf, yo‘nalish, ishlar soni va status kiritiladi. Ma’lumot saqlangach, o‘quvchi darhol portfolio sahifasida ko‘rinadi.</textarea>
                            </div>

                            <a class="btn btn-secondary" style="width:100%;" href="/portfolio">Portfolio sahifasini ochish</a>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </body>
    </html>
    """
    return render_template_string(
        html,
        css=BASE_CSS,
        navbar=navbar(),
        students=students,
        total_students=total_students,
        total_works=total_works,
        active_students=active_students,
        request=request
    )


@app.route("/admin/add", methods=["POST"])
def add_student():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    name = request.form.get("name")
    grade = request.form.get("grade")
    direction = request.form.get("direction")
    status = request.form.get("status")
    works = request.form.get("works")
    image = request.form.get("image")

    if not image:
        image = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=900&q=80"

    try:
        works = int(works)
    except:
        works = 0

    new_id = max([s["id"] for s in students]) + 1 if students else 1

    students.append({
        "id": new_id,
        "name": name,
        "grade": grade,
        "direction": direction,
        "status": status,
        "works": works,
        "image": image,
        "description": f"{name}ning yillik o‘quv faoliyati, loyiha ishlari va portfolio natijalari ushbu sahifada jamlanadi."
    })

    return redirect(url_for("admin_dashboard", success=1))


@app.route("/admin/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    global students
    students = [s for s in students if s["id"] != student_id]

    return redirect(url_for("admin_dashboard", deleted=1))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
