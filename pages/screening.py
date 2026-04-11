"""
GT-ASES — Screening & Ranking Page
"""

import tkinter as tk
from tkinter import ttk, messagebox
from theme import *
from data_manager import load_applicants, get_stats


class ScreeningPage:
    def __init__(self, parent, user, app):
        self.parent = parent
        self.user   = user
        self.app    = app
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self.parent, bg=BG_MAIN, padx=36, pady=24)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Screening & Ranking", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(side="left")

        run_btn = tk.Button(hdr, text="▶  Run Screening Now",
                            font=FONT_H3, bg=SUCCESS, fg=TEXT_WHITE,
                            relief="flat", cursor="hand2", padx=16, pady=8,
                            command=self._run_screening)
        run_btn.pack(side="right")

        # Info banner
        banner = tk.Frame(self.parent, bg=ACCENT_DARK, padx=24, pady=12)
        banner.pack(fill="x", padx=36, pady=(0, 20))
        tk.Label(banner, text="ℹ  Applicants are automatically scored based on Education, Experience, Skills, and Certifications.",
                 font=FONT_BODY, bg=ACCENT_DARK, fg=ACCENT).pack(side="left")

        # Scoring legend
        legend = tk.Frame(self.parent, bg=BG_MAIN, padx=36)
        legend.pack(fill="x", pady=(0, 16))

        score_info = [
            ("Education",      "High School:10  Vocational:20  Bachelor's:40  Master's:55  Doctorate:70", ACCENT),
            ("Experience",     "0yr:0  1-2yr:10  3-5yr:20  6-10yr:30  10+yr:40", WARNING),
            ("Skills",         "+5 pts each", SUCCESS),
            ("Certifications", "+5 pts each", GOLD),
            ("Qualified",      "80+ pts", SUCCESS),
            ("For Review",     "50–79 pts", WARNING),
            ("Disqualified",   "Below 50 pts", DANGER),
        ]
        for i, (label, detail, color) in enumerate(score_info):
            row = tk.Frame(legend, bg=BG_CARD, padx=12, pady=8)
            row.grid(row=i//2, column=i%2, sticky="ew", padx=(0,8), pady=4)
            legend.columnconfigure(i%2, weight=1)
            tk.Label(row, text=label, font=FONT_H3, bg=BG_CARD, fg=color).pack(side="left")
            tk.Label(row, text=detail, font=FONT_SMALL, bg=BG_CARD, fg=TEXT_MUTED).pack(side="left", padx=8)

        # Results table
        tk.Label(self.parent, text="Ranked Results", font=FONT_H1,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", padx=36, pady=(12, 8))

        table_frame = tk.Frame(self.parent, bg=BG_CARD, padx=36)
        table_frame.pack(fill="both", expand=True, padx=36, pady=(0, 24))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("GT.Treeview",
                         background=BG_CARD, foreground=TEXT_PRIMARY,
                         fieldbackground=BG_CARD, rowheight=40,
                         font=FONT_BODY, borderwidth=0)
        style.configure("GT.Treeview.Heading",
                         background=BG_SIDEBAR, foreground=ACCENT,
                         font=FONT_H3, relief="flat")
        style.map("GT.Treeview", background=[("selected", ACCENT_DARK)],
                  foreground=[("selected", ACCENT)])

        cols = ("Rank","ID","Name","Position","Education","Experience","Skills","Certs","Score","Status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="GT.Treeview")

        widths = [50, 60, 150, 180, 110, 100, 55, 50, 75, 120]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center" if col not in ("Name","Position") else "w", minwidth=40)

        vsb = ttk.Scrollbar(table_frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right",  fill="y")
        self.tree.pack(fill="both", expand=True)

        self.status_lbl = tk.Label(self.parent, text="Click 'Run Screening Now' to evaluate all applicants.",
                                    font=FONT_BODY, bg=BG_MAIN, fg=TEXT_MUTED)
        self.status_lbl.pack(pady=8)

        self._run_screening()

    def _run_screening(self):
        apps = sorted(load_applicants(), key=lambda x: x["score"], reverse=True)
        self.tree.delete(*self.tree.get_children())

        for rank, a in enumerate(apps, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, str(rank))
            status_symbol = {"Qualified":"✅","For Review":"⚠️","Disqualified":"❌"}.get(a["status"],"")
            self.tree.insert("", "end", values=(
                medal,
                f"#{a['applicantID']}",
                f"{a['firstName']} {a['lastName']}",
                a["position"],
                a["education"],
                a["experience"],
                len(a.get("skills", [])),
                len(a.get("certifications", [])),
                f"{a['score']} pts",
                f"{status_symbol} {a['status']}",
            ))

        stats = get_stats()
        self.status_lbl.configure(
            text=f"✅ Screening complete!  Total: {stats['total']}  |  "
                 f"Qualified: {stats['qualified']}  |  "
                 f"For Review: {stats['for_review']}  |  "
                 f"Disqualified: {stats['disqualified']}",
            fg=SUCCESS
        )
