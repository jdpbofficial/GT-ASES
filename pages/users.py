"""
GT-ASES — User Management Page (Admin Only)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from theme import *
from data_manager import load_users, add_user, delete_user


class UsersPage:
    def __init__(self, parent, user, app):
        self.parent = parent
        self.user   = user
        self.app    = app
        self._build()
        self._load_table()

    def _build(self):
        pad = tk.Frame(self.parent, bg=BG_MAIN, padx=36, pady=24)
        pad.pack(fill="both", expand=True)

        tk.Label(pad, text="User Management", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 4))
        tk.Label(pad, text="Admin access only — manage HR staff accounts",
                 font=FONT_BODY, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 24))

        body = tk.Frame(pad, bg=BG_MAIN)
        body.pack(fill="both", expand=True)

        # ── Left: user list ────────────────────────────────────────────────
        left = tk.Frame(body, bg=BG_MAIN)
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))

        tk.Label(left, text="HR Accounts", font=FONT_H2,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 12))

        table_frame = tk.Frame(left, bg=BG_CARD)
        table_frame.pack(fill="both", expand=True)

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

        cols = ("ID", "Full Name", "Username", "Role")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings",
                                  style="GT.Treeview", height=10)
        widths = [60, 200, 160, 100]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center" if col not in ("Full Name",) else "w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        del_btn = tk.Button(left, text="🗑  Delete Selected User",
                            font=FONT_SMALL, bg=DANGER, fg=TEXT_WHITE,
                            relief="flat", cursor="hand2", padx=14, pady=8,
                            command=self._delete_user)
        del_btn.pack(anchor="w", pady=(12, 0))

        # ── Right: add user form ───────────────────────────────────────────
        right = tk.Frame(body, bg=BG_CARD, padx=24, pady=24, width=280)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="Add New User", font=FONT_H2,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 20))

        self.form_vars = {}

        for label, key in [("Full Name", "fullName"), ("Username", "username"), ("Password", "password")]:
            tk.Label(right, text=label.upper(), font=("Segoe UI", 8, "bold"),
                     bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
            var = tk.StringVar()
            show = "●" if key == "password" else ""
            e = tk.Entry(right, textvariable=var, show=show,
                         font=FONT_BODY, bg=BG_INPUT, fg=TEXT_PRIMARY,
                         insertbackground=ACCENT, relief="flat",
                         highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=ACCENT)
            e.pack(fill="x", ipady=9, pady=(4, 16))
            self.form_vars[key] = var

        tk.Label(right, text="ROLE", font=("Segoe UI", 8, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
        self.role_var = tk.StringVar(value="Staff")
        role_cb = ttk.Combobox(right, textvariable=self.role_var,
                                values=["Staff", "Admin"],
                                font=FONT_BODY, state="readonly")
        role_cb.pack(fill="x", ipady=8, pady=(4, 24))

        add_btn = tk.Button(right, text="➕  Add User",
                            font=FONT_H3, bg=ACCENT, fg=TEXT_DARK,
                            relief="flat", cursor="hand2", pady=12,
                            command=self._add_user)
        add_btn.pack(fill="x")

        self.msg_lbl = tk.Label(right, text="", font=FONT_SMALL,
                                 bg=BG_CARD, fg=SUCCESS, wraplength=220)
        self.msg_lbl.pack(pady=12)

    def _load_table(self):
        self.tree.delete(*self.tree.get_children())
        for u in load_users():
            self.tree.insert("", "end", iid=str(u["userID"]), values=(
                f"#{u['userID']}", u["fullName"], u["username"], u["role"]
            ))

    def _add_user(self):
        full  = self.form_vars["fullName"].get().strip()
        uname = self.form_vars["username"].get().strip()
        pwd   = self.form_vars["password"].get().strip()
        role  = self.role_var.get()

        if not full or not uname or not pwd:
            self.msg_lbl.configure(text="Please fill in all fields.", fg=DANGER)
            return

        ok, msg = add_user(full, uname, pwd, role)
        self.msg_lbl.configure(text=msg, fg=SUCCESS if ok else DANGER)
        if ok:
            for v in self.form_vars.values():
                v.set("")
            self._load_table()

    def _delete_user(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a user to delete.")
            return
        uid = int(sel[0])
        if uid == self.user["userID"]:
            messagebox.showerror("Error", "You cannot delete your own account.")
            return
        users = load_users()
        u = next((x for x in users if x["userID"] == uid), None)
        if u and messagebox.askyesno("Confirm Delete", f"Delete user '{u['username']}'?"):
            delete_user(uid)
            self._load_table()
