"""
GT-ASES Data Manager — handles all JSON read/write operations.
"""

import json, os, csv, hashlib, secrets, shutil
from datetime import datetime
from config_loader import load_config

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
DATA_DIR       = os.path.join(BASE_DIR, "data")
BACKUP_DIR     = os.path.join(DATA_DIR, "backups")
APPLICANTS_FILE = os.path.join(DATA_DIR, "applicants.json")
USERS_FILE      = os.path.join(DATA_DIR, "users.json")
AUDIT_LOG_FILE  = os.path.join(DATA_DIR, "audit_log.jsonl")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# ── CURRENT USER (set by MainApp on login, cleared on logout) ────────────────
_current_user = None

def set_current_user(user):
    global _current_user
    _current_user = user

def get_current_user():
    return _current_user

# ── DEFAULT DATA ──────────────────────────────────────────────────────────────
DEFAULT_USERS = [
    {"userID": 1, "username": "admin",    "password": "admin123",  "role": "Admin", "fullName": "HR Administrator"},
    {"userID": 2, "username": "hrstaff",  "password": "staff123",  "role": "Staff", "fullName": "HR Staff Member"},
]

DEFAULT_APPLICANTS = [
    {"applicantID": 1001, "firstName": "Maria", "lastName": "Santos", "age": 24, "gender": "Female",
     "contact": "09171234567", "email": "maria.santos@email.com", "position": "Junior Software Developer",
     "education": "Bachelor's", "experience": "1-2 years", "skills": ["Python", "JavaScript", "HTML/CSS"],
     "certifications": ["Google IT Support"], "score": 0, "status": "", "dateApplied": "2025-01-10"},
    {"applicantID": 1002, "firstName": "Juan", "lastName": "Dela Cruz", "age": 30, "gender": "Male",
     "contact": "09181234567", "email": "juan.dc@email.com", "position": "Network Engineer",
     "education": "Bachelor's", "experience": "3-5 years", "skills": ["Networking", "Cybersecurity", "CCNA"],
     "certifications": ["CCNA", "CompTIA Security+"], "score": 0, "status": "", "dateApplied": "2025-01-11"},
    {"applicantID": 1003, "firstName": "Ana", "lastName": "Reyes", "age": 27, "gender": "Female",
     "contact": "09191234567", "email": "ana.reyes@email.com", "position": "Database Administrator",
     "education": "Master's", "experience": "3-5 years", "skills": ["SQL", "Database Admin", "Python"],
     "certifications": ["Oracle Certified", "Microsoft Certified"], "score": 0, "status": "", "dateApplied": "2025-01-12"},
    {"applicantID": 1004, "firstName": "Carlos", "lastName": "Mendoza", "age": 21, "gender": "Male",
     "contact": "09201234567", "email": "carlos.m@email.com", "position": "IT Support Specialist",
     "education": "Vocational", "experience": "0 years", "skills": ["HTML/CSS"],
     "certifications": [], "score": 0, "status": "", "dateApplied": "2025-01-13"},
    {"applicantID": 1005, "firstName": "Sofia", "lastName": "Garcia", "age": 35, "gender": "Female",
     "contact": "09211234567", "email": "sofia.garcia@email.com", "position": "Project Manager (IT)",
     "education": "Master's", "experience": "10+ years", "skills": ["Python", "Cloud Computing", "Machine Learning", "Data Analysis", "System Administration"],
     "certifications": ["PMP", "AWS Certified", "Microsoft Certified"], "score": 0, "status": "", "dateApplied": "2025-01-14"},
]

# ── PASSWORD HASHING ──────────────────────────────────────────────────────────
def hash_password(password):
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored, input_password):
    if "$" not in stored:
        return stored == input_password
    salt, hashed = stored.split("$", 1)
    check = hashlib.sha256((salt + input_password).encode()).hexdigest()
    return check == hashed

def _migrate_passwords(users):
    changed = False
    for u in users:
        if "$" not in u["password"]:
            u["password"] = hash_password(u["password"])
            changed = True
    if changed:
        save_users(users)
    return users

# ── AUDIT LOG ────────────────────────────────────────────────────────────────
def log_action(action, target="", details=""):
    user = get_current_user()
    username = user.get("username", "system") if isinstance(user, dict) else str(user or "system")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user": username,
        "action": action,
        "target": str(target),
        "details": details
    }
    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

# ── FILE HELPERS ──────────────────────────────────────────────────────────────
def _init_file(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=2)

def _load(path):
    _init_file(path, [])
    with open(path, "r") as f:
        return json.load(f)

def _save(path, data):
    # Backup existing file before overwriting
    if os.path.exists(path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{os.path.basename(path)}.{timestamp}.bak"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        shutil.copy2(path, backup_path)
        _prune_backups(os.path.basename(path))
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def _prune_backups(base_name, keep=10):
    backups = sorted(
        [f for f in os.listdir(BACKUP_DIR) if f.startswith(base_name)],
        reverse=True
    )
    for old in backups[keep:]:
        os.remove(os.path.join(BACKUP_DIR, old))

# ── USERS ─────────────────────────────────────────────────────────────────────
def load_users():
    _init_file(USERS_FILE, DEFAULT_USERS)
    data = _load(USERS_FILE)
    _migrate_passwords(data)
    return data

def save_users(users):
    _save(USERS_FILE, users)

def authenticate(username, password):
    for u in load_users():
        if u["username"] == username and verify_password(u["password"], password):
            return u
    return None

def add_user(fullName, username, password, role):
    users = load_users()
    if any(u["username"] == username for u in users):
        return False, "Username already exists."
    new_id = max((u["userID"] for u in users), default=0) + 1
    users.append({"userID": new_id, "username": username, "password": hash_password(password),
                  "role": role, "fullName": fullName})
    save_users(users)
    log_action("ADD_USER", username, f"role={role}")
    return True, "User added successfully."

def update_user(user_id, updates):
    users = load_users()
    for u in users:
        if u["userID"] == user_id:
            if updates.get("password"):
                u["password"] = hash_password(updates["password"])
            u["fullName"] = updates.get("fullName", u["fullName"])
            u["username"] = updates.get("username", u["username"])
            u["role"] = updates.get("role", u["role"])
            save_users(users)
            log_action("UPDATE_USER", user_id, f"fields={list(updates.keys())}")
            return True
    return False

def delete_user(user_id):
    users = load_users()
    users = [u for u in users if u["userID"] != user_id]
    save_users(users)
    log_action("DELETE_USER", user_id)

# ── APPLICANTS ────────────────────────────────────────────────────────────────
def load_applicants():
    _init_file(APPLICANTS_FILE, DEFAULT_APPLICANTS)
    data = _load(APPLICANTS_FILE)
    # auto-score on load and persist if changed
    changed = False
    for a in data:
        new_score, new_status = compute_score(a)
        if a.get("score") != new_score or a.get("status") != new_status:
            a["score"] = new_score
            a["status"] = new_status
            changed = True
    if changed:
        _save(APPLICANTS_FILE, data)
    return data

def save_applicants(applicants):
    _save(APPLICANTS_FILE, applicants)

def compute_score(app):
    cfg = load_config()
    edu_scores    = cfg["EDU_SCORES"]
    exp_scores    = cfg["EXP_SCORES"]
    skill_pts     = cfg["SKILL_PTS"]
    cert_pts      = cfg["CERT_PTS"]
    qualified_min = cfg["QUALIFIED_MIN"]
    for_review_min = cfg["FOR_REVIEW_MIN"]

    score  = edu_scores.get(app.get("education", ""), 0)
    score += exp_scores.get(app.get("experience", ""), 0)

    # Position-aware scoring: relevant skills/certs get double points
    position = app.get("position", "")
    relevance = cfg.get("POSITION_RELEVANCE", {}).get(position, {})
    rel_skills = set(relevance.get("relevant_skills", []))
    rel_certs = set(relevance.get("relevant_certs", []))

    for skill in app.get("skills", []):
        score += skill_pts * 2 if skill in rel_skills else skill_pts

    for cert in app.get("certifications", []):
        score += cert_pts * 2 if cert in rel_certs else cert_pts

    if score >= qualified_min:
        status = "Qualified"
    elif score >= for_review_min:
        status = "For Review"
    else:
        status = "Disqualified"
    return score, status

def next_applicant_id():
    apps = load_applicants()
    return max((a["applicantID"] for a in apps), default=1000) + 1

def add_applicant(data):
    apps = load_applicants()
    data["applicantID"] = next_applicant_id()
    data["dateApplied"] = datetime.now().strftime("%Y-%m-%d")
    data["score"], data["status"] = compute_score(data)
    apps.append(data)
    save_applicants(apps)
    log_action("ADD_APPLICANT", data["applicantID"], f"{data['firstName']} {data['lastName']}")
    return data["applicantID"]

def update_applicant(app_id, data):
    apps = load_applicants()
    for i, a in enumerate(apps):
        if a["applicantID"] == app_id:
            data["applicantID"] = app_id
            data["dateApplied"] = a.get("dateApplied", datetime.now().strftime("%Y-%m-%d"))
            data["score"], data["status"] = compute_score(data)
            apps[i] = data
            break
    save_applicants(apps)
    log_action("UPDATE_APPLICANT", app_id, f"{data.get('firstName','')} {data.get('lastName','')}")

def delete_applicant(app_id):
    apps = load_applicants()
    apps = [a for a in apps if a["applicantID"] != app_id]
    save_applicants(apps)
    log_action("DELETE_APPLICANT", app_id)

def search_applicants(query):
    query = query.lower()
    return [a for a in load_applicants()
            if query in a["firstName"].lower()
            or query in a["lastName"].lower()
            or query in str(a["applicantID"])
            or query in a["position"].lower()
            or query in a["status"].lower()]

def export_to_csv(path, qualified_only=False):
    apps = load_applicants()
    if qualified_only:
        apps = [a for a in apps if a["status"] == "Qualified"]
    apps = sorted(apps, key=lambda x: x["score"], reverse=True)
    fields = ["applicantID","firstName","lastName","age","gender","contact",
              "email","position","education","experience","score","status","dateApplied"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(apps)
    log_action("EXPORT_CSV", path, f"qualified_only={qualified_only}, count={len(apps)}")
    return len(apps)

def get_stats():
    apps = load_applicants()
    total       = len(apps)
    qualified   = sum(1 for a in apps if a["status"] == "Qualified")
    for_review  = sum(1 for a in apps if a["status"] == "For Review")
    disqualified= sum(1 for a in apps if a["status"] == "Disqualified")
    return {"total": total, "qualified": qualified,
            "for_review": for_review, "disqualified": disqualified}