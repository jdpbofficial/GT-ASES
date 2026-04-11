GT-ASES — Globe Telecom Applicant Screening and Evaluation System
Phase 1: Local Desktop Application
=================================================================

HOW TO RUN:
1. Make sure Python 3.x is installed on your computer.
2. Open a terminal or command prompt.
3. Navigate to this folder: cd GT-ASES
4. Run the app: python main.py

DEFAULT LOGIN CREDENTIALS:
  Admin  →  username: admin     password: admin123
  Staff  →  username: hrstaff  password: staff123

FILE STRUCTURE:
  main.py          — Entry point, run this!
  theme.py         — Colors and fonts
  data_manager.py  — All data read/write logic
  login.py         — Login screen
  dashboard.py     — Main app shell + dashboard
  pages/
    applicants.py  — View, search, edit, delete applicants
    add_applicant.py — Add new / edit applicant form
    screening.py   — Auto-screening and ranking
    export.py      — Export to CSV
    users.py       — User management (Admin only)
  data/
    applicants.json — Applicant records (auto-created)
    users.json      — User accounts (auto-created)

REQUIREMENTS:
  Python 3.x (no extra packages needed — uses built-in tkinter)

Developed by: Jae, Christine Joy, Jerox, Anne Chel, Sam
Course: Information Technology — OLSHCO
