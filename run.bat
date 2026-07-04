@echo off
REM ===== StudentHub launcher =====
REM Double-click this file to start the app from the correct folder.
cd /d "%~dp0"
echo Starting StudentHub...
echo Open your browser at http://127.0.0.1:5000  (login: student / 1234)
echo Press CTRL+C to stop.
python app.py
pause
