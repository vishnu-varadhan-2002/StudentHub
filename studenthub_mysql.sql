-- ============================================================
--  StudentHub - COMPLETE MySQL database (all tables + data)
--  Run the WHOLE script with  Alt + X  (Execute Script)
--  Then press F5 to refresh -> studenthub -> Tables
-- ============================================================

CREATE DATABASE IF NOT EXISTS studenthub;

-- Clean rebuild (avoids duplicate rows from earlier runs)
DROP TABLE IF EXISTS studenthub.users;
DROP TABLE IF EXISTS studenthub.students;
DROP TABLE IF EXISTS studenthub.attendance;
DROP TABLE IF EXISTS studenthub.exam_scores;
DROP TABLE IF EXISTS studenthub.practical_scores;
DROP TABLE IF EXISTS studenthub.announcements;
DROP TABLE IF EXISTS studenthub.updates;
DROP TABLE IF EXISTS studenthub.fees;
DROP TABLE IF EXISTS studenthub.projects;

-- ---------- 1. users (login) ----------
CREATE TABLE studenthub.users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), password VARCHAR(50), role VARCHAR(20));
INSERT INTO studenthub.users (username, password, role) VALUES ('student', '1234', 'student');
INSERT INTO studenthub.users (username, password, role) VALUES ('admin', 'admin123', 'admin');

-- ---------- 2. students (bio data) ----------
CREATE TABLE studenthub.students (id INT AUTO_INCREMENT PRIMARY KEY, roll_no VARCHAR(20), name VARCHAR(100), program VARCHAR(80), email VARCHAR(80), phone VARCHAR(30), dob VARCHAR(30), blood VARCHAR(5), gender VARCHAR(10), address VARCHAR(150), guardian VARCHAR(80), mentor VARCHAR(80), admission_year VARCHAR(10));
INSERT INTO studenthub.students (roll_no, name, program, email, phone, dob, blood, gender, address, guardian, mentor, admission_year) VALUES ('126003100', 'Vishnu Kumar', 'MCA (Online) - Semester 3', 'vishnu@sastra.edu', '+91 98765 43210', '12 March 2002', 'O+', 'Male', 'Thanjavur, Tamil Nadu, India', 'Mr. Ramesh Kumar', 'Dr. S. Priya', '2024');

-- ---------- 3. attendance ----------
CREATE TABLE studenthub.attendance (id INT AUTO_INCREMENT PRIMARY KEY, roll_no VARCHAR(20), subject VARCHAR(80), attended INT, total INT);
INSERT INTO studenthub.attendance (roll_no, subject, attended, total) VALUES ('126003100', 'Information Security', 44, 48);
INSERT INTO studenthub.attendance (roll_no, subject, attended, total) VALUES ('126003100', 'Cloud Computing', 40, 46);
INSERT INTO studenthub.attendance (roll_no, subject, attended, total) VALUES ('126003100', 'Machine Learning', 38, 45);
INSERT INTO studenthub.attendance (roll_no, subject, attended, total) VALUES ('126003100', 'Software Project Management', 42, 44);
INSERT INTO studenthub.attendance (roll_no, subject, attended, total) VALUES ('126003100', 'IS Development Laboratory', 30, 32);

-- ---------- 4. exam_scores ----------
CREATE TABLE studenthub.exam_scores (id INT AUTO_INCREMENT PRIMARY KEY, roll_no VARCHAR(20), subject VARCHAR(80), internal INT, external INT, grade VARCHAR(5));
INSERT INTO studenthub.exam_scores (roll_no, subject, internal, external, grade) VALUES ('126003100', 'Information Security', 28, 61, 'A');
INSERT INTO studenthub.exam_scores (roll_no, subject, internal, external, grade) VALUES ('126003100', 'Cloud Computing', 26, 58, 'A');
INSERT INTO studenthub.exam_scores (roll_no, subject, internal, external, grade) VALUES ('126003100', 'Machine Learning', 24, 55, 'B+');
INSERT INTO studenthub.exam_scores (roll_no, subject, internal, external, grade) VALUES ('126003100', 'Software Project Management', 29, 63, 'A+');

-- ---------- 5. practical_scores ----------
CREATE TABLE studenthub.practical_scores (id INT AUTO_INCREMENT PRIMARY KEY, roll_no VARCHAR(20), lab VARCHAR(80), marks INT, grade VARCHAR(5));
INSERT INTO studenthub.practical_scores (roll_no, lab, marks, grade) VALUES ('126003100', 'IS Development Laboratory', 92, 'A+');
INSERT INTO studenthub.practical_scores (roll_no, lab, marks, grade) VALUES ('126003100', 'Cloud Computing Lab', 88, 'A');
INSERT INTO studenthub.practical_scores (roll_no, lab, marks, grade) VALUES ('126003100', 'Machine Learning Lab', 85, 'A');

-- ---------- 6. announcements ----------
CREATE TABLE studenthub.announcements (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(20), title VARCHAR(120), posted_on VARCHAR(30), body VARCHAR(255));
INSERT INTO studenthub.announcements (category, title, posted_on, body) VALUES ('General', 'Library timings extended', '02 Jul 2026', 'The central library will now remain open till 9:00 PM on weekdays.');
INSERT INTO studenthub.announcements (category, title, posted_on, body) VALUES ('General', 'New Wi-Fi network live', '28 Jun 2026', 'Connect to ''SASTRA-Campus-5G'' using your student credentials.');
INSERT INTO studenthub.announcements (category, title, posted_on, body) VALUES ('General', 'ID card renewal', '20 Jun 2026', 'Students must renew their ID cards at the admin office before 15 Jul.');
INSERT INTO studenthub.announcements (category, title, posted_on, body) VALUES ('Exam', 'End-Semester Exam Schedule Released', '01 Jul 2026', 'Semester 3 theory exams begin from 20 Jul 2026. Check the timetable.');
INSERT INTO studenthub.announcements (category, title, posted_on, body) VALUES ('Exam', 'Practical Exam Dates', '26 Jun 2026', 'Lab practical exams are scheduled between 12 Jul and 18 Jul 2026.');
INSERT INTO studenthub.announcements (category, title, posted_on, body) VALUES ('Exam', 'Hall Ticket Download', '24 Jun 2026', 'Hall tickets can be downloaded from 10 Jul. Clear pending fees first.');

-- ---------- 7. updates (campus / events / culturals / sports) ----------
CREATE TABLE studenthub.updates (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(20), title VARCHAR(120), posted_on VARCHAR(30), body VARCHAR(255));
INSERT INTO studenthub.updates (category, title, posted_on, body) VALUES ('Campus', 'New Innovation Lab inaugurated', '03 Jul 2026', 'A state-of-the-art AI and IoT lab has opened in Block C.');
INSERT INTO studenthub.updates (category, title, posted_on, body) VALUES ('Campus', 'Green campus drive', '29 Jun 2026', 'Tree plantation programme this weekend. Volunteers welcome.');
INSERT INTO studenthub.updates (category, title, posted_on, body) VALUES ('Events', 'Tech Symposium Cognizance 2026', '15 Jul 2026', 'National level technical symposium with workshops and prizes.');
INSERT INTO studenthub.updates (category, title, posted_on, body) VALUES ('Events', 'Guest Lecture on Cyber Security', '10 Jul 2026', 'Industry expert session on ethical hacking. Register now.');
INSERT INTO studenthub.updates (category, title, posted_on, body) VALUES ('Culturals', 'Annual Cultural Fest Kalotsav', '22 Jul 2026', 'Music, dance and drama competitions. Registrations open.');
INSERT INTO studenthub.updates (category, title, posted_on, body) VALUES ('Culturals', 'Battle of Bands', '18 Jul 2026', 'Show your musical talent. Sign up at the cultural desk.');
INSERT INTO studenthub.updates (category, title, posted_on, body) VALUES ('Sports', 'Inter-Department Cricket Tournament', '20 Jul 2026', 'Form your teams and register before 12 Jul.');
INSERT INTO studenthub.updates (category, title, posted_on, body) VALUES ('Sports', 'Annual Athletic Meet', '25 Jul 2026', 'Track and field events at the main stadium.');

-- ---------- 8. fees ----------
CREATE TABLE studenthub.fees (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), category VARCHAR(50), amount INT, status VARCHAR(20) DEFAULT 'Pending', receipt_no VARCHAR(30), paid_on VARCHAR(30));
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Tuition Fee', 'Academic', 45000, 'Pending', NULL, NULL);
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Exam Fee', 'Academic', 2500, 'Pending', NULL, NULL);
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Bus Fee', 'Transport', 18000, 'Paid', 'SH-1003', '15 Jun 2026');
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Canteen Fee', 'Food', 12000, 'Pending', NULL, NULL);
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Hostel Fee', 'Boarding', 35000, 'Paid', 'SH-1005', '10 Jun 2026');

-- ---------- 9. projects ----------
CREATE TABLE studenthub.projects (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(150), subject VARCHAR(100), filename VARCHAR(200), uploaded_on VARCHAR(30));
INSERT INTO studenthub.projects (title, subject, filename, uploaded_on) VALUES ('StudentHub Portal', 'IS Development Lab', 'studenthub.zip', '01 Jul 2026');
INSERT INTO studenthub.projects (title, subject, filename, uploaded_on) VALUES ('Cloud Notes App', 'Cloud Computing', 'cloudnotes.pdf', '28 Jun 2026');

-- ---------- Check everything ----------
SHOW TABLES FROM studenthub;
