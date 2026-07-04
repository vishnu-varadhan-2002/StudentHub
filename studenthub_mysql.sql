-- ============================================================
--  StudentHub - MySQL schema + demo data  (fully-qualified)
--  Run the WHOLE script with  Alt + X  (Execute Script)
--  Every table is written as  studenthub.<table>  so it always
--  goes into the right database, no matter what is selected.
-- ============================================================

CREATE DATABASE IF NOT EXISTS studenthub;

CREATE TABLE IF NOT EXISTS studenthub.fees (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), category VARCHAR(50), amount INT, status VARCHAR(20) DEFAULT 'Pending', receipt_no VARCHAR(30), paid_on VARCHAR(30));

CREATE TABLE IF NOT EXISTS studenthub.projects (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(150), subject VARCHAR(100), filename VARCHAR(200), uploaded_on VARCHAR(30));

INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Tuition Fee', 'Academic', 45000, 'Pending', NULL, NULL);
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Exam Fee', 'Academic', 2500, 'Pending', NULL, NULL);
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Bus Fee', 'Transport', 18000, 'Paid', 'SH-1003', '15 Jun 2026');
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Canteen Fee', 'Food', 12000, 'Pending', NULL, NULL);
INSERT INTO studenthub.fees (name, category, amount, status, receipt_no, paid_on) VALUES ('Hostel Fee', 'Boarding', 35000, 'Paid', 'SH-1005', '10 Jun 2026');

INSERT INTO studenthub.projects (title, subject, filename, uploaded_on) VALUES ('StudentHub Portal', 'IS Development Lab', 'studenthub.zip', '01 Jul 2026');
INSERT INTO studenthub.projects (title, subject, filename, uploaded_on) VALUES ('Cloud Notes App', 'Cloud Computing', 'cloudnotes.pdf', '28 Jun 2026');

SELECT * FROM studenthub.fees;
