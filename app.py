from flask import Flask, render_template_string, request, redirect, url_for, session

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


CSS = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, "Segoe UI", sans-serif;
    background: #f1f4f7;
    color: #111;
}

a {
    text-decoration: none;
    color: inherit;
}

.navbar {
    height: 118px;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 46px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    position: sticky;
    top: 0;
    z-index: 99;
}

.logo {
    display: flex;
    align-items: center;
    gap: 18px;
}

.logo-box {
    width: 72px;
    height: 72px;
    background: #5471c8;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    font-size: 21px;
    line-height: 18px;
    font-weight: 500;
}

.logo-box .e {
    font-size: 46px;
    line-height: 38px;
}

.logo-text {
    font-size: 33px;
    color: #5471c8;
    font-weight: 800;
    line-height: 1.15;
}

.nav-links {
    display: flex;
    gap: 28px;
    align-items: center;
    font-size: 20px;
    font-weight: 500;
    white-space: nowrap;
}

.nav-links a:hover {
    color: #5471c8;
}

.hero {
    min-height: 650px;
    background:
        linear-gradient(rgba(24, 52, 78, 0.72), rgba(24, 52, 78, 0.72)),
        url("https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1800&q=80");
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    padding-left: 92px;
}

.hero-content {
    color: white;
    max-width: 720px;
}

.hero-content h1 {
    font-size: 78px;
    line-height: 1.1;
    margin-bottom: 55px;
    font-weight: 800;
}

.hero-content p {
    font-size: 24px;
    line-height: 1.35;
    font-weight: 800;
    text-align: justify;
    max-width: 680px;
}

.floating-card {
    max-width: 1120px;
    margin: -95px auto 50px;
    background: #5b78d1;
    border-radius: 9px;
    min-height: 250px;
    box-shadow: 0 13px 24px rgba(0,0,0,0.28);
    display: grid;
    grid-template-columns: 1fr 180px 180px 180px;
    gap: 34px;
    align-items: center;
    padding: 45px 70px;
    color: white;
    position: relative;
    z-index: 2;
}

.floating-card h2 {
    font-size: 36px;
    line-height: 1.25;
}

.mini-card {
    height: 145px;
    border-radius: 9px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 9px;
    text-align: center;
    font-weight: 800;
    font-size: 16px;
}

.mini-card .ico {
    font-size: 50px;
}

.cyan {
    background: #11c5c8;
}

.green {
    background: #c9e76a;
}

.red {
    background: #ff7070;
}

.section {
    max-width: 1120px;
    margin: 0 auto;
    padding: 45px 20px;
}

.section-label {
    display: inline-block;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 8px;
    border-bottom: 2px solid #06c4c6;
    padding-bottom: 9px;
}

.section-title {
    font-size: 43px;
    margin: 8px 0 24px;
    font-weight: 900;
}

.about-grid {
    display: grid;
    grid-template-columns: 1.25fr .75fr;
    gap: 55px;
    align-items: center;
}

.about-text p {
    font-size: 20px;
    line-height: 1.55;
    text-align: justify;
    margin-bottom: 22px;
}

.about-img {
    text-align: center;
}

.about-img img {
    width: 360px;
    max-width: 100%;
}

.btn {
    display: inline-block;
    border: none;
    cursor: pointer;
    padding: 12px 35px;
    border-radius: 8px;
    background: #08c6c9;
    color: white;
    font-size: 18px;
    font-weight: 700;
}

.purpose {
    max-width: 1080px;
    margin: 35px auto 25px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: #5b78d1;
    color: white;
    border-radius: 9px;
    overflow: hidden;
}

.purpose-box {
    padding: 34px 52px;
}

.purpose-box:first-child {
    background: rgba(45, 73, 160, 0.25);
}

.purpose-box h2 {
    font-size: 31px;
    margin-bottom: 18px;
}

.purpose-box p {
    font-size: 18px;
    line-height: 1.35;
    text-align: justify;
    font-weight: 600;
    margin-bottom: 18px;
}

.advantages {
    display: grid;
    grid-template-columns: 1fr 1fr;
    min-height: 620px;
    margin-top: 25px;
}

.adv-left {
    background: url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1400&q=80");
    background-size: cover;
    background-position: center;
}

.adv-right {
    background:
        linear-gradient(rgba(84, 113, 200, 0.80), rgba(84, 113, 200, 0.80)),
        url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1400&q=80");
    background-size: cover;
    background-position: center;
    padding: 70px 65px;
    color: white;
}

.adv-right h2 {
    font-size: 46px;
    margin-bottom: 25px;
}

.adv-item {
    display: grid;
    grid-template-columns: 110px 1fr;
    align-items: center;
    gap: 24px;
    margin-bottom: 28px;
}

.adv-icon {
    font-size: 76px;
    color: #04d0d3;
}

.adv-item h3 {
    font-size: 29px;
    margin-bottom: 8px;
}

.adv-item p {
    font-size: 17px;
    line-height: 1.4;
}

.partners {
    background: #eef2f5;
    padding: 38px 0 50px;
}

.partners-inner {
    max-width: 1160px;
    margin: 0 auto;
    padding: 0 20px;
}

.partner-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 35px;
    align-items: center;
    margin-top: 25px;
}

.partner-logo {
    height: 150px;
    background: white;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: #5471c8;
    font-size: 22px;
    text-align: center;
    font-weight: 900;
    border: 4px solid #d9e1f2;
}

.feedback {
    min-height: 520px;
    background:
        linear-gradient(rgba(67, 125, 176, 0.62), rgba(67, 125, 176, 0.62)),
        url("https://images.unsplash.com/photo-1452860606245-08befc0ff44b?auto=format&fit=crop&w=1800&q=80");
    background-size: cover;
    background-position: center;
    color: white;
    padding: 50px 0;
}

.feedback-inner {
    max-width: 1160px;
    margin: 0 auto;
    padding: 0 20px;
}

.feedback h2 {
    font-size: 43px;
    margin-top: 8px;
}

.feedback-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    margin-top: 80px;
}

.feedback-card {
    display: grid;
    grid-template-columns: 130px 1fr;
    gap: 22px;
    align-items: center;
}

.feedback-card img {
    width: 112px;
    height: 112px;
    object-fit: cover;
    border-radius: 12px;
}

.feedback-card p {
    font-size: 18px;
    line-height: 1.35;
    margin-bottom: 20px;
}

.feedback-card h3 {
    font-size: 19px;
    margin-bottom: 8px;
}

.social {
    background: #eef2f5;
    padding: 40px 20px 55px;
    text-align: center;
}

.social h2 {
    font-size: 32px;
    margin-bottom: 30px;
}

.social-grid {
    max-width: 1120px;
    margin: auto;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 48px;
}

.social-card {
    background: white;
    height: 75px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 22px;
    font-size: 24px;
    font-weight: 800;
    box-shadow: 0 9px 18px rgba(0,0,0,0.16);
}

.social-icon {
    font-size: 42px;
}

.footer {
    background: #5b78d1;
    color: white;
    min-height: 275px;
    padding: 40px 45px;
}

.footer-inner {
    max-width: 1220px;
    margin: auto;
    display: grid;
    grid-template-columns: 1.2fr 1fr 1.2fr 1.6fr;
    gap: 50px;
    align-items: start;
}

.footer-logo {
    display: flex;
    gap: 22px;
    align-items: flex-start;
}

.footer-text {
    font-size: 18px;
    line-height: 1.28;
    text-align: justify;
}

.footer h3 {
    font-size: 22px;
    margin-bottom: 13px;
    border-bottom: 1px solid white;
    padding-bottom: 6px;
    display: inline-block;
}

.footer p,
.footer li {
    font-size: 16px;
    line-height: 1.7;
    list-style: none;
}

.map-box {
    height: 160px;
    background: #dbeafe;
    border: 4px solid white;
    display: grid;
    place-items: center;
    color: #1e3a8a;
    font-weight: 800;
    text-align: center;
}

.page-head {
    background: #5b78d1;
    color: white;
    padding: 58px 20px;
    text-align: center;
}

.page-head h1 {
    font-size: 46px;
}

.portfolio-grid {
    max-width: 1120px;
    margin: 45px auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 28px;
}

.portfolio-card {
    background: white;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 8px 22px rgba(0,0,0,0.14);
}

.portfolio-card img {
    width: 100%;
    height: 220px;
    object-fit: cover;
}

.card-body {
    padding: 22px;
}

.card-body h3 {
    font-size: 24px;
    margin-bottom: 10px;
}

.card-body p {
    font-size: 16px;
    line-height: 1.5;
    margin-bottom: 14px;
}

.badge {
    display: inline-block;
    background: #e8efff;
    color: #5471c8;
    padding: 6px 10px;
    border-radius: 20px;
    font-weight: 700;
    margin: 3px;
    font-size: 13px;
}

.login-wrap {
    min-height: 620px;
    display: grid;
    place-items: center;
    padding: 40px 20px;
}

.login-card,
.admin-panel {
    background: white;
    border-radius: 14px;
    box-shadow: 0 10px 28px rgba(0,0,0,.18);
    padding: 32px;
}

.login-card {
    width: 430px;
    max-width: 100%;
}

.login-card h2 {
    font-size: 32px;
    margin-bottom: 10px;
    color: #5471c8;
}

.form-group {
    margin-bottom: 16px;
}

.form-group label {
    display: block;
    font-weight: 800;
    margin-bottom: 7px;
}

input,
select,
textarea {
    width: 100%;
    padding: 13px 14px;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    font-size: 15px;
}

textarea {
    min-height: 100px;
}

.admin-wrap {
    max-width: 1200px;
    margin: 40px auto;
    padding: 0 20px;
}

.admin-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 22px;
    margin-bottom: 25px;
}

.stat {
    background: #5b78d1;
    color: white;
    border-radius: 12px;
    padding: 25px;
}

.stat h3 {
    font-size: 17px;
    margin-bottom: 10px;
}

.stat strong {
    font-size: 34px;
}

.admin-grid {
    display: grid;
    grid-template-columns: 1.2fr .8fr;
    gap: 24px;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th,
td {
    border-bottom: 1px solid #e5e7eb;
    padding: 13px;
    text-align: left;
}

th {
    background: #eef2ff;
    color: #334155;
}

.alert {
    padding: 12px 15px;
    background: #dcfce7;
    color: #166534;
    border-radius: 8px;
    margin-bottom: 15px;
    font-weight: 700;
}

@media(max-width: 1000px) {
    .navbar {
        height: auto;
        padding: 18px;
        flex-direction: column;
        gap: 15px;
    }

    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
        font-size: 16px;
        gap: 14px;
    }

    .hero {
        padding: 80px 28px;
    }

    .hero-content h1 {
        font-size: 48px;
    }

    .floating-card,
    .about-grid,
    .purpose,
    .advantages,
    .feedback-grid,
    .footer-inner,
    .admin-grid {
        grid-template-columns: 1fr;
    }

    .floating-card {
        margin: 20px;
        padding: 30px;
    }

    .partner-grid,
    .social-grid,
    .portfolio-grid,
    .admin-stats {
        grid-template-columns: 1fr 1fr;
    }
}

@media(max-width: 650px) {
    .partner-grid,
    .social-grid,
    .portfolio-grid,
    .admin-stats {
        grid-template-columns: 1fr;
    }

    .logo-text {
        font-size: 25px;
    }
}
</style>
"""


def navbar():
    return """
    <div class="navbar">
        <a class="logo" href="/">
            <div class="logo-box">
                <div class="e">e</div>
                <div>portfel</div>
            </div>
            <div class="logo-text">Elektron<br>portfel</div>
        </a>
        <div class="nav-links">
            <a href="/personal">Shaxsiy ma’lumotlar</a>
            <a href="/portfolio">Pedagogik portfel</a>
            <a href="/achievements">Akademik yutuqlar</a>
            <a href="/reflection">Refleksiya va o‘zini baholash</a>
            <a href="/about">Biz haqimizda</a>
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
        <title>Elektron portfel</title>
        {{ css|safe }}
    </head>
    <body>
        {{ navbar|safe }}

        <section class="hero">
            <div class="hero-content">
                <h1>Elektron<br>portfel</h1>
                <p>
                    Ushbu platformada talabaning o‘quv natijalari, loyihalari,
                    ijodiy ishlari, refleksiyalari va kompetensiyalari raqamli tarzda
                    jamlanib, tahlil qilinadi, ham baholash jarayonlari qo‘llab-quvvatlanadi.
                </p>
            </div>
        </section>

        <section class="floating-card">
            <h2>Shaxsiy raqamli<br>o‘quv portfeli</h2>
            <div class="mini-card cyan">
                <div class="ico">🌐</div>
                <div>Xorijiy<br>tajriba</div>
            </div>
            <div class="mini-card green">
                <div class="ico">👩‍🏫</div>
                <div>Ta’limda<br>kreativlik</div>
            </div>
            <div class="mini-card red">
                <div class="ico">⚙️</div>
                <div>Mustaqil<br>tadqiqotchilik</div>
            </div>
        </section>

        <section class="section" id="about">
            <div class="about-grid">
                <div class="about-text">
                    <div class="section-label">Ma'lumot</div>
                    <h2 class="section-title">Platforma haqida</h2>
                    <p>
                        E-portfel – talabaning o‘quv jarayonidagi natijalari, kompetensiyalari
                        va ijodiy ishlari raqamli muhitda jamlanadigan shaxsiy elektron to‘plamdir.
                        U o‘quv faoliyatini individuallashtirish, o‘z-o‘zini baholash va rivojlanishni
                        tahlil qilishga yordam beradi.
                    </p>
                    <p>
                        E-portfel dars ishlanmalari, loyihalar, refleksiyalar va boshqa raqamli
                        materiallarni bir tizimda to‘plab, talabaning kompetensiyalarini aniq
                        namoyish etadi hamda o‘qituvchi uchun baholashning samarali vositasiga aylanadi.
                    </p>
                    <a class="btn" href="/about">Ko‘proq</a>
                </div>
                <div class="about-img">
                    <img src="https://cdn-icons-png.flaticon.com/512/3135/3135755.png">
                </div>
            </div>
        </section>

        <section class="purpose">
            <div class="purpose-box">
                <h2>Platformaning maqsadi</h2>
                <p>
                    Talabalarning o‘quv va kasbiy rivojlanish jarayonida hosil qilgan raqamli
                    artefaktlarini tizimli yig‘ish, baholash va reflektiv tahlil qilish imkonini yaratish.
                    Platforma talabaning shaxsiy o‘sishini monitoring qilish, kompetensiyalarni dalillarga
                    asoslangan baholash hamda mustaqil ta’lim, kreativlik va metakognitiv ko‘nikmalarni
                    rivojlantirish uchun ilmiy asoslangan raqamli muhitni ta’minlaydi.
                </p>
                <a class="btn" href="/about">Ko‘proq</a>
            </div>
            <div class="purpose-box">
                <h2>Platformaning vazifasi</h2>
                <p>
                    Talabalarning raqamli artefaktlarini tizimli yig‘ish, ularning kompetensiyalarini
                    dalillarga asoslangan baholash, o‘z-o‘zini reflektiv tahlil qilish ko‘nikmalarini
                    rivojlantirish va kasbiy portfel shakllantirishni ta’minlash.
                </p>
                <a class="btn" href="/portfolio">Ko‘proq</a>
            </div>
        </section>

        <section class="advantages">
            <div class="adv-left"></div>
            <div class="adv-right">
                <h2>Afzalliklari</h2>

                <div class="adv-item">
                    <div class="adv-icon">📄</div>
                    <div>
                        <h3>Dalillilik</h3>
                        <p>Kompetensiyalarni real artefaktlar orqali ishonchli baholashni ta’minlaydi.</p>
                    </div>
                </div>

                <div class="adv-item">
                    <div class="adv-icon">📈</div>
                    <div>
                        <h3>Rivojlanish monitoringi</h3>
                        <p>Talabalarni yutuqlarining dinamikasini tizimli kuzatish imkonini yaratadi.</p>
                    </div>
                </div>

                <div class="adv-item">
                    <div class="adv-icon">👥</div>
                    <div>
                        <h3>Refleksiya va metakognitsiya</h3>
                        <p>O‘z-o‘zini tahlil qilish va o‘qishni boshqarish ko‘nikmalarini rivojlantiradi.</p>
                    </div>
                </div>

                <div class="adv-item">
                    <div class="adv-icon">📚</div>
                    <div>
                        <h3>Raqamli savodxonlik</h3>
                        <p>Talabaning zamonaviy texnologiyalar bilan ishlash kompetensiyasini mustahkamlaydi.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="partners">
            <div class="partners-inner">
                <div class="section-label">Hamkorlar</div>
                <h2 class="section-title">Hamkor tashkilotlar</h2>
                <div class="partner-grid">
                    <div class="partner-logo">OTFIV</div>
                    <div class="partner-logo">NamDPI</div>
                    <div class="partner-logo">Andijon<br>DPI</div>
                    <div class="partner-logo">Qarshi<br>DU</div>
                    <div class="partner-logo">CHDPU</div>
                </div>
            </div>
        </section>

        <section class="feedback">
            <div class="feedback-inner">
                <div class="section-label">Fikrlar</div>
                <h2>Foydalanuvchilar fikri</h2>

                <div class="feedback-grid">
                    <div class="feedback-card">
                        <img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80">
                        <div>
                            <p>
                                E-portfel platformasi ta’lim sifatini oshirib, shaffof baholash,
                                refleksiya va kasbiy rivojlanishni qo‘llab-quvvatlaydigan samarali
                                raqamli vositadir.
                            </p>
                            <h3>Atamuratov R.</h3>
                            <span>Toshkent davlat pedagogika universiteti dotsenti</span>
                        </div>
                    </div>

                    <div class="feedback-card">
                        <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80">
                        <div>
                            <p>
                                E-portfel ta’lim jarayonini interaktiv qilib, refleksiya,
                                metakognitsiya va kasbiy rivojlanishni qo‘llab-quvvatlovchi
                                samarali raqamli muhitdir.
                            </p>
                            <h3>Saparboyeva Z.</h3>
                            <span>CHDPU. Tarix fakulteti talabasi</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="social">
            <h2>Bizni kuzating</h2>
            <div class="social-grid">
                <div class="social-card"><span class="social-icon">▶️</span> YouTube</div>
                <div class="social-card"><span class="social-icon">✈️</span> Telegram</div>
                <div class="social-card"><span class="social-icon">📷</span> Instagram</div>
                <div class="social-card"><span class="social-icon">f</span> Facebook</div>
            </div>
        </section>

        {{ footer|safe }}
    </body>
    </html>
    """
    return render_template_string(html, css=CSS, navbar=navbar(), footer=footer())


def footer():
    return """
    <footer class="footer">
        <div class="footer-inner">
            <div class="footer-logo">
                <div class="logo-box">
                    <div class="e">e</div>
                    <div>portfel</div>
                </div>
                <div class="footer-text">
                    “Elektron portfel” platformasida e’lon qilingan materiallardan nusxa ko‘chirish,
                    tarqatish va boshqa shakllarda foydalanish faqat tahririyat yozma roziligi bilan
                    amalga oshirilishi mumkin.
                </div>
            </div>

            <div>
                <h3>Menyu</h3>
                <ul>
                    <li>Shaxsiy ma’lumotlar</li>
                    <li>Pedagogik portfel</li>
                    <li>Akademik yutuqlar</li>
                    <li>Refleksiya</li>
                </ul>
            </div>

            <div>
                <h3>Aloqa uchun</h3>
                <p>☎ +998939264206</p>
                <p>✉ yuldashevjavohir2018@gmail.com</p>
                <p>🌐 www.eportfel.uz</p>
                <p>📍 Namangan shahar Obi-Hayot MFY</p>
            </div>

            <div class="map-box">
                Google Map<br>Namangan shahri
            </div>
        </div>
    </footer>
    """


@app.route("/portfolio")
def portfolio():
    q = request.args.get("q", "").lower().strip()
    if q:
        filtered = [s for s in students if q in s["name"].lower() or q in s["direction"].lower() or q in s["grade"].lower()]
    else:
        filtered = students

    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Pedagogik portfel</title>
        {{ css|safe }}
    </head>
    <body>
        {{ navbar|safe }}
        <div class="page-head">
            <h1>Pedagogik portfel</h1>
            <p>Talabalarning raqamli o‘quv portfellari</p>
        </div>

        <div class="section">
            <form method="GET" style="display:grid;grid-template-columns:1fr auto;gap:12px;margin-bottom:25px;">
                <input name="q" value="{{ q }}" placeholder="Ism, sinf yoki yo‘nalish bo‘yicha qidirish...">
                <button class="btn" type="submit">Qidirish</button>
            </form>
        </div>

        <div class="portfolio-grid">
            {% for s in filtered %}
            <div class="portfolio-card">
                <img src="{{ s.image }}">
                <div class="card-body">
                    <h3>{{ s.name }}</h3>
                    <span class="badge">{{ s.grade }}</span>
                    <span class="badge">{{ s.direction }}</span>
                    <span class="badge">{{ s.score }} ball</span>
                    <p>{{ s.description }}</p>
                    <a class="btn" href="/student/{{ s.id }}">Batafsil</a>
                </div>
            </div>
            {% endfor %}
        </div>

        {{ footer|safe }}
    </body>
    </html>
    """
    return render_template_string(html, css=CSS, navbar=navbar(), footer=footer(), filtered=filtered, q=q)


@app.route("/student/<int:student_id>")
def student(student_id):
    s = next((x for x in students if x["id"] == student_id), None)
    if not s:
        return redirect(url_for("portfolio"))

    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>{{ s.name }}</title>
        {{ css|safe }}
    </head>
    <body>
        {{ navbar|safe }}
        <div class="page-head">
            <h1>{{ s.name }}</h1>
            <p>{{ s.direction }}</p>
        </div>

        <section class="section">
            <div class="about-grid">
                <div>
                    <img src="{{ s.image }}" style="width:100%;border-radius:14px;">
                </div>
                <div class="about-text">
                    <div class="section-label">Shaxsiy portfel</div>
                    <h2 class="section-title">{{ s.name }}</h2>
                    <p>{{ s.description }}</p>
                    <p><b>Sinf:</b> {{ s.grade }}</p>
                    <p><b>Status:</b> {{ s.status }}</p>
                    <p><b>Umumiy ball:</b> {{ s.score }}</p>
                    <h3 style="font-size:25px;margin:20px 0;">Portfolio ishlari</h3>
                    {% for p in s.projects %}
                    <p>📌 {{ p }}</p>
                    {% endfor %}
                    <a class="btn" href="/portfolio">Ortga</a>
                </div>
            </div>
        </section>

        {{ footer|safe }}
    </body>
    </html>
    """
    return render_template_string(html, css=CSS, navbar=navbar(), footer=footer(), s=s)


@app.route("/personal")
def personal():
    return simple_page("Shaxsiy ma’lumotlar", "Bu bo‘limda talabaning shaxsiy ma’lumotlari, ta’lim yo‘nalishi va umumiy portfel ma’lumotlari joylashtiriladi.")


@app.route("/achievements")
def achievements():
    return simple_page("Akademik yutuqlar", "Bu bo‘limda talabaning sertifikatlari, tanlov natijalari, ilmiy va ijodiy yutuqlari jamlanadi.")


@app.route("/reflection")
def reflection():
    return simple_page("Refleksiya va o‘zini baholash", "Bu bo‘limda talabaning o‘zini baholashi, reflektiv yozuvlari va rivojlanish monitoringi keltiriladi.")


@app.route("/about")
def about():
    return simple_page("Biz haqimizda", "Elektron portfel platformasi ta’lim jarayonini raqamlashtirish, shaffof baholash va talaba rivojlanishini monitoring qilishga xizmat qiladi.")


def simple_page(title, text):
    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        {{ css|safe }}
    </head>
    <body>
        {{ navbar|safe }}
        <div class="page-head">
            <h1>{{ title }}</h1>
        </div>
        <section class="section">
            <div class="about-text">
                <div class="section-label">Ma'lumot</div>
                <h2 class="section-title">{{ title }}</h2>
                <p>{{ text }}</p>
                <a class="btn" href="/">Bosh sahifa</a>
            </div>
        </section>
        {{ footer|safe }}
    </body>
    </html>
    """
    return render_template_string(html, css=CSS, navbar=navbar(), footer=footer(), title=title, text=text)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "12345":
            session["admin"] = True
            return redirect(url_for("admin"))
        error = "Login yoki parol noto‘g‘ri"

    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Admin</title>
        {{ css|safe }}
    </head>
    <body>
        {{ navbar|safe }}
        <div class="login-wrap">
            <form class="login-card" method="POST">
                <h2>Admin panel</h2>
                <p>Platformani boshqarish uchun tizimga kiring.</p>
                {% if error %}<div class="alert" style="background:#fee2e2;color:#991b1b;">{{ error }}</div>{% endif %}
                <div class="form-group">
                    <label>Login</label>
                    <input name="username" placeholder="admin" required>
                </div>
                <div class="form-group">
                    <label>Parol</label>
                    <input name="password" type="password" placeholder="12345" required>
                </div>
                <button class="btn" style="width:100%;">Kirish</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, css=CSS, navbar=navbar(), error=error)


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    total_students = len(students)
    total_works = sum(s["works"] for s in students)
    active = len([s for s in students if s["status"] == "Faol"])
    avg = round(sum(s["score"] for s in students) / len(students)) if students else 0

    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Admin panel</title>
        {{ css|safe }}
    </head>
    <body>
        {{ navbar|safe }}

        <div class="page-head">
            <h1>Admin panel</h1>
            <p>Elektron portfel platformasini boshqarish</p>
        </div>

        <div class="admin-wrap">
            {% if request.args.get('success') %}
            <div class="alert">Yangi o‘quvchi qo‘shildi.</div>
            {% endif %}
            {% if request.args.get('deleted') %}
            <div class="alert">O‘quvchi o‘chirildi.</div>
            {% endif %}

            <div class="admin-stats">
                <div class="stat"><h3>Jami talabalar</h3><strong>{{ total_students }}</strong></div>
                <div class="stat"><h3>Jami ishlar</h3><strong>{{ total_works }}</strong></div>
                <div class="stat"><h3>Faol portfellar</h3><strong>{{ active }}</strong></div>
                <div class="stat"><h3>O‘rtacha ball</h3><strong>{{ avg }}</strong></div>
            </div>

            <div class="admin-grid">
                <div class="admin-panel">
                    <h2 style="margin-bottom:18px;">Talabalar ro‘yxati</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Ism</th>
                                <th>Sinf</th>
                                <th>Yo‘nalish</th>
                                <th>Ball</th>
                                <th>Amal</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for s in students %}
                            <tr>
                                <td>{{ s.name }}</td>
                                <td>{{ s.grade }}</td>
                                <td>{{ s.direction }}</td>
                                <td>{{ s.score }}</td>
                                <td>
                                    <a class="btn" href="/student/{{ s.id }}">Ko‘rish</a>
                                    <form method="POST" action="/admin/delete/{{ s.id }}" style="display:inline;">
                                        <button class="btn" style="background:#ef4444;">O‘chirish</button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <div class="admin-panel">
                    <h2 style="margin-bottom:18px;">Yangi talaba qo‘shish</h2>
                    <form method="POST" action="/admin/add">
                        <div class="form-group">
                            <label>Ism-familiya</label>
                            <input name="name" required>
                        </div>
                        <div class="form-group">
                            <label>Sinf yoki guruh</label>
                            <input name="grade" required>
                        </div>
                        <div class="form-group">
                            <label>Yo‘nalish</label>
                            <select name="direction">
                                <option>Shaxsiy ma’lumotlar</option>
                                <option>Pedagogik portfel</option>
                                <option>Akademik yutuqlar</option>
                                <option>Refleksiya</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Ishlar soni</label>
                            <input name="works" type="number" value="0">
                        </div>
                        <div class="form-group">
                            <label>Ball</label>
                            <input name="score" type="number" value="80">
                        </div>
                        <div class="form-group">
                            <label>Rasm URL</label>
                            <input name="image">
                        </div>
                        <div class="form-group">
                            <label>Tavsif</label>
                            <textarea name="description"></textarea>
                        </div>
                        <button class="btn" style="width:100%;">Saqlash</button>
                    </form>
                </div>
            </div>

            <br>
            <a class="btn" href="/admin/logout">Chiqish</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, css=CSS, navbar=navbar(), students=students,
                                  total_students=total_students, total_works=total_works,
                                  active=active, avg=avg, request=request)


@app.route("/admin/add", methods=["POST"])
def admin_add():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    name = request.form.get("name")
    grade = request.form.get("grade")
    direction = request.form.get("direction")
    works = request.form.get("works")
    score = request.form.get("score")
    image = request.form.get("image")
    description = request.form.get("description")

    if not image:
        image = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1000&q=80"

    if not description:
        description = f"{name}ning elektron portfel materiallari ushbu sahifada jamlanadi."

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
        "status": "Faol",
        "works": works,
        "score": score,
        "image": image,
        "description": description,
        "projects": ["Raqamli artefakt", "Refleksiya", "Akademik natija"]
    })

    return redirect(url_for("admin", success=1))


@app.route("/admin/delete/<int:student_id>", methods=["POST"])
def admin_delete(student_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    global students
    students = [s for s in students if s["id"] != student_id]
    return redirect(url_for("admin", deleted=1))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
