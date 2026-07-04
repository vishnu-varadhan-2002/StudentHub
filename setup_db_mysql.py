"""
StudentHub - MySQL database builder
Creates the studenthub database + all 9 tables + demo data in one run.

Run:  python setup_db_mysql.py
Then type your MySQL root password when asked.
"""

import sys
import subprocess
import getpass

# Auto-install the MySQL driver if it's missing
try:
    import pymysql
except ImportError:
    print("Installing pymysql (one-time)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql"])
    import pymysql

pwd = getpass.getpass("Enter your MySQL root password: ")

# ---- connect (no database yet) ----
conn = pymysql.connect(host="localhost", user="root", password=pwd)
cur = conn.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS studenthub")
cur.execute("USE studenthub")
print("Database 'studenthub' ready.\n")

# ---- drop old tables for a clean rebuild ----
tables = ["users", "students", "attendance", "exam_scores",
          "practical_scores", "announcements", "updates", "fees", "projects"]
for t in tables:
    cur.execute(f"DROP TABLE IF EXISTS {t}")

# ---- create tables ----
create = {
    "users": "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), password VARCHAR(50), role VARCHAR(20))",
    "students": "CREATE TABLE students (id INT AUTO_INCREMENT PRIMARY KEY, roll_no VARCHAR(20), name VARCHAR(100), program VARCHAR(80), email VARCHAR(80), phone VARCHAR(30), dob VARCHAR(30), blood VARCHAR(5), gender VARCHAR(10), address VARCHAR(150), guardian VARCHAR(80), mentor VARCHAR(80), admission_year VARCHAR(10))",
    "attendance": "CREATE TABLE attendance (id INT AUTO_INCREMENT PRIMARY KEY, roll_no VARCHAR(20), subject VARCHAR(80), attended INT, total INT)",
    "exam_scores": "CREATE TABLE exam_scores (id INT AUTO_INCREMENT PRIMARY KEY, roll_no VARCHAR(20), subject VARCHAR(80), internal INT, external INT, grade VARCHAR(5))",
    "practical_scores": "CREATE TABLE practical_scores (id INT AUTO_INCREMENT PRIMARY KEY, roll_no VARCHAR(20), lab VARCHAR(80), marks INT, grade VARCHAR(5))",
    "announcements": "CREATE TABLE announcements (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(20), title VARCHAR(120), posted_on VARCHAR(30), body VARCHAR(255))",
    "updates": "CREATE TABLE updates (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(20), title VARCHAR(120), posted_on VARCHAR(30), body VARCHAR(255))",
    "fees": "CREATE TABLE fees (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), category VARCHAR(50), amount INT, status VARCHAR(20) DEFAULT 'Pending', receipt_no VARCHAR(30), paid_on VARCHAR(30))",
    "projects": "CREATE TABLE projects (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(150), subject VARCHAR(100), filename VARCHAR(200), uploaded_on VARCHAR(30))",
}
for name, sql in create.items():
    try:
        cur.execute(sql)
        print(f"  [OK]     created table: {name}")
    except Exception as e:
        print(f"  [FAILED] {name}: {e}")

# ---- insert demo data ----
data = {
    "users": [
        ("student", "1234", "student"),
        ("admin", "admin123", "admin"),
    ],
    "students": [
        ("126003100", "Vishnu Kumar", "MCA (Online) - Semester 3", "vishnu@sastra.edu",
         "+91 98765 43210", "12 March 2002", "O+", "Male",
         "Thanjavur, Tamil Nadu, India", "Mr. Ramesh Kumar", "Dr. S. Priya", "2024"),
    ],
    "attendance": [
        ("126003100", "Information Security", 44, 48),
        ("126003100", "Cloud Computing", 40, 46),
        ("126003100", "Machine Learning", 38, 45),
        ("126003100", "Software Project Management", 42, 44),
        ("126003100", "IS Development Laboratory", 30, 32),
    ],
    "exam_scores": [
        ("126003100", "Information Security", 28, 61, "A"),
        ("126003100", "Cloud Computing", 26, 58, "A"),
        ("126003100", "Machine Learning", 24, 55, "B+"),
        ("126003100", "Software Project Management", 29, 63, "A+"),
    ],
    "practical_scores": [
        ("126003100", "IS Development Laboratory", 92, "A+"),
        ("126003100", "Cloud Computing Lab", 88, "A"),
        ("126003100", "Machine Learning Lab", 85, "A"),
    ],
    "announcements": [
        ("General", "Library timings extended", "02 Jul 2026", "The central library will now remain open till 9:00 PM on weekdays."),
        ("General", "New Wi-Fi network live", "28 Jun 2026", "Connect to 'SASTRA-Campus-5G' using your student credentials."),
        ("General", "ID card renewal", "20 Jun 2026", "Students must renew their ID cards at the admin office before 15 Jul."),
        ("Exam", "End-Semester Exam Schedule Released", "01 Jul 2026", "Semester 3 theory exams begin from 20 Jul 2026. Check the timetable."),
        ("Exam", "Practical Exam Dates", "26 Jun 2026", "Lab practical exams are scheduled between 12 Jul and 18 Jul 2026."),
        ("Exam", "Hall Ticket Download", "24 Jun 2026", "Hall tickets can be downloaded from 10 Jul. Clear pending fees first."),
    ],
    "updates": [
        ("Campus", "New Innovation Lab inaugurated", "03 Jul 2026", "A state-of-the-art AI and IoT lab has opened in Block C."),
        ("Campus", "Green campus drive", "29 Jun 2026", "Tree plantation programme this weekend. Volunteers welcome."),
        ("Events", "Tech Symposium Cognizance 2026", "15 Jul 2026", "National level technical symposium with workshops and prizes."),
        ("Events", "Guest Lecture on Cyber Security", "10 Jul 2026", "Industry expert session on ethical hacking. Register now."),
        ("Culturals", "Annual Cultural Fest Kalotsav", "22 Jul 2026", "Music, dance and drama competitions. Registrations open."),
        ("Culturals", "Battle of Bands", "18 Jul 2026", "Show your musical talent. Sign up at the cultural desk."),
        ("Sports", "Inter-Department Cricket Tournament", "20 Jul 2026", "Form your teams and register before 12 Jul."),
        ("Sports", "Annual Athletic Meet", "25 Jul 2026", "Track and field events at the main stadium."),
    ],
    "fees": [
        ("Tuition Fee", "Academic", 45000, "Pending", None, None),
        ("Exam Fee", "Academic", 2500, "Pending", None, None),
        ("Bus Fee", "Transport", 18000, "Paid", "SH-1003", "15 Jun 2026"),
        ("Canteen Fee", "Food", 12000, "Pending", None, None),
        ("Hostel Fee", "Boarding", 35000, "Paid", "SH-1005", "10 Jun 2026"),
    ],
    "projects": [
        ("StudentHub Portal", "IS Development Lab", "studenthub.zip", "01 Jul 2026"),
        ("Cloud Notes App", "Cloud Computing", "cloudnotes.pdf", "28 Jun 2026"),
    ],
}
cols = {
    "users": "(username, password, role)",
    "students": "(roll_no, name, program, email, phone, dob, blood, gender, address, guardian, mentor, admission_year)",
    "attendance": "(roll_no, subject, attended, total)",
    "exam_scores": "(roll_no, subject, internal, external, grade)",
    "practical_scores": "(roll_no, lab, marks, grade)",
    "announcements": "(category, title, posted_on, body)",
    "updates": "(category, title, posted_on, body)",
    "fees": "(name, category, amount, status, receipt_no, paid_on)",
    "projects": "(title, subject, filename, uploaded_on)",
}
for name, rows in data.items():
    ph = ", ".join(["%s"] * len(rows[0]))
    cur.executemany(f"INSERT INTO {name} {cols[name]} VALUES ({ph})", rows)
    print(f"  [OK]     inserted {len(rows)} rows into: {name}")

conn.commit()

# ---- show final result ----
cur.execute("SHOW TABLES")
print("\nTables now in 'studenthub':")
for row in cur.fetchall():
    print("   -", row[0])

cur.close()
conn.close()
print("\nDONE! Open DBeaver and press F5 to refresh -> studenthub -> Tables.")
