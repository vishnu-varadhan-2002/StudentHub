"""
StudentHub - All-in-One Student Portal
CAPOL510 - IS Development Laboratory (Mini Project)

Dual-database design:
  * On your laptop  -> MySQL  (UI matches your DBeaver 'studenthub' database)
  * On Vercel        -> SQLite (self-contained, auto-seeded, no server needed)

The switch is automatic: Vercel sets the env var VERCEL=1, so there we fall
back to SQLite. Locally it uses MySQL. You can force SQLite locally for testing
with:  set USE_SQLITE=1

Local setup:
  1. MySQL running + run setup_db_mysql.py once.
  2. Put your MySQL password in MYSQL_PASSWORD below (default 'root').
  3. pip install -r requirements.txt ; python app.py ; login student / 1234
"""

import os
import tempfile
from datetime import datetime
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, send_from_directory)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "studenthub-mini-project"

# ---- choose the database backend ----
ON_VERCEL = os.environ.get("VERCEL") == "1"
USE_MYSQL = (not ON_VERCEL) and os.environ.get("USE_SQLITE") != "1"

# ---- MySQL settings (used locally) ----
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root")
MYSQL_DB = os.environ.get("MYSQL_DB", "studenthub")

# ---- SQLite settings (used on Vercel) ----
SQLITE_PATH = os.path.join(tempfile.gettempdir() if ON_VERCEL else ".", "studenthub.db")

# ---- uploads (writable temp on Vercel) ----
UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "uploads") if ON_VERCEL else os.path.join("static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==================================================================
#  Tiny data-access layer that works with BOTH MySQL and SQLite
# ==================================================================
def get_conn():
    if USE_MYSQL:
        import pymysql
        return pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD,
                               database=MYSQL_DB, cursorclass=pymysql.cursors.DictCursor,
                               autocommit=True)
    import sqlite3
    conn = sqlite3.connect(SQLITE_PATH)
    # return rows as plain dicts so templates + computations work the same way
    conn.row_factory = lambda cur, row: {d[0]: row[i] for i, d in enumerate(cur.description)}
    return conn


def _q(sql):
    """MySQL uses %s placeholders; SQLite uses ?. Translate when needed."""
    return sql if USE_MYSQL else sql.replace("%s", "?")


def fetch_all(sql, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(_q(sql), params)
    rows = cur.fetchall()
    conn.close()
    return rows


def fetch_one(sql, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(_q(sql), params)
    row = cur.fetchone()
    conn.close()
    return row


def execute(sql, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(_q(sql), params)
    conn.commit()
    conn.close()


# ==================================================================
#  SQLite bootstrap (Vercel) - create + seed the same demo data
# ==================================================================
SEED = {
    "users": ("(username, password, role)", [
        ("student", "1234", "student"),
        ("admin", "admin123", "admin"),
    ]),
    "students": ("(roll_no, name, program, email, phone, dob, blood, gender, address, guardian, mentor, admission_year)", [
        ("126003100", "Vishnu Kumar", "MCA (Online) - Semester 3", "vishnu@sastra.edu",
         "+91 98765 43210", "12 March 2002", "O+", "Male",
         "Thanjavur, Tamil Nadu, India", "Mr. Ramesh Kumar", "Dr. S. Priya", "2024"),
    ]),
    "attendance": ("(roll_no, subject, attended, total)", [
        ("126003100", "Information Security", 44, 48),
        ("126003100", "Cloud Computing", 40, 46),
        ("126003100", "Machine Learning", 38, 45),
        ("126003100", "Software Project Management", 42, 44),
        ("126003100", "IS Development Laboratory", 30, 32),
    ]),
    "exam_scores": ("(roll_no, subject, internal, external, grade)", [
        ("126003100", "Information Security", 28, 61, "A"),
        ("126003100", "Cloud Computing", 26, 58, "A"),
        ("126003100", "Machine Learning", 24, 55, "B+"),
        ("126003100", "Software Project Management", 29, 63, "A+"),
    ]),
    "practical_scores": ("(roll_no, lab, marks, grade)", [
        ("126003100", "IS Development Laboratory", 92, "A+"),
        ("126003100", "Cloud Computing Lab", 88, "A"),
        ("126003100", "Machine Learning Lab", 85, "A"),
    ]),
    "announcements": ("(category, title, posted_on, body)", [
        ("General", "Library timings extended", "02 Jul 2026", "The central library will now remain open till 9:00 PM on weekdays."),
        ("General", "New Wi-Fi network live", "28 Jun 2026", "Connect to 'SASTRA-Campus-5G' using your student credentials."),
        ("General", "ID card renewal", "20 Jun 2026", "Students must renew their ID cards at the admin office before 15 Jul."),
        ("Exam", "End-Semester Exam Schedule Released", "01 Jul 2026", "Semester 3 theory exams begin from 20 Jul 2026. Check the timetable."),
        ("Exam", "Practical Exam Dates", "26 Jun 2026", "Lab practical exams are scheduled between 12 Jul and 18 Jul 2026."),
        ("Exam", "Hall Ticket Download", "24 Jun 2026", "Hall tickets can be downloaded from 10 Jul. Clear pending fees first."),
    ]),
    "updates": ("(category, title, posted_on, body)", [
        ("Campus", "New Innovation Lab inaugurated", "03 Jul 2026", "A state-of-the-art AI and IoT lab has opened in Block C."),
        ("Campus", "Green campus drive", "29 Jun 2026", "Tree plantation programme this weekend. Volunteers welcome."),
        ("Events", "Tech Symposium Cognizance 2026", "15 Jul 2026", "National level technical symposium with workshops and prizes."),
        ("Events", "Guest Lecture on Cyber Security", "10 Jul 2026", "Industry expert session on ethical hacking. Register now."),
        ("Culturals", "Annual Cultural Fest Kalotsav", "22 Jul 2026", "Music, dance and drama competitions. Registrations open."),
        ("Culturals", "Battle of Bands", "18 Jul 2026", "Show your musical talent. Sign up at the cultural desk."),
        ("Sports", "Inter-Department Cricket Tournament", "20 Jul 2026", "Form your teams and register before 12 Jul."),
        ("Sports", "Annual Athletic Meet", "25 Jul 2026", "Track and field events at the main stadium."),
    ]),
    "fees": ("(name, category, amount, status, receipt_no, paid_on)", [
        ("Tuition Fee", "Academic", 45000, "Pending", None, None),
        ("Exam Fee", "Academic", 2500, "Pending", None, None),
        ("Bus Fee", "Transport", 18000, "Paid", "SH-1003", "15 Jun 2026"),
        ("Canteen Fee", "Food", 12000, "Pending", None, None),
        ("Hostel Fee", "Boarding", 35000, "Paid", "SH-1005", "10 Jun 2026"),
    ]),
    "projects": ("(title, subject, filename, uploaded_on)", [
        ("StudentHub Portal", "IS Development Lab", "studenthub.zip", "01 Jul 2026"),
        ("Cloud Notes App", "Cloud Computing", "cloudnotes.pdf", "28 Jun 2026"),
    ]),
}

SQLITE_SCHEMA = {
    "users": "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, role TEXT",
    "students": "id INTEGER PRIMARY KEY AUTOINCREMENT, roll_no TEXT, name TEXT, program TEXT, email TEXT, phone TEXT, dob TEXT, blood TEXT, gender TEXT, address TEXT, guardian TEXT, mentor TEXT, admission_year TEXT",
    "attendance": "id INTEGER PRIMARY KEY AUTOINCREMENT, roll_no TEXT, subject TEXT, attended INTEGER, total INTEGER",
    "exam_scores": "id INTEGER PRIMARY KEY AUTOINCREMENT, roll_no TEXT, subject TEXT, internal INTEGER, external INTEGER, grade TEXT",
    "practical_scores": "id INTEGER PRIMARY KEY AUTOINCREMENT, roll_no TEXT, lab TEXT, marks INTEGER, grade TEXT",
    "announcements": "id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, title TEXT, posted_on TEXT, body TEXT",
    "updates": "id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, title TEXT, posted_on TEXT, body TEXT",
    "fees": "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, amount INTEGER, status TEXT DEFAULT 'Pending', receipt_no TEXT, paid_on TEXT",
    "projects": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, subject TEXT, filename TEXT, uploaded_on TEXT",
}


def init_sqlite():
    """Create and seed the SQLite tables (only used when not on MySQL)."""
    import sqlite3
    conn = sqlite3.connect(SQLITE_PATH)
    cur = conn.cursor()
    for table, cols in SQLITE_SCHEMA.items():
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({cols})")
        if cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0:
            col_list, rows = SEED[table]
            ph = ", ".join(["?"] * len(rows[0]))
            cur.executemany(f"INSERT INTO {table} {col_list} VALUES ({ph})", rows)
    conn.commit()
    conn.close()


if not USE_MYSQL:
    init_sqlite()


# ==================================================================
#  Auth
# ==================================================================
def login_required(view):
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    wrapper.__name__ = view.__name__
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = fetch_one("SELECT * FROM users WHERE username=%s AND password=%s",
                         (request.form.get("username"), request.form.get("password")))
        if user:
            session["user"] = user["username"]
            return redirect(url_for("dashboard"))
        flash("Invalid Credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ==================================================================
#  Dashboard
# ==================================================================
@app.route("/")
@login_required
def dashboard():
    profile = fetch_one("""SELECT roll_no AS roll, name, program, email, phone, dob,
                                  blood, gender, address, guardian, mentor, admission_year
                           FROM students LIMIT 1""") or {}
    attendance = fetch_all("SELECT subject, attended, total FROM attendance ORDER BY id")
    exams = fetch_all("SELECT subject, internal, external, grade FROM exam_scores ORDER BY id")
    practicals = fetch_all("SELECT lab, marks, grade FROM practical_scores ORDER BY id")
    ann_general = fetch_all("SELECT title, posted_on AS date, body FROM announcements WHERE category='General' ORDER BY id")
    ann_exam = fetch_all("SELECT title, posted_on AS date, body FROM announcements WHERE category='Exam' ORDER BY id")
    upd_rows = fetch_all("SELECT category, title, posted_on AS date, body FROM updates ORDER BY id")
    fees = fetch_all("SELECT * FROM fees ORDER BY id")
    projects = fetch_all("SELECT * FROM projects ORDER BY id DESC")

    updates = {"campus": [], "events": [], "culturals": [], "sports": []}
    for r in upd_rows:
        key = r["category"].lower()
        if key in updates:
            updates[key].append(r)

    for a in attendance:
        a["pct"] = round(a["attended"] / a["total"] * 100) if a["total"] else 0
    for s in exams:
        s["total"] = s["internal"] + s["external"]

    total_att = sum(a["attended"] for a in attendance)
    total_cls = sum(a["total"] for a in attendance)
    attendance_pct = round(total_att / total_cls * 100) if total_cls else 0
    pending_fees = sum(f["amount"] for f in fees if f["status"] == "Pending")
    upcoming_events = sum(len(v) for v in updates.values())

    grade_points = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C": 6}
    pts = [grade_points.get(s["grade"], 7) for s in exams]
    cgpa = round(sum(pts) / len(pts), 2) if pts else 0

    return render_template(
        "dashboard.html",
        profile=profile, attendance=attendance, exams=exams, practicals=practicals,
        ann_general=ann_general, ann_exam=ann_exam, updates=updates,
        fees=fees, projects=projects,
        summary={"attendance_pct": attendance_pct, "pending_fees": pending_fees,
                 "upcoming_events": upcoming_events, "cgpa": cgpa},
    )


# ==================================================================
#  Fees + receipts
# ==================================================================
@app.route("/pay/<int:fee_id>")
@login_required
def pay(fee_id):
    fee = fetch_one("SELECT * FROM fees WHERE id=%s", (fee_id,))
    if fee and fee["status"] == "Pending":
        execute("UPDATE fees SET status='Paid', receipt_no=%s, paid_on=%s WHERE id=%s",
                (f"SH-{2000 + fee_id}", datetime.now().strftime("%d %b %Y"), fee_id))
        flash("Payment successful! Receipt generated.")
    return redirect(url_for("dashboard") + "#panel-fees")


@app.route("/receipt/<int:fee_id>")
@login_required
def receipt(fee_id):
    fee = fetch_one("SELECT * FROM fees WHERE id=%s", (fee_id,))
    profile = fetch_one("SELECT roll_no AS roll, name, program FROM students LIMIT 1") or {}
    if not fee or fee["status"] != "Paid":
        return redirect(url_for("dashboard"))
    return render_template("receipt.html", fee=fee, profile=profile)


# ==================================================================
#  Project upload
# ==================================================================
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    if file and file.filename:
        fname = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, fname))
        execute("INSERT INTO projects (title, subject, filename, uploaded_on) VALUES (%s, %s, %s, %s)",
                (request.form.get("title", "Untitled"), request.form.get("subject", ""),
                 fname, datetime.now().strftime("%d %b %Y")))
        flash("Project uploaded successfully!")
    else:
        flash("Please choose a file to upload.")
    return redirect(url_for("dashboard") + "#panel-projects")


@app.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
