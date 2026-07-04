"""
StudentHub - All-in-One Student Portal
CAPOL510 - IS Development Laboratory (Mini Project)

Lightweight portal built with Flask + SQLite.
Run:  python app.py   then open  http://127.0.0.1:5000
Login:  student / 1234
"""

import os
import sqlite3
import tempfile
from datetime import datetime
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, send_from_directory)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "studenthub-mini-project"

# On Vercel (serverless) only the temp folder is writable, so the database and
# uploads must live there. Locally they stay inside the project folder as usual.
ON_VERCEL = os.environ.get("VERCEL") == "1"
DATA_DIR = tempfile.gettempdir() if ON_VERCEL else "."
DB = os.path.join(DATA_DIR, "studenthub.db")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads") if ON_VERCEL else os.path.join("static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---- Demo login ----
STUDENT_USER = "student"
STUDENT_PASS = "1234"


# ==================================================================
#  Seeded content (static demo data shown on the dashboard)
# ==================================================================
PROFILE = {
    "name": "Vishnu Kumar",
    "roll": "126003100",
    "program": "MCA (Online) - Semester 3",
    "email": "vishnu@sastra.edu",
    "phone": "+91 98765 43210",
    "dob": "12 March 2002",
    "blood": "O+",
    "gender": "Male",
    "address": "Thanjavur, Tamil Nadu, India",
    "guardian": "Mr. Ramesh Kumar",
    "admission_year": "2024",
    "mentor": "Dr. S. Priya",
}

ATTENDANCE = [
    {"subject": "Information Security",          "attended": 44, "total": 48},
    {"subject": "Cloud Computing",               "attended": 40, "total": 46},
    {"subject": "Machine Learning",              "attended": 38, "total": 45},
    {"subject": "Software Project Management",   "attended": 42, "total": 44},
    {"subject": "IS Development Laboratory",      "attended": 30, "total": 32},
]

EXAM_SCORES = [
    {"subject": "Information Security",        "internal": 28, "external": 61, "grade": "A"},
    {"subject": "Cloud Computing",             "internal": 26, "external": 58, "grade": "A"},
    {"subject": "Machine Learning",            "internal": 24, "external": 55, "grade": "B+"},
    {"subject": "Software Project Management",  "internal": 29, "external": 63, "grade": "A+"},
]

PRACTICAL_SCORES = [
    {"lab": "IS Development Laboratory",  "marks": 92, "grade": "A+"},
    {"lab": "Cloud Computing Lab",        "marks": 88, "grade": "A"},
    {"lab": "Machine Learning Lab",       "marks": 85, "grade": "A"},
]

ANNOUNCEMENTS_GENERAL = [
    {"title": "Library timings extended", "date": "02 Jul 2026",
     "body": "The central library will now remain open till 9:00 PM on weekdays."},
    {"title": "New Wi-Fi network live", "date": "28 Jun 2026",
     "body": "Connect to 'SASTRA-Campus-5G' using your student credentials."},
    {"title": "ID card renewal", "date": "20 Jun 2026",
     "body": "Students must renew their ID cards at the admin office before 15 Jul."},
]

ANNOUNCEMENTS_EXAM = [
    {"title": "End-Semester Exam Schedule Released", "date": "01 Jul 2026",
     "body": "Semester 3 theory exams begin from 20 Jul 2026. Check the timetable."},
    {"title": "Practical Exam Dates", "date": "26 Jun 2026",
     "body": "Lab practical exams are scheduled between 12 Jul and 18 Jul 2026."},
    {"title": "Hall Ticket Download", "date": "24 Jun 2026",
     "body": "Hall tickets can be downloaded from 10 Jul. Clear pending fees first."},
]

UPDATES = {
    "campus": [
        {"title": "New Innovation Lab inaugurated", "date": "03 Jul 2026",
         "body": "A state-of-the-art AI & IoT lab has opened in Block C."},
        {"title": "Green campus drive", "date": "29 Jun 2026",
         "body": "Tree plantation programme this weekend. Volunteers welcome."},
    ],
    "events": [
        {"title": "Tech Symposium 'Cognizance 2026'", "date": "15 Jul 2026",
         "body": "National level technical symposium with workshops and prizes."},
        {"title": "Guest Lecture: Cyber Security", "date": "10 Jul 2026",
         "body": "Industry expert session on ethical hacking. Register now."},
    ],
    "culturals": [
        {"title": "Annual Cultural Fest 'Kalotsav'", "date": "22 Jul 2026",
         "body": "Music, dance and drama competitions. Registrations open."},
        {"title": "Battle of Bands", "date": "18 Jul 2026",
         "body": "Show your musical talent. Sign up at the cultural desk."},
    ],
    "sports": [
        {"title": "Inter-Department Cricket Tournament", "date": "20 Jul 2026",
         "body": "Form your teams and register before 12 Jul."},
        {"title": "Annual Athletic Meet", "date": "25 Jul 2026",
         "body": "Track and field events at the main stadium."},
    ],
}


# ==================================================================
#  Database (fees + uploaded projects live here)
# ==================================================================
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT,
            category  TEXT,
            amount    INTEGER,
            status    TEXT DEFAULT 'Pending',
            receipt_no TEXT,
            paid_on   TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT,
            subject     TEXT,
            filename    TEXT,
            uploaded_on TEXT
        )
    """)
    # Seed the fee list only once
    if conn.execute("SELECT COUNT(*) AS c FROM fees").fetchone()["c"] == 0:
        conn.executemany(
            "INSERT INTO fees (name, category, amount, status) VALUES (?, ?, ?, ?)",
            [
                ("Tuition Fee",  "Academic", 45000, "Pending"),
                ("Exam Fee",     "Academic",  2500, "Pending"),
                ("Bus Fee",      "Transport", 18000, "Paid"),
                ("Canteen Fee",  "Food",      12000, "Pending"),
                ("Hostel Fee",   "Boarding",  35000, "Paid"),
            ],
        )
        # give the pre-paid ones a receipt number
        conn.execute("UPDATE fees SET receipt_no='SH-1003', paid_on='15 Jun 2026' WHERE name='Bus Fee'")
        conn.execute("UPDATE fees SET receipt_no='SH-1005', paid_on='10 Jun 2026' WHERE name='Hostel Fee'")
    conn.commit()
    conn.close()


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
        if (request.form.get("username") == STUDENT_USER
                and request.form.get("password") == STUDENT_PASS):
            session["user"] = PROFILE["name"]
            return redirect(url_for("dashboard"))
        flash("Invalid Credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ==================================================================
#  Main dashboard (single page, panels switched with JavaScript)
# ==================================================================
@app.route("/")
@login_required
def dashboard():
    conn = get_db()
    fees = conn.execute("SELECT * FROM fees ORDER BY id").fetchall()
    projects = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    conn.close()

    # ---- summary numbers for the dashboard tiles ----
    total_att = sum(a["attended"] for a in ATTENDANCE)
    total_cls = sum(a["total"] for a in ATTENDANCE)
    attendance_pct = round(total_att / total_cls * 100) if total_cls else 0

    pending_fees = sum(f["amount"] for f in fees if f["status"] == "Pending")
    upcoming_events = sum(len(v) for v in UPDATES.values())

    # simple CGPA estimate from grades
    grade_points = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C": 6}
    pts = [grade_points.get(s["grade"], 7) for s in EXAM_SCORES]
    cgpa = round(sum(pts) / len(pts), 2) if pts else 0

    # attach computed % to each attendance row
    att = [{**a, "pct": round(a["attended"] / a["total"] * 100)} for a in ATTENDANCE]
    exams = [{**s, "total": s["internal"] + s["external"]} for s in EXAM_SCORES]

    return render_template(
        "dashboard.html",
        profile=PROFILE,
        attendance=att,
        exams=exams,
        practicals=PRACTICAL_SCORES,
        ann_general=ANNOUNCEMENTS_GENERAL,
        ann_exam=ANNOUNCEMENTS_EXAM,
        updates=UPDATES,
        fees=fees,
        projects=projects,
        summary={
            "attendance_pct": attendance_pct,
            "pending_fees": pending_fees,
            "upcoming_events": upcoming_events,
            "cgpa": cgpa,
        },
    )


# ==================================================================
#  Fee payment + receipts
# ==================================================================
@app.route("/pay/<int:fee_id>")
@login_required
def pay(fee_id):
    conn = get_db()
    fee = conn.execute("SELECT * FROM fees WHERE id=?", (fee_id,)).fetchone()
    if fee and fee["status"] == "Pending":
        receipt_no = f"SH-{2000 + fee_id}"
        paid_on = datetime.now().strftime("%d %b %Y")
        conn.execute(
            "UPDATE fees SET status='Paid', receipt_no=?, paid_on=? WHERE id=?",
            (receipt_no, paid_on, fee_id),
        )
        conn.commit()
    conn.close()
    flash("Payment successful! Receipt generated.")
    return redirect(url_for("dashboard") + "#panel-fees")


@app.route("/receipt/<int:fee_id>")
@login_required
def receipt(fee_id):
    conn = get_db()
    fee = conn.execute("SELECT * FROM fees WHERE id=?", (fee_id,)).fetchone()
    conn.close()
    if not fee or fee["status"] != "Paid":
        return redirect(url_for("dashboard"))
    return render_template("receipt.html", fee=fee, profile=PROFILE)


# ==================================================================
#  Project upload
# ==================================================================
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    title = request.form.get("title", "Untitled")
    subject = request.form.get("subject", "")
    if file and file.filename:
        fname = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, fname))
        conn = get_db()
        conn.execute(
            "INSERT INTO projects (title, subject, filename, uploaded_on) VALUES (?, ?, ?, ?)",
            (title, subject, fname, datetime.now().strftime("%d %b %Y")),
        )
        conn.commit()
        conn.close()
        flash("Project uploaded successfully!")
    else:
        flash("Please choose a file to upload.")
    return redirect(url_for("dashboard") + "#panel-projects")


@app.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


# Create/seed the database as soon as the app is imported. This is required on
# Vercel (which imports `app` and never runs the block below) and is harmless
# locally because the tables are only created if they don't already exist.
init_db()

if __name__ == "__main__":
    app.run(debug=True)
