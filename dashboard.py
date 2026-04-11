"""
GT-ASES — Main Application Shell (Dashboard + Sidebar Navigation)
"""

import tkinter as tk
from tkinter import ttk
from theme import *
from data_manager import get_stats, load_applicants, set_current_user


class MainApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.deiconify()
        self.root.title(f"GT-ASES — Globe Telecom Applicant Screening System")
        self.root.geometry("1280x780")
        self.root.minsize(1100, 680)
        self.root.configure(bg=BG_ROOT)
        set_current_user(user)
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  // 2) - 640
        y = (self.root.winfo_screenheight() // 2) - 390
        self.root.geometry(f"1280x780+{x}+{y}")

        self.current_page = None
        self.nav_buttons  = {}
        self._build_shell()
        self._show_page("Dashboard")

    # ── SHELL ─────────────────────────────────────────────────────────────────
    def _build_shell(self):
        # Top bar
        topbar = tk.Frame(self.root, bg=BG_SIDEBAR, height=52)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        tk.Frame(topbar, bg=ACCENT, width=4).pack(side="left", fill="y")
        tk.Label(topbar, text="  ●  GT-ASES", font=("Segoe UI", 13, "bold"),
                 bg=BG_SIDEBAR, fg=ACCENT).pack(side="left", padx=(12, 0))
        tk.Label(topbar, text="Globe Telecom Applicant Screening & Evaluation System",
                 font=FONT_SMALL, bg=BG_SIDEBAR, fg=TEXT_MUTED).pack(side="left", padx=12)

        # User info + logout
        user_frame = tk.Frame(topbar, bg=BG_SIDEBAR)
        user_frame.pack(side="right", padx=20)
        tk.Label(user_frame, text=f"{self.user['fullName']}",
                 font=FONT_H3, bg=BG_SIDEBAR, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))
        role_badge = tk.Label(user_frame,
                              text=f" {self.user['role'].upper()} ",
                              font=("Segoe UI", 8, "bold"),
                              bg=ACCENT_DARK, fg=ACCENT, padx=6, pady=2)
        role_badge.pack(side="left", padx=(0, 16))
        logout_btn = tk.Button(user_frame, text="⏻  Logout",
                               font=FONT_SMALL, bg=BG_CARD, fg=DANGER,
                               activebackground=DANGER, activeforeground=TEXT_WHITE,
                               relief="flat", cursor="hand2", padx=10, pady=4,
                               command=self._logout)
        logout_btn.pack(side="left")

        # Body
        body = tk.Frame(self.root, bg=BG_ROOT)
        body.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(body, bg=BG_SIDEBAR, width=220)
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        # Content area
        self.content = tk.Frame(body, bg=BG_MAIN)
        self.content.pack(fill="both", expand=True, side="left")

    def _build_sidebar(self):
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x")

        nav_items = [
            ("Dashboard",    "🏠"),
            ("Applicants",   "📋"),
            ("Add Applicant","➕"),
            ("Screening",    "🔍"),
            ("Export",       "📤"),
        ]
        if self.user["role"] == "Admin":
            nav_items.append(("Users", "👥"))

        tk.Frame(self.sidebar, bg=BG_SIDEBAR, height=16).pack()

        for label, icon in nav_items:
            btn_frame = tk.Frame(self.sidebar, bg=BG_SIDEBAR)
            btn_frame.pack(fill="x")

            btn = tk.Button(btn_frame,
                            text=f"  {icon}   {label}",
                            font=FONT_NAV,
                            bg=BG_SIDEBAR, fg=TEXT_SECONDARY,
                            activebackground=ACCENT_DARK,
                            activeforeground=ACCENT,
                            relief="flat", anchor="w",
                            cursor="hand2", pady=14,
                            command=lambda l=label: self._show_page(l))
            btn.pack(fill="x")
            self.nav_buttons[label] = btn

        # Bottom user section
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", side="bottom", pady=(0, 0))
        bottom = tk.Frame(self.sidebar, bg=BG_SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=16, pady=16)
        tk.Label(bottom, text=f"Logged in as", font=FONT_SMALL,
                 bg=BG_SIDEBAR, fg=TEXT_MUTED).pack(anchor="w")
        tk.Label(bottom, text=f"{self.user['username']}",
                 font=FONT_H3, bg=BG_SIDEBAR, fg=ACCENT).pack(anchor="w")

    def _set_active_nav(self, label):
        for name, btn in self.nav_buttons.items():
            if name == label:
                btn.configure(bg=ACCENT_DARK, fg=ACCENT)
            else:
                btn.configure(bg=BG_SIDEBAR, fg=TEXT_SECONDARY)

    # ── PAGE ROUTING ──────────────────────────────────────────────────────────
    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _show_page(self, name):
        self._set_active_nav(name)
        self._clear_content()
        self.current_page = name

        if name == "Dashboard":
            DashboardPage(self.content, self.user, self)
        elif name == "Applicants":
            from pages.applicants import ApplicantsPage
            ApplicantsPage(self.content, self.user, self)
        elif name == "Add Applicant":
            from pages.add_applicant import AddApplicantPage
            AddApplicantPage(self.content, self.user, self)
        elif name == "Screening":
            from pages.screening import ScreeningPage
            ScreeningPage(self.content, self.user, self)
        elif name == "Export":
            from pages.export import ExportPage
            ExportPage(self.content, self.user, self)
        elif name == "Users" and self.user["role"] == "Admin":
            from pages.users import UsersPage
            UsersPage(self.content, self.user, self)

    def _logout(self):
        set_current_user(None)
        # Destroy all widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        # Unbind mousewheel to prevent stale references
        self.root.unbind_all("<MouseWheel>")
        # Re-hide the root window and show login
        self.root.withdraw()
        from login import LoginWindow
        LoginWindow(self.root)

    def navigate(self, page):
        self._show_page(page)


# ── DASHBOARD PAGE ────────────────────────────────────────────────────────────
class DashboardPage:
    def __init__(self, parent, user, app):
        self.parent = parent
        self.user   = user
        self.app    = app
        self._build()

    def _build(self):
        # Scrollable canvas
        canvas = tk.Canvas(self.parent, bg=BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        frame = tk.Frame(canvas, bg=BG_MAIN)
        canvas_win = canvas.create_window((0, 0), window=frame, anchor="nw")

        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_win, width=canvas.winfo_width())
        frame.bind("<Configure>", on_configure)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_win, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        pad = tk.Frame(frame, bg=BG_MAIN)
        pad.pack(fill="both", expand=True, padx=36, pady=32)

        # ── Header ────────────────────────────────────────────────────────
        hdr = tk.Frame(pad, bg=BG_MAIN)
        hdr.pack(fill="x", pady=(0, 28))
        tk.Label(hdr, text="Dashboard", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(side="left")
        from datetime import datetime
        tk.Label(hdr, text=datetime.now().strftime("%B %d, %Y"),
                 font=FONT_BODY, bg=BG_MAIN, fg=TEXT_MUTED).pack(side="right", pady=(10, 0))

        # ── Stat cards ────────────────────────────────────────────────────
        stats = get_stats()
        cards_frame = tk.Frame(pad, bg=BG_MAIN)
        cards_frame.pack(fill="x", pady=(0, 28))

        stat_data = [
            ("Total Applicants", stats["total"],       ACCENT,   "👥"),
            ("Qualified",        stats["qualified"],   SUCCESS,  "✅"),
            ("For Review",       stats["for_review"],  WARNING,  "⚠️"),
            ("Disqualified",     stats["disqualified"],DANGER,   "❌"),
        ]

        for i, (label, value, color, icon) in enumerate(stat_data):
            col = tk.Frame(cards_frame, bg=BG_MAIN)
            col.grid(row=0, column=i, padx=(0, 16), sticky="ew")
            cards_frame.columnconfigure(i, weight=1)

            card = tk.Frame(col, bg=BG_CARD, padx=24, pady=20)
            card.pack(fill="both", expand=True)

            # Top color accent
            tk.Frame(card, bg=color, height=3).pack(fill="x", pady=(0, 16))

            top_row = tk.Frame(card, bg=BG_CARD)
            top_row.pack(fill="x")
            tk.Label(top_row, text=icon, font=("Segoe UI", 20),
                     bg=BG_CARD, fg=color).pack(side="left")
            tk.Label(top_row, text=str(value), font=FONT_STAT,
                     bg=BG_CARD, fg=color).pack(side="right")

            tk.Label(card, text=label, font=FONT_H3,
                     bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor="w", pady=(8, 0))

        # ── Recent applicants table ────────────────────────────────────────
        tk.Label(pad, text="Recent Applicants", font=FONT_H1,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 12))

        table_frame = tk.Frame(pad, bg=BG_CARD)
        table_frame.pack(fill="x")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("GT.Treeview",
                         background=BG_CARD, foreground=TEXT_PRIMARY,
                         fieldbackground=BG_CARD, rowheight=38,
                         font=FONT_BODY, borderwidth=0)
        style.configure("GT.Treeview.Heading",
                         background=BG_SIDEBAR, foreground=ACCENT,
                         font=FONT_H3, relief="flat", borderwidth=0)
        style.map("GT.Treeview", background=[("selected", ACCENT_DARK)],
                  foreground=[("selected", ACCENT)])

        cols = ("ID", "Name", "Position", "Education", "Score", "Status", "Date")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings",
                            style="GT.Treeview", height=8)

        widths = [70, 160, 200, 130, 70, 110, 100]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center" if col not in ("Name","Position") else "w")

        apps = sorted(load_applicants(), key=lambda x: x["dateApplied"], reverse=True)[:10]
        for a in apps:
            status_symbol = {"Qualified":"✅","For Review":"⚠️","Disqualified":"❌"}.get(a["status"],"")
            tree.insert("", "end", values=(
                f"#{a['applicantID']}",
                f"{a['firstName']} {a['lastName']}",
                a["position"],
                a["education"],
                f"{a['score']} pts",
                f"{status_symbol} {a['status']}",
                a["dateApplied"],
            ))

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        # ── Quick actions ─────────────────────────────────────────────────
        tk.Label(pad, text="Quick Actions", font=FONT_H1,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=(28, 12))

        qa_frame = tk.Frame(pad, bg=BG_MAIN)
        qa_frame.pack(fill="x")

        actions = [
            ("➕  Add New Applicant", ACCENT,   lambda: self.app.navigate("Add Applicant")),
            ("🔍  Run Screening",     SUCCESS,  lambda: self.app.navigate("Screening")),
            ("📋  View All Records",  WARNING,  lambda: self.app.navigate("Applicants")),
            ("📤  Export Reports",    ACCENT_DIM,lambda: self.app.navigate("Export")),
        ]
        for i, (label, color, cmd) in enumerate(actions):
            btn = tk.Button(qa_frame, text=label, font=FONT_H3,
                            bg=color, fg=TEXT_DARK if color == ACCENT else TEXT_WHITE,
                            activebackground=BG_HOVER, activeforeground=TEXT_WHITE,
                            relief="flat", cursor="hand2", pady=14, padx=20,
                            command=cmd)
            btn.grid(row=0, column=i, padx=(0, 12), sticky="ew")
            qa_frame.columnconfigure(i, weight=1)
