# 🎓 StudentHub — All-in-One Student Portal

A lightweight student portal built for **CAPOL510 – IS Development Laboratory (Mini Project)**.

**Tech:** Python (Flask) + SQLite + HTML/CSS/JS — no heavy frameworks.

## ✨ Features
- 🔐 Student login
- 🤖 Animated cartoon guide **"Hubby"** that gives a first-time tour
- 🏠 Dashboard with attendance %, CGPA, pending fees & upcoming events
- 🗓️ Subject-wise attendance (low attendance flagged)
- 📊 Results — exam scores + practical lab scores
- 🧑 Bio Data (student profile)
- 📤 Project upload (with file storage)
- 📢 Announcements — general + exam
- 📰 Campus updates — Campus / Events / Culturals / Sports
- 💳 Fees — Tuition / Exam / Bus / Canteen / Hostel + online payment + printable receipts

## ▶️ How to run (Windows)
1. Install Python 3 from python.org (if not already installed).
2. Open a terminal in this folder and install Flask:
   ```
   pip install -r requirements.txt
   ```
3. Start the app:
   ```
   python app.py
   ```
4. Open your browser at **http://127.0.0.1:5000**
5. Login with **student** / **1234**

The database `studenthub.db` and the `static/uploads/` folder are created automatically.

> 💡 An internet connection lets the "Poppins" web font load for the best look;
> without it, the app falls back to a clean system font and still works fully offline.

## 📁 Structure
```
StudentHub/
├── app.py                  # Flask backend + SQLite + routes
├── requirements.txt
├── static/
│   ├── style.css           # full UI + mascot & tour animations
│   ├── app.js              # panel switching, tabs, guided tour
│   └── uploads/            # uploaded project files
└── templates/
    ├── _logo.html          # StudentHub logo (SVG)
    ├── _mascot.html        # Hubby the mascot (SVG)
    ├── login.html
    ├── dashboard.html      # single-page dashboard with all sections
    └── receipt.html        # printable fee receipt
```
