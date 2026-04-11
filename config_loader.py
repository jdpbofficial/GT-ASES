"""
GT-ASES Config Loader — loads scoring rules and option lists from config.json.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

_cache = None


def load_config():
    global _cache
    if _cache is not None:
        return _cache
    if not os.path.exists(CONFIG_FILE):
        _generate_default()
    with open(CONFIG_FILE, "r") as f:
        _cache = json.load(f)
    return _cache


def reload_config():
    global _cache
    _cache = None
    return load_config()


def _generate_default():
    default = {
        "EDU_SCORES": {"High School": 10, "Vocational": 20, "Bachelor's": 40,
                       "Master's": 55, "Doctorate": 70},
        "EXP_SCORES": {"0 years": 0, "1-2 years": 10, "3-5 years": 20,
                       "6-10 years": 30, "10+ years": 40},
        "SKILL_PTS": 5, "CERT_PTS": 5,
        "QUALIFIED_MIN": 80, "FOR_REVIEW_MIN": 50,
        "POSITIONS": ["Junior Software Developer", "Network Engineer",
                      "IT Support Specialist", "Cybersecurity Analyst",
                      "Database Administrator", "Systems Analyst",
                      "Project Manager (IT)"],
        "SKILLS_LIST": ["Python", "Java", "C++", "JavaScript", "HTML/CSS",
                        "SQL", "Networking", "Cybersecurity", "Database Admin",
                        "Web Development", "Mobile Development", "Cloud Computing",
                        "Machine Learning", "Data Analysis", "System Administration"],
        "CERTS_LIST": ["CCNA", "CompTIA A+", "CompTIA Security+", "AWS Certified",
                       "PMP", "TESDA NC II", "Oracle Certified", "Microsoft Certified",
                       "Google IT Support", "Cisco CCNP"],
        "POSITION_RELEVANCE": {}
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(default, f, indent=2)


# Convenience accessors
def get_edu_scores():
    return load_config()["EDU_SCORES"]

def get_exp_scores():
    return load_config()["EXP_SCORES"]

def get_skill_pts():
    return load_config()["SKILL_PTS"]

def get_cert_pts():
    return load_config()["CERT_PTS"]

def get_qualified_min():
    return load_config()["QUALIFIED_MIN"]

def get_for_review_min():
    return load_config()["FOR_REVIEW_MIN"]

def get_positions():
    return load_config()["POSITIONS"]

def get_skills_list():
    return load_config()["SKILLS_LIST"]

def get_certs_list():
    return load_config()["CERTS_LIST"]

def get_education_levels():
    return list(load_config()["EDU_SCORES"].keys())

def get_experience_levels():
    return list(load_config()["EXP_SCORES"].keys())

def get_position_relevance():
    return load_config().get("POSITION_RELEVANCE", {})