"""
StudentHub - All-in-One Student Portal (MySQL version)
CAPOL510 - IS Development Laboratory (Mini Project)

Reads ALL data from the MySQL 'studenthub' database, so the UI always
matches what you see in DBeaver.

Setup:
  1. Make sure MySQL is running and you ran  setup_db_mysql.py  once.
  2. Put your MySQL root password below (or set env var MYSQL_PASSWORD).
  3. pip install -r requirements.txt
  4. python app.py   ->  http://127.0.0.1:5000   (login: student / 1234)
"""

import os
from datetime import datetime
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, send_from_directory)
from werkzeug.utils import secure_filename
import pymysql

app = Flask(__name__)
app.secret_key = "studenthub-mini-project"

# ================= MySQL connection settings =================
# >>> EDIT the password here to match your MySQL root password <<<
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root")
MYSQL_DB = "studenthub"

UPLOAD_DIR = os.path.join("static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    """Open a new MySQL connection that returns rows as dictionaries."""
    return pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD,
        database=MYSQL_DB, cursorclass=pymysql.cursors.DictCursor, autocommit=True,
    )


# ================= Auth =================
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
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (request.form.get("username"), request.form.get("password")),
            )
            user = cur.fetchone()
        conn.close()
        if user:
            session["user"] = user["username"]
            return redirect(url_for("dashboard"))
        flash("Invalid Credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ================= Dashboard =================
@app.route("/")
@login_required
def dashboard():
    conn = get_db()
    with conn.cursor() as cur:
        # profile (the single student). roll_no is aliased to 'roll' for the template.
        cur.execute("""SELECT roll_no AS roll, name, program, email, phone, dob,
                              blood, gender, address, guardian, mentor, admission_year
                       FROM students LIMIT 1""")
        profile = cur.fetchone() or {}

        cur.execute("SELECT subject, attended, total FROM attendance ORDER BY id")
        attendance = cur.fetchall()

        cur.execute("SELECT subject, internal, external, grade FROM exam_scores ORDER BY id")
        exams = cur.fetchall()

        cur.execute("SELECT lab, marks, grade FROM practical_scores ORDER BY id")
        practicals = cur.fetchall()

        cur.execute("SELECT title, posted_on AS date, body FROM announcements WHERE category='General' ORDER BY id")
        ann_general = cur.fetchall()
        cur.execute("SELECT title, posted_on AS date, body FROM announcements WHERE category='Exam' ORDER BY id")
        ann_exam = cur.fetchall()

        cur.execute("SELECT category, title, posted_on AS date, body FROM updates ORDER BY id")
        upd_rows = cur.fetchall()

        cur.execute("SELECT * FROM fees ORDER BY id")
        fees = cur.fetchall()

        cur.execute("SELECT * FROM projects ORDER BY id DESC")
        projects = cur.fetchall()
    conn.close()

    # group updates by category for the tabbed panel
    updates = {"campus": [], "events": [], "culturals": [], "sports": []}
    for r in upd_rows:
        key = r["category"].lower()
        if key in updates:
            updates[key].append(r)

    # computed values
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


# ================= Fees + receipts =================
@app.route("/pay/<int:fee_id>")
@login_required
def pay(fee_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM fees WHERE id=%s", (fee_id,))
        fee = cur.fetchone()
        if fee and fee["status"] == "Pending":
            cur.execute(
                "UPDATE fees SET status='Paid', receipt_no=%s, paid_on=%s WHERE id=%s",
                (f"SH-{2000 + fee_id}", datetime.now().strftime("%d %b %Y"), fee_id),
            )
    conn.close()
    flash("Payment successful! Receipt generated.")
    return redirect(url_for("dashboard") + "#panel-fees")


@app.route("/receipt/<int:fee_id>")
@login_required
def receipt(fee_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM fees WHERE id=%s", (fee_id,))
        fee = cur.fetchone()
        cur.execute("SELECT roll_no AS roll, name, program FROM students LIMIT 1")
        profile = cur.fetchone() or {}
    conn.close()
    if not fee or fee["status"] != "Paid":
        return redirect(url_for("dashboard"))
    return render_template("receipt.html", fee=fee, profile=profile)


# ================= Project upload =================
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    if file and file.filename:
        fname = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, fname))
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO projects (title, subject, filename, uploaded_on) VALUES (%s, %s, %s, %s)",
                (request.form.get("title", "Untitled"), request.form.get("subject", ""),
                 fname, datetime.now().strftime("%d %b %Y")),
            )
        conn.close()
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
