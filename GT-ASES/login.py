"""
GT-ASES — Login Window
"""

import tkinter as tk
from tkinter import messagebox
from theme import *
from data_manager import authenticate


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.win = tk.Toplevel(root)
        self.win.title("GT-ASES — Login")
        self.win.geometry("480x580")
        self.win.resizable(False, False)
        self.win.configure(bg=BG_ROOT)
        self.win.protocol("WM_DELETE_WINDOW", self._on_close)

        # Center window
        self.win.update_idletasks()
        x = (self.win.winfo_screenwidth()  // 2) - 240
        y = (self.win.winfo_screenheight() // 2) - 290
        self.win.geometry(f"480x580+{x}+{y}")

        self._build_ui()
        self.win.lift()
        self.win.focus_force()

    def _on_close(self):
        self.root.destroy()

    def _build_ui(self):
        # ── Top accent bar ─────────────────────────────────────────────────
        accent = tk.Frame(self.win, bg=ACCENT, height=4)
        accent.pack(fill="x")

        # ── Logo area ──────────────────────────────────────────────────────
        logo_frame = tk.Frame(self.win, bg=BG_ROOT)
        logo_frame.pack(pady=(48, 0))

        globe_lbl = tk.Label(logo_frame, text="●  GLOBE TELECOM",
                             font=("Segoe UI", 13, "bold"),
                             bg=BG_ROOT, fg=ACCENT)
        globe_lbl.pack()

        tk.Label(logo_frame, text="GT-ASES",
                 font=("Segoe UI", 36, "bold"),
                 bg=BG_ROOT, fg=TEXT_PRIMARY).pack(pady=(8, 0))

        tk.Label(logo_frame, text="Applicant Screening & Evaluation System",
                 font=FONT_SMALL, bg=BG_ROOT, fg=TEXT_SECONDARY).pack()

        # ── Divider ────────────────────────────────────────────────────────
        tk.Frame(self.win, bg=BORDER, height=1).pack(fill="x", padx=48, pady=32)

        # ── Form card ──────────────────────────────────────────────────────
        card = tk.Frame(self.win, bg=BG_CARD, padx=36, pady=32)
        card.pack(fill="x", padx=36)

        tk.Label(card, text="Sign in to your account",
                 font=FONT_H2, bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 20))

        # Username
        tk.Label(card, text="USERNAME", font=("Segoe UI", 8, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
        self.username_var = tk.StringVar()
        user_entry = tk.Entry(card, textvariable=self.username_var,
                              font=FONT_BODY, bg=BG_INPUT, fg=TEXT_PRIMARY,
                              insertbackground=ACCENT, relief="flat",
                              bd=0, highlightthickness=1,
                              highlightbackground=BORDER,
                              highlightcolor=ACCENT)
        user_entry.pack(fill="x", ipady=10, pady=(4, 16))

        # Password
        tk.Label(card, text="PASSWORD", font=("Segoe UI", 8, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
        self.password_var = tk.StringVar()
        pass_entry = tk.Entry(card, textvariable=self.password_var, show="●",
                              font=FONT_BODY, bg=BG_INPUT, fg=TEXT_PRIMARY,
                              insertbackground=ACCENT, relief="flat",
                              bd=0, highlightthickness=1,
                              highlightbackground=BORDER,
                              highlightcolor=ACCENT)
        pass_entry.pack(fill="x", ipady=10, pady=(4, 24))

        # Login button
        self.login_btn = tk.Button(card, text="SIGN IN",
                                   font=("Segoe UI", 11, "bold"),
                                   bg=ACCENT, fg=TEXT_DARK,
                                   activebackground=ACCENT_DIM,
                                   activeforeground=TEXT_WHITE,
                                   relief="flat", cursor="hand2",
                                   command=self._login)
        self.login_btn.pack(fill="x", ipady=12)

        # Error label
        self.error_var = tk.StringVar()
        tk.Label(card, textvariable=self.error_var,
                 font=FONT_SMALL, bg=BG_CARD, fg=DANGER).pack(pady=(12, 0))

        # ── Hint ───────────────────────────────────────────────────────────
        hint = tk.Frame(self.win, bg=BG_ROOT)
        hint.pack(pady=20)
        tk.Label(hint, text="Default credentials — Admin: admin / admin123   Staff: hrstaff / staff123",
                 font=("Segoe UI", 8), bg=BG_ROOT, fg=TEXT_MUTED).pack()

        # ── Bind Enter ─────────────────────────────────────────────────────
        self.win.bind("<Return>", lambda e: self._login())
        user_entry.focus_set()

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            self.error_var.set("Please enter username and password.")
            return

        user = authenticate(username, password)
        if user:
            self.error_var.set("")
            self.win.destroy()
            from dashboard import MainApp
            MainApp(self.root, user)
        else:
            self.error_var.set("Invalid username or password. Please try again.")
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
            self.password_var.set("")
