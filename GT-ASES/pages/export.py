"""
GT-ASES — Export Page
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from theme import *
from data_manager import export_to_csv, get_stats
import os


class ExportPage:
    def __init__(self, parent, user, app):
        self.parent = parent
        self.user   = user
        self.app    = app
        self._build()

    def _build(self):
        pad = tk.Frame(self.parent, bg=BG_MAIN, padx=36, pady=32)
        pad.pack(fill="both", expand=True)

        tk.Label(pad, text="Export Reports", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 24))

        # Stats summary
        stats = get_stats()
        summary = tk.Frame(pad, bg=BG_CARD, padx=24, pady=20)
        summary.pack(fill="x", pady=(0, 28))

        tk.Label(summary, text="Current Data Summary", font=FONT_H2,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 12))

        stat_row = tk.Frame(summary, bg=BG_CARD)
        stat_row.pack(fill="x")

        for label, val, color in [
            ("Total Applicants", stats["total"],        ACCENT),
            ("Qualified",        stats["qualified"],    SUCCESS),
            ("For Review",       stats["for_review"],   WARNING),
            ("Disqualified",     stats["disqualified"], DANGER),
        ]:
            col = tk.Frame(stat_row, bg=BG_INPUT, padx=20, pady=14)
            col.pack(side="left", expand=True, fill="x", padx=(0, 12))
            tk.Label(col, text=str(val), font=FONT_STAT, bg=BG_INPUT, fg=color).pack()
            tk.Label(col, text=label, font=FONT_SMALL, bg=BG_INPUT, fg=TEXT_MUTED).pack()

        # Export options
        tk.Label(pad, text="Export Options", font=FONT_H1,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 16))

        options = [
            ("📋  Export All Applicants",
             "Exports the complete list of all applicants sorted by score (highest to lowest).",
             ACCENT, False),
            ("✅  Export Qualified Only",
             "Exports only applicants with a status of 'Qualified' (score 80+), sorted by rank.",
             SUCCESS, True),
        ]

        for title, desc, color, qual_only in options:
            card = tk.Frame(pad, bg=BG_CARD, padx=24, pady=20)
            card.pack(fill="x", pady=(0, 16))

            left = tk.Frame(card, bg=BG_CARD)
            left.pack(side="left", fill="both", expand=True)

            tk.Label(left, text=title, font=FONT_H2, bg=BG_CARD, fg=color).pack(anchor="w")
            tk.Label(left, text=desc,  font=FONT_BODY, bg=BG_CARD, fg=TEXT_MUTED,
                     wraplength=600, justify="left").pack(anchor="w", pady=(4, 0))

            q = qual_only
            btn = tk.Button(card, text="Export CSV →",
                            font=FONT_H3, bg=color,
                            fg=TEXT_DARK if color == ACCENT else TEXT_WHITE,
                            relief="flat", cursor="hand2", padx=20, pady=10,
                            command=lambda qo=q: self._export(qo))
            btn.pack(side="right", padx=(16, 0))

        # Result label
        self.result_lbl = tk.Label(pad, text="", font=FONT_BODY, bg=BG_MAIN, fg=SUCCESS)
        self.result_lbl.pack(anchor="w", pady=16)

        # Instructions
        info = tk.Frame(pad, bg=BG_CARD, padx=20, pady=16)
        info.pack(fill="x")
        tk.Label(info, text="📌  Export Tips", font=FONT_H3, bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        for tip in [
            "CSV files can be opened in Microsoft Excel or Google Sheets.",
            "Exported data is sorted from highest to lowest score.",
            "You can export multiple times — each export is a fresh snapshot.",
        ]:
            tk.Label(info, text=f"  •  {tip}", font=FONT_BODY,
                     bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=2)

    def _export(self, qualified_only):
        label = "qualified_applicants" if qualified_only else "all_applicants"
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile=f"GT-ASES_{label}.csv",
            title="Save Export File"
        )
        if not path:
            return
        try:
            count = export_to_csv(path, qualified_only)
            self.result_lbl.configure(
                text=f"✅  Successfully exported {count} applicant(s) to: {os.path.basename(path)}"
            )
            messagebox.showinfo("Export Successful",
                                f"Exported {count} applicant(s) to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
