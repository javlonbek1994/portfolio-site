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
        "score": 94,
        "image": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1000&q=80",
        "description": "Tarixiy tafakkur, muzey eksponatlari va ijodiy loyiha ishlari bo‘yicha faol o‘quvchi.",
        "projects": ["Muzey eksponatlari tahlili", "Mahalliy tarix loyihasi", "Tarixiy xarita bilan ishlash"]
    },
    {
        "id": 2,
        "name": "Karimova Madina",
        "grade": "8-sinf",
        "direction": "Madaniy meros",
        "status": "Faol",
        "works": 9,
        "score": 88,
        "image": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1000&q=80",
        "description": "Madaniy meros, mahalliy tarix va muzey pedagogikasi yo‘nalishida portfolioga ega.",
        "projects": ["Madaniy meros taqdimoti", "Oila tarixi loyihasi", "Muzeyga virtual sayohat"]
    },
    {
        "id": 3,
        "name": "Saidov Javohir",
        "grade": "9-sinf",
        "direction": "Ilmiy loyiha",
        "status": "Ko‘rib chiqilmoqda",
        "works": 7,
        "score": 81,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1000&q=80",
        "description": "Tarixiy manbalar bilan ishlash va mustaqil tadqiqot olib borish ko‘nikmalarini shakllantirmoqda.",
        "projects": ["Tarixiy manba tahlili", "Mini tadqiqot ishi", "Ilmiy poster"]
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

html {
    scroll-behavior: smooth;
}

body {
    min-height: 100vh;
    background: #07111f;
    color: #e5e7eb;
    overflow-x: hidden;
}

.bg {
    position: fixed;
    inset: 0;
    z-index: -1;
    background:
        radial-gradient(circle at 15% 18%, rgba(14, 165, 233, .30), transparent 30%),
        radial-gradient(circle at 85% 8%, rgba(168, 85, 247, .24), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(34, 197, 94, .13), transparent 28%),
        linear-gradient(135deg, #020617, #0f172a, #111827);
}

a {
    color: inherit;
    text-decoration: none;
}

.navbar {
    height: 78px;
    padding: 0 44px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(2, 6, 23, .76);
    border-bottom: 1px solid rgba(148, 163, 184, .16);
    backdrop-filter: blur(18px);
    position: sticky;
    top: 0;
    z-index: 99;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 24px;
    font-weight: 900;
    color: #fff;
}

.logo span {
    width: 42px;
    height: 42px;
    border-radius: 15px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #0ea5e9, #7c3aed);
    box-shadow: 0 12px 30px rgba(14, 165, 233, .28);
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 24px;
}

.nav-links a {
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 700;
}

.nav-links a:hover {
    color: #38bdf8;
}

.btn {
    border: 0;
    outline: 0;
    cursor: pointer;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    padding: 13px 18px;
    border-radius: 15px;
    font-size: 14px;
    font-weight: 900;
    transition: .25s;
}

.btn-primary {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: #fff;
    box-shadow: 0 16px 34px rgba(37, 99, 235, .30);
}

.btn-primary:hover {
    transform: translateY(-2px);
}

.btn-secondary {
    background: rgba(30, 41, 59, .82);
    color: #e2e8f0;
    border: 1px solid rgba(148, 163, 184, .22);
}

.btn-danger {
    background: rgba(239, 68, 68, .15);
    color: #fecaca;
    border: 1px solid rgba(239, 68, 68, .28);
}

.hero {
    max-width: 1260px;
    margin: 0 auto;
    padding: 88px 44px 55px;
    display: grid;
    grid-template-columns: 1.15fr .85fr;
    gap: 36px;
    align-items: center;
}

.badge-soft {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 9px 14px;
    border-radius: 999px;
    background: rgba(14, 165, 233, .13);
    border: 1px solid rgba(14, 165, 233, .28);
    color: #7dd3fc;
    font-size: 14px;
    font-weight: 900;
    margin-bottom: 22px;
}

.hero h1 {
    font-size: 62px;
    line-height: 1.04;
    letter-spacing: -1.7px;
    color: #fff;
    margin-bottom: 22px;
}

.hero h1 strong {
    background: linear-gradient(90deg, #38bdf8, #c084fc, #86efac);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #cbd5e1;
    font-size: 18px;
    line-height: 1.85;
    margin-bottom: 30px;
}

.hero-actions {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}

.hero-preview {
    background: rgba(15, 23, 42, .76);
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 32px;
    padding: 22px;
    box-shadow: 0 28px 80px rgba(0, 0, 0, .35);
    backdrop-filter: blur(18px);
}

.hero-preview img {
    width: 100%;
    height: 320px;
    object-fit: cover;
    border-radius: 24px;
}

.preview-info {
    padding: 20px 8px 6px;
}

.preview-info h3 {
    color: #fff;
    font-size: 24px;
    margin-bottom: 8px;
}

.preview-info p {
    margin: 0;
    font-size: 15px;
    color: #94a3b8;
}

.section {
    max-width: 1260px;
    margin: 0 auto;
    padding: 54px 44px;
}

.section-head {
    display: flex;
    justify-content: space-between;
    align-items: end;
    gap: 20px;
    margin-bottom: 28px;
}

.section-head h2 {
    color: #fff;
    font-size: 38px;
    letter-spacing: -.8px;
}

.section-head p {
    color: #94a3b8;
    line-height: 1.7;
    max-width: 650px;
}

.feature-grid,
.stats-grid,
.portfolio-grid {
    display: grid;
    gap: 22px;
}

.feature-grid {
    grid-template-columns: repeat(4, 1fr);
}

.stats-grid {
    grid-template-columns: repeat(4, 1fr);
    margin-bottom: 28px;
}

.portfolio-grid {
    grid-template-columns: repeat(3, 1fr);
}

.card,
.feature-card,
.portfolio-card,
.stat-card,
.panel,
.profile-card {
    background: rgba(15, 23, 42, .76);
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 26px;
    box-shadow: 0 22px 50px rgba(0, 0, 0, .24);
    backdrop-filter: blur(18px);
}

.feature-card,
.stat-card,
.panel,
.profile-card {
    padding: 24px;
}

.feature-card {
    transition: .25s;
}

.feature-card:hover,
.portfolio-card:hover,
.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(56, 189, 248, .45);
}

.icon-box {
    width: 52px;
    height: 52px;
    border-radius: 17px;
    display: grid;
    place-items: center;
    font-size: 24px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    margin-bottom: 16px;
}

.feature-card h3 {
    color: #fff;
    font-size: 19px;
    margin-bottom: 10px;
}

.feature-card p {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.7;
}

.portfolio-card {
    overflow: hidden;
    transition: .25s;
}

.portfolio-card img {
    width: 100%;
    height: 215px;
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
    margin-bottom: 16px;
}

.meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 14px;
}

.badge {
    display: inline-flex;
    padding: 7px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 900;
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

.badge-purple {
    background: rgba(168, 85, 247, .16);
    color: #d8b4fe;
}

.footer {
    margin-top: 48px;
    padding: 30px 44px;
    text-align: center;
    color: #94a3b8;
    border-top: 1px solid rgba(148, 163, 184, .15);
    background: rgba(2, 6, 23, .55);
}

.login-wrap {
    min-height: calc(100vh - 78px);
    display: grid;
    place-items: center;
    padding: 34px;
}

.login-card {
    width: 100%;
    max-width: 450px;
    padding: 34px;
    background: rgba(15, 23, 42, .82);
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 30px;
    box-shadow: 0 28px 75px rgba(0, 0, 0, .34);
}

.login-card h2 {
    color: #fff;
    font-size: 32px;
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
    margin-bottom: 17px;
}

.form-group label {
    display: block;
    color: #cbd5e1;
    margin-bottom: 8px;
    font-size: 14px;
    font-weight: 800;
}

input,
select,
textarea {
    width: 100%;
    padding: 14px 16px;
    border-radius: 15px;
    border: 1px solid rgba(148, 163, 184, .23);
    outline: none;
    background: rgba(2, 6, 23, .74);
    color: #fff;
    font-size: 15px;
}

input:focus,
select:focus,
textarea:focus {
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, .13);
}

textarea {
    min-height: 116px;
    resize: vertical;
}

.alert {
    padding: 13px 15px;
    border-radius: 15px;
    margin-bottom: 18px;
    font-size: 14px;
    font-weight: 800;
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
    min-height: calc(100vh - 78px);
}

.sidebar {
    width: 292px;
    padding: 28px 20px;
    background: rgba(2, 6, 23, .65);
    border-right: 1px solid rgba(148, 163, 184, .14);
    backdrop-filter: blur(18px);
}

.sidebar h2 {
    color: #fff;
    font-size: 21px;
    margin-bottom: 24px;
}

.sidebar a {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 16px;
    color: #cbd5e1;
    margin-bottom: 10px;
    font-weight: 850;
}

.sidebar a:hover,
.sidebar a.active {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: #fff;
}

.content {
    flex: 1;
    padding: 34px;
}

.content-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    margin-bottom: 28px;
}

.content-head h1 {
    color: #fff;
    font-size: 35px;
    letter-spacing: -.7px;
}

.content-head p {
    color: #94a3b8;
    margin-top: 6px;
}

.stat-card .stat-icon {
    width: 50px;
    height: 50px;
    border-radius: 17px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    display: grid;
    place-items: center;
    font-size: 23px;
    margin-bottom: 15px;
}

.stat-card h3 {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 8px;
}

.stat-card .number {
    color: #fff;
    font-size: 35px;
    font-weight: 950;
}

.stat-card span {
    color: #86efac;
    font-size: 13px;
    display: block;
    margin-top: 8px;
}

.panel {
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
    background: rgba(2, 6, 23, .72);
}

th,
td {
    padding: 16px;
    text-align: left;
    border-bottom: 1px solid rgba(148, 163, 184, .13);
    font-size: 14px;
}

th {
    color: #93c5fd;
}

td {
    color: #e2e8f0;
}

tr:hover {
    background: rgba(30, 41, 59, .46);
}

.admin-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
}

.search-row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
    margin-bottom: 18px;
}

.profile-wrap {
    max-width: 1120px;
    margin: 0 auto;
    padding: 54px 44px;
}

.profile-hero {
    display: grid;
    grid-template-columns: 360px 1fr;
    gap: 28px;
    align-items: start;
}

.profile-hero img {
    width: 100%;
    height: 390px;
    object-fit: cover;
    border-radius: 26px;
}

.profile-card h1 {
    color: #fff;
    font-size: 38px;
    margin-bottom: 10px;
}

.profile-card p {
    color: #cbd5e1;
    line-height: 1.8;
    margin: 16px 0;
}

.project-list {
    margin-top: 20px;
    display: grid;
    gap: 12px;
}

.project-item {
    padding: 14px 16px;
    border-radius: 16px;
    background: rgba(2, 6, 23, .45);
    border: 1px solid rgba(148, 163, 184, .14);
    color: #e2e8f0;
}

@media (max-width: 1050px) {
    .hero,
    .profile-hero {
        grid-template-columns: 1fr;
    }

    .feature-grid,
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
        gap: 10px;
    }

    .nav-links a {
        font-size: 13px;
    }

    .hero,
    .section,
    .profile-wrap {
        padding-left: 22px;
        padding-right: 22px;
    }

    .hero h1 {
        font-size: 40px;
    }

    .feature-grid,
    .stats-grid,
    .portfolio-grid {
        grid-template-columns: 1fr;
    }

    .dashboard {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        border-right: 0;
        border-bottom: 1px solid rgba(148, 163, 184, .14);
    }

    .content {
        padding: 22px;
    }

    .content-head,
    .section-head {
        flex-direction: column;
        align-items: flex-start;
    }

    .search-row {
        grid-template-columns: 1fr;
    }
}
</style>
"""


def navbar():
    return """
    <div class="navbar">
        <a class="logo" href="/">
            <span>🏛️</span>
            MuzeyLab
        </a>
        <div class="nav-links">
            <a href="/">Bosh sahifa</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/admin/login">Admin</a>
        </div>
    </div>
    """


@app.route("/")
def home():
    total_students = len(students)
    total_works = sum(s["works"] for s in students)

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
        <div class="bg"></div>
        {{ navbar|safe }}

        <section class="hero">
            <div>
                <div class="badge-soft">🏛️ Elektron o‘quvchi portfolio platformasi</div>
                <h1>O‘quvchilar yutuqlarini <strong>zamonaviy va tartibli</strong> ko‘rsating</h1>
                <p>
                    MuzeyLab Portfolio — o‘qituvchi tomonidan boshqariladigan, o‘quvchilar va ota-onalar
                    ko‘ra oladigan zamonaviy portfolio platformasi. Unda loyiha ishlari, ijodiy topshiriqlar,
                    tarixiy tadqiqotlar va yillik natijalar jamlanadi.
                </p>
                <div class="hero-actions">
                    <a class="btn btn-primary" href="/portfolio">Portfoliolarni ko‘rish</a>
                    <a class="btn btn-secondary" href="/admin/login">Admin panel</a>
                </div>
            </div>

            <div class="hero-preview">
                <img src="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1000&q=80">
                <div class="preview-info">
                    <h3>Yillik portfolio boshqaruvi</h3>
                    <p>O‘quvchi faoliyati, loyiha ishlari va natijalari bitta sahifada jamlanadi.</p>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <h3>Jami o‘quvchilar</h3>
                    <div class="number">{{ total_students }}</div>
                    <span>platformada mavjud</span>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📚</div>
                    <h3>Jami ishlar</h3>
                    <div class="number">{{ total_works }}</div>
                    <span>portfolio materiallari</span>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🏛️</div>
                    <h3>Yo‘nalishlar</h3>
                    <div class="number">3</div>
                    <span>tarix, muzey, meros</span>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🔐</div>
                    <h3>Boshqaruv</h3>
                    <div class="number">Admin</div>
                    <span>faqat admin tahrirlaydi</span>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="section-head">
                <div>
                    <h2>Platforma imkoniyatlari</h2>
                    <p>Sayt o‘quvchilar portfoliolarini ochiq, chiroyli va tartibli ko‘rsatish uchun moslashtirilgan.</p>
                </div>
            </div>

            <div class="feature-grid">
                <div class="feature-card">
                    <div class="icon-box">🎓</div>
                    <h3>O‘quvchi profili</h3>
                    <p>Har bir o‘quvchiga alohida sahifa, rasm, sinf, yo‘nalish va tavsif beriladi.</p>
                </div>
                <div class="feature-card">
                    <div class="icon-box">📁</div>
                    <h3>Loyiha ishlari</h3>
                    <p>Ijodiy ishlar, tadqiqotlar va muzey pedagogikasi topshiriqlari ko‘rsatiladi.</p>
                </div>
                <div class="feature-card">
                    <div class="icon-box">📊</div>
                    <h3>Dashboard</h3>
                    <p>Admin o‘quvchilar soni, ishlar soni va umumiy holatni tez ko‘ra oladi.</p>
                </div>
                <div class="feature-card">
                    <div class="icon-box">🔎</div>
                    <h3>Qidiruv</h3>
                    <p>Admin panelda o‘quvchilarni ism, sinf yoki yo‘nalish bo‘yicha qidirish mumkin.</p>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="section-head">
                <div>
                    <h2>Faol portfoliolar</h2>
                    <p>Quyida platformaga joylangan o‘quvchilar portfoliolaridan namunalar berilgan.</p>
                </div>
                <a class="btn btn-primary" href="/portfolio">Barchasini ko‘rish</a>
            </div>

            <div class="portfolio-grid">
                {% for s in students[:3] %}
                <div class="portfolio-card">
                    <img src="{{ s.image }}">
                    <div class="card-body">
                        <h3>{{ s.name }}</h3>
                        <div class="meta">
                            <span class="badge badge-blue">{{ s.grade }}</span>
                            <span class="badge badge-green">{{ s.direction }}</span>
                            <span class="badge badge-purple">{{ s.score }} ball</span>
                        </div>
                        <p>{{ s.description }}</p>
                        <a class="btn btn-secondary" href="/student/{{ s.id }}">Batafsil ko‘rish</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <div class="footer">© 2026 MuzeyLab Portfolio. O‘quvchilar yillik portfolio platformasi.</div>
    </body>
    </html>
    """
    return render_template_string(html, css=BASE_CSS, navbar=navbar(), students=students,
                                  total_students=total_students, total_works=total_works)


@app.route("/portfolio")
def portfolio():
    q = request.args.get("q", "").lower().strip()

    if q:
        filtered = [
            s for s in students
            if q in s["name"].lower()
            or q in s["grade"].lower()
            or q in s["direction"].lower()
            or q in s["status"].lower()
        ]
    else:
        filtered = students

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
        <div class="bg"></div>
        {{ navbar|safe }}

        <section class="section">
            <div class="section-head">
                <div>
                    <h2>O‘quvchilar portfoliolari</h2>
                    <p>O‘quvchilarning yillik faoliyati, loyiha ishlari, tarixiy tadqiqotlari va natijalari.</p>
                </div>
                <a class="btn btn-primary" href="/admin/login">Admin kirish</a>
            </div>

            <form class="search-row" method="GET">
                <input name="q" value="{{ q }}" placeholder="Ism, sinf, yo‘nalish yoki status bo‘yicha qidirish...">
                <button class="btn btn-primary" type="submit">Qidirish</button>
            </form>

            <div class="portfolio-grid">
                {% for s in filtered %}
                <div class="portfolio-card">
                    <img src="{{ s.image }}" alt="{{ s.name }}">
                    <div class="card-body">
                        <h3>{{ s.name }}</h3>
                        <div class="meta">
                            <span class="badge badge-blue">{{ s.grade }}</span>
                            <span class="badge badge-green">{{ s.direction }}</span>
                            <span class="badge badge-yellow">{{ s.works }} ta ish</span>
                            <span class="badge badge-purple">{{ s.score }} ball</span>
                        </div>
                        <p>{{ s.description }}</p>
                        <a class="btn btn-secondary" href="/student/{{ s.id }}">Batafsil ko‘rish</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <div class="footer">© 2026 MuzeyLab Portfolio.</div>
    </body>
    </html>
    """
    return render_template_string(html, css=BASE_CSS, navbar=navbar(), filtered=filtered, q=q)


@app.route("/student/<int:student_id>")
def student_profile(student_id):
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        return redirect(url_for("portfolio"))

    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ student.name }}</title>
        {{ css|safe }}
    </head>
    <body>
        <div class="bg"></div>
        {{ navbar|safe }}

        <div class="profile-wrap">
            <div class="profile-hero">
                <img src="{{ student.image }}" alt="{{ student.name }}">

                <div class="profile-card">
                    <div class="badge-soft">🎓 O‘quvchi portfolio profili</div>
                    <h1>{{ student.name }}</h1>

                    <div class="meta">
                        <span class="badge badge-blue">{{ student.grade }}</span>
                        <span class="badge badge-green">{{ student.direction }}</span>
                        <span class="badge badge-yellow">{{ student.works }} ta ish</span>
                        <span class="badge badge-purple">{{ student.score }} ball</span>
                    </div>

                    <p>{{ student.description }}</p>

                    <h2 style="color:#fff; margin-top:22px; margin-bottom:12px;">Portfolio ishlari</h2>
                    <div class="project-list">
                        {% for p in student.projects %}
                        <div class="project-item">📌 {{ p }}</div>
                        {% endfor %}
                    </div>

                    <div style="margin-top:24px;">
                        <a class="btn btn-primary" href="/portfolio">Ortga qaytish</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">© 2026 MuzeyLab Portfolio.</div>
    </body>
    </html>
    """
    return render_template_string(html, css=BASE_CSS, navbar=navbar(), student=student)


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
        <div class="bg"></div>
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

    q = request.args.get("q", "").lower().strip()

    if q:
        filtered = [
            s for s in students
            if q in s["name"].lower()
            or q in s["grade"].lower()
            or q in s["direction"].lower()
            or q in s["status"].lower()
        ]
    else:
        filtered = students

    total_students = len(students)
    total_works = sum(s["works"] for s in students)
    active_students = len([s for s in students if s["status"] == "Faol"])
    avg_score = round(sum(s["score"] for s in students) / len(students)) if students else 0

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
        <div class="bg"></div>
        {{ navbar|safe }}

        <div class="dashboard">
            <aside class="sidebar">
                <h2>Admin boshqaruvi</h2>
                <a class="active" href="/admin">📊 Dashboard</a>
                <a href="/portfolio">🎓 Portfoliolar</a>
                <a href="#add-student">➕ O‘quvchi qo‘shish</a>
                <a href="#students-list">👥 Ro‘yxat</a>
                <a href="/">🌐 Sayt bosh sahifasi</a>
                <a href="/admin/logout">🚪 Chiqish</a>
            </aside>

            <main class="content">
                <div class="content-head">
                    <div>
                        <h1>Admin Dashboard</h1>
                        <p>O‘quvchilar portfolio tizimini boshqarish oynasi.</p>
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
                        <div class="stat-icon">⭐</div>
                        <h3>O‘rtacha ball</h3>
                        <div class="number">{{ avg_score }}</div>
                        <span>umumiy natija</span>
                    </div>
                </div>

                <div class="panel" id="students-list">
                    <h2>O‘quvchilar ro‘yxati</h2>

                    <form class="search-row" method="GET" action="/admin">
                        <input name="q" value="{{ q }}" placeholder="Ism, sinf, yo‘nalish yoki status bo‘yicha qidirish...">
                        <button class="btn btn-primary" type="submit">Qidirish</button>
                    </form>

                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Ism-familiya</th>
                                    <th>Sinf</th>
                                    <th>Yo‘nalish</th>
                                    <th>Ishlar</th>
                                    <th>Ball</th>
                                    <th>Status</th>
                                    <th>Amal</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for s in filtered %}
                                <tr>
                                    <td>{{ s.name }}</td>
                                    <td>{{ s.grade }}</td>
                                    <td>{{ s.direction }}</td>
                                    <td>{{ s.works }}</td>
                                    <td>{{ s.score }}</td>
                                    <td>
                                        {% if s.status == "Faol" %}
                                        <span class="badge badge-green">{{ s.status }}</span>
                                        {% else %}
                                        <span class="badge badge-yellow">{{ s.status }}</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a class="btn btn-secondary" href="/student/{{ s.id }}">Ko‘rish</a>
                                        <form style="display:inline;" method="POST" action="/admin/delete/{{ s.id }}">
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
                        <form method="POST" action="/admin/add">
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
                                <label>Ball</label>
                                <input name="score" type="number" min="0" max="100" value="80">
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
                            <div class="form-group">
                                <label>Qisqacha tavsif</label>
                                <textarea name="description" placeholder="O‘quvchi portfolioga oid qisqacha tavsif..."></textarea>
                            </div>
                            <button class="btn btn-primary" style="width:100%;" type="submit">Saqlash</button>
                        </form>
                    </div>

                    <div class="panel">
                        <h2>Admin eslatma</h2>
                        <p style="color:#cbd5e1; line-height:1.8;">
                            Ushbu admin panel orqali o‘quvchi qo‘shish, ro‘yxatni ko‘rish,
                            qidirish va portfolio sahifalariga o‘tish mumkin. Oddiy foydalanuvchilar
                            faqat public portfolio sahifalarini ko‘radi.
                        </p>
                        <br>
                        <a class="btn btn-secondary" href="/portfolio">Public portfolio sahifasini ochish</a>
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
        filtered=filtered,
        total_students=total_students,
        total_works=total_works,
        active_students=active_students,
        avg_score=avg_score,
        q=q,
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
    score = request.form.get("score")
    image = request.form.get("image")
    description = request.form.get("description")

    if not image:
        image = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1000&q=80"

    if not description:
        description = f"{name}ning yillik o‘quv faoliyati, loyiha ishlari va portfolio natijalari ushbu sahifada jamlanadi."

    try:
        works = int(works)
    except:
        works = 0

    try:
        score = int(score)
    except:
        score = 80

    new_id = max([s["id"] for s in students]) + 1 if students else 1

    students.append({
        "id": new_id,
        "name": name,
        "grade": grade,
        "direction": direction,
        "status": status,
        "works": works,
        "score": score,
        "image": image,
        "description": description,
        "projects": [
            "Yillik portfolio materiali",
            "Ijodiy yoki tadqiqot ishi",
            "O‘quv natijalari jamlanmasi"
        ]
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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
