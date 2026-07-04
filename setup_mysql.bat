@echo off
REM ================================================================
REM  Runs the ENTIRE studenthub_mysql.sql file into MySQL at once.
REM  Double-click this file, then type your MySQL root password.
REM ================================================================
cd /d "%~dp0"

echo Setting up the StudentHub database in MySQL...
echo (Enter your MySQL root password when asked)
echo.

REM Try mysql from PATH first
mysql -u root -p < studenthub_mysql.sql

if %errorlevel%==0 (
    echo.
    echo ====================================================
    echo  SUCCESS! All 9 tables created in database studenthub.
    echo  Now open DBeaver and press F5 to refresh.
    echo ====================================================
) else (
    echo.
    echo If you saw "mysql is not recognized", MySQL is not on your PATH.
    echo Read the instructions Claude gave you for the full-path command.
)
echo.
pause
