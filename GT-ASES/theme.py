"""
GT-ASES Theme — centralized colors, fonts, and style helpers.
Scoring and dropdown values are loaded from config.json via config_loader.
"""

# ── PALETTE ──────────────────────────────────────────────────────────────────
BG_ROOT      = "#0D1117"   # deepest background
BG_SIDEBAR   = "#0F1923"   # sidebar
BG_MAIN      = "#141C26"   # main content area
BG_CARD      = "#1A2332"   # cards / panels
BG_INPUT     = "#1E2A3A"   # input fields
BG_HOVER     = "#223044"   # hover state
BG_ROW_ALT  = "#182030"   # alternating table row

ACCENT       = "#00BFFF"   # Globe blue-cyan (primary accent)
ACCENT_DIM   = "#007DAA"   # dimmed accent
ACCENT_DARK  = "#004D6B"   # dark accent (selected sidebar)
SUCCESS      = "#2ECC71"   # qualified / green
WARNING      = "#F39C12"   # for review / amber
DANGER       = "#E74C3C"   # disqualified / red
GOLD         = "#F1C40F"   # rank #1

TEXT_PRIMARY  = "#E8F4FD"
TEXT_SECONDARY= "#8BAAC4"
TEXT_MUTED    = "#4A6A84"
TEXT_WHITE    = "#FFFFFF"
TEXT_DARK     = "#0D1117"

BORDER        = "#1E3A52"
BORDER_LIGHT  = "#2A4A64"

# ── FONTS ────────────────────────────────────────────────────────────────────
FONT_TITLE    = ("Segoe UI", 22, "bold")
FONT_SUBTITLE = ("Segoe UI", 13)
FONT_H1       = ("Segoe UI", 16, "bold")
FONT_H2       = ("Segoe UI", 13, "bold")
FONT_H3       = ("Segoe UI", 11, "bold")
FONT_BODY     = ("Segoe UI", 10)
FONT_SMALL    = ("Segoe UI", 9)
FONT_MONO     = ("Consolas", 10)
FONT_NAV      = ("Segoe UI", 10, "bold")
FONT_STAT     = ("Segoe UI", 28, "bold")

# ── STATUS COLORS ─────────────────────────────────────────────────────────────
STATUS_COLORS = {
    "Qualified":    SUCCESS,
    "For Review":   WARNING,
    "Disqualified": DANGER,
}

GENDER_OPTIONS = ["Male", "Female", "Prefer not to say"]

# ── SCORING & DROPDOWNS (loaded from config.json) ─────────────────────────────
from config_loader import load_config as _load_config
_cfg = _load_config()

EDU_SCORES        = _cfg["EDU_SCORES"]
EXP_SCORES        = _cfg["EXP_SCORES"]
SKILL_PTS         = _cfg["SKILL_PTS"]
CERT_PTS          = _cfg["CERT_PTS"]
QUALIFIED_MIN     = _cfg["QUALIFIED_MIN"]
FOR_REVIEW_MIN    = _cfg["FOR_REVIEW_MIN"]
POSITIONS         = _cfg["POSITIONS"]
SKILLS_LIST       = _cfg["SKILLS_LIST"]
CERTS_LIST        = _cfg["CERTS_LIST"]
EDUCATION_LEVELS  = list(_cfg["EDU_SCORES"].keys())
EXPERIENCE_LEVELS = list(_cfg["EXP_SCORES"].keys())