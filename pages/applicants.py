"""
GT-ASES — Applicants List Page (View, Search, Edit, Delete)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from theme import *
from data_manager import load_applicants, delete_applicant


class ApplicantsPage:
    def __init__(self, parent, user, app):
        self.parent = parent
        self.user   = user
        self.app    = app
        self.all_apps = []
        self._build()
        self._load_table()

    def _build(self):
        # Header row
        hdr = tk.Frame(self.parent, bg=BG_MAIN, padx=36, pady=24)
        hdr.pack(fill="x")

        tk.Label(hdr, text="Applicant Records", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(side="left")

        add_btn = tk.Button(hdr, text="➕  Add Applicant",
                            font=FONT_H3, bg=ACCENT, fg=TEXT_DARK,
                            relief="flat", cursor="hand2", padx=16, pady=8,
                            command=lambda: self.app.navigate("Add Applicant"))
        add_btn.pack(side="right")

        # Search bar
        search_frame = tk.Frame(self.parent, bg=BG_MAIN, padx=36)
        search_frame.pack(fill="x", pady=(0, 12))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._filter())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                font=FONT_BODY, bg=BG_INPUT, fg=TEXT_PRIMARY,
                                insertbackground=ACCENT, relief="flat",
                                highlightthickness=1, highlightbackground=BORDER,
                                highlightcolor=ACCENT)
        search_entry.pack(side="left", fill="x", expand=True, ipady=9)
        tk.Label(search_frame, text="🔍  Search by name, ID, position, or status",
                 font=FONT_SMALL, bg=BG_MAIN, fg=TEXT_MUTED).pack(side="left", padx=12)

        # Filter buttons
        filter_frame = tk.Frame(self.parent, bg=BG_MAIN, padx=36)
        filter_frame.pack(fill="x", pady=(0, 12))
        self.filter_var = tk.StringVar(value="All")
        for label in ["All", "Qualified", "For Review", "Disqualified"]:
            color = {"All": ACCENT, "Qualified": SUCCESS, "For Review": WARNING, "Disqualified": DANGER}.get(label, ACCENT)
            btn = tk.Button(filter_frame, text=label, font=FONT_SMALL,
                            bg=BG_CARD, fg=color,
                            relief="flat", cursor="hand2", padx=14, pady=6,
                            command=lambda l=label: self._set_filter(l))
            btn.pack(side="left", padx=(0, 8))

        # Table
        table_frame = tk.Frame(self.parent, bg=BG_CARD, padx=36, pady=0)
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

        cols = ("ID", "Name", "Age", "Position", "Education", "Experience", "Score", "Status", "Date Applied")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings",
                                 style="GT.Treeview")

        widths = [65, 160, 45, 190, 120, 100, 65, 120, 100]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col, command=lambda c=col: self._sort(c))
            self.tree.column(col, width=w, anchor="center" if col not in ("Name","Position") else "w", minwidth=40)

        vsb = ttk.Scrollbar(table_frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right",  fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self._on_double_click)

        # Bottom action bar
        action_bar = tk.Frame(self.parent, bg=BG_MAIN, padx=36, pady=12)
        action_bar.pack(fill="x")

        self.count_lbl = tk.Label(action_bar, text="", font=FONT_BODY,
                                   bg=BG_MAIN, fg=TEXT_MUTED)
        self.count_lbl.pack(side="left")

        if self.user["role"] == "Admin":
            del_btn = tk.Button(action_bar, text="🗑  Delete Selected",
                                font=FONT_SMALL, bg=DANGER, fg=TEXT_WHITE,
                                relief="flat", cursor="hand2", padx=14, pady=6,
                                command=self._delete_selected)
            del_btn.pack(side="right")

        edit_btn = tk.Button(action_bar, text="✏️  Edit Selected",
                             font=FONT_SMALL, bg=WARNING, fg=TEXT_DARK,
                             relief="flat", cursor="hand2", padx=14, pady=6,
                             command=self._edit_selected)
        edit_btn.pack(side="right", padx=(0, 8))

    def _load_table(self, apps=None):
        if apps is None:
            self.all_apps = sorted(load_applicants(), key=lambda x: x["score"], reverse=True)
            apps = self.all_apps
        self.tree.delete(*self.tree.get_children())
        for a in apps:
            status_symbol = {"Qualified":"✅","For Review":"⚠️","Disqualified":"❌"}.get(a["status"],"")
            self.tree.insert("", "end", iid=str(a["applicantID"]), values=(
                f"#{a['applicantID']}",
                f"{a['firstName']} {a['lastName']}",
                a["age"],
                a["position"],
                a["education"],
                a["experience"],
                f"{a['score']} pts",
                f"{status_symbol} {a['status']}",
                a["dateApplied"],
            ))
        self.count_lbl.configure(text=f"Showing {len(apps)} applicant(s)")

    def _filter(self):
        q = self.search_var.get().lower()
        f = self.filter_var.get()
        apps = self.all_apps
        if q:
            apps = [a for a in apps if q in f"{a['firstName']} {a['lastName']}".lower()
                    or q in str(a["applicantID"])
                    or q in a["position"].lower()
                    or q in a["status"].lower()]
        if f != "All":
            apps = [a for a in apps if a["status"] == f]
        self._load_table(apps)

    def _set_filter(self, label):
        self.filter_var.set(label)
        self._filter()

    def _sort(self, col):
        apps = self.all_apps[:]
        key_map = {"Score": lambda a: a["score"], "Name": lambda a: a["lastName"],
                   "Date Applied": lambda a: a["dateApplied"], "ID": lambda a: a["applicantID"]}
        apps.sort(key=key_map.get(col, lambda a: str(a.get(col.lower().replace(" ",""), ""))), reverse=True)
        self._load_table(apps)

    def _get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select an applicant first.")
            return None
        return int(sel[0])

    def _on_double_click(self, event):
        self._edit_selected()

    def _edit_selected(self):
        app_id = self._get_selected_id()
        if app_id is None:
            return
        app_data = next((a for a in self.all_apps if a["applicantID"] == app_id), None)
        if app_data:
            from pages.add_applicant import AddApplicantPage
            AddApplicantPage(self.parent, self.user, self.app, edit_data=app_data,
                             on_save=lambda: self._load_table())

    def _delete_selected(self):
        app_id = self._get_selected_id()
        if app_id is None:
            return
        app_data = next((a for a in self.all_apps if a["applicantID"] == app_id), None)
        if not app_data:
            return
        name = f"{app_data['firstName']} {app_data['lastName']}"
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete applicant:\n\n{name} (#{app_id})?\n\nThis action cannot be undone.")
        if confirm:
            delete_applicant(app_id)
            messagebox.showinfo("Deleted", f"Applicant {name} has been removed.")
            self._load_table()
