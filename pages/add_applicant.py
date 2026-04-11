"""
GT-ASES — Add / Edit Applicant Page
"""

import tkinter as tk
import re
from tkinter import messagebox
from theme import *
from data_manager import add_applicant, update_applicant


class AddApplicantPage:
    def __init__(self, parent, user, app, edit_data=None, on_save=None):
        self.parent    = parent
        self.user      = user
        self.app       = app
        self.edit_data = edit_data
        self.on_save   = on_save
        self.is_edit   = edit_data is not None

        if self.is_edit:
            # Open as a modal dialog
            self._open_modal()
        else:
            self._build(parent)

    def _open_modal(self):
        self.modal = tk.Toplevel()
        self.modal.title("Edit Applicant")
        self.modal.geometry("700x700")
        self.modal.configure(bg=BG_MAIN)
        self.modal.grab_set()
        self.modal.update_idletasks()
        x = (self.modal.winfo_screenwidth()  // 2) - 350
        y = (self.modal.winfo_screenheight() // 2) - 350
        self.modal.geometry(f"700x700+{x}+{y}")
        self._build(self.modal)

    def _build(self, container):
        # Scrollable
        canvas = tk.Canvas(container, bg=BG_MAIN, highlightthickness=0)
        vsb = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        frame = tk.Frame(canvas, bg=BG_MAIN)
        win_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        def on_cfg(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(win_id, width=canvas.winfo_width())
        frame.bind("<Configure>", on_cfg)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        pad = tk.Frame(frame, bg=BG_MAIN, padx=36, pady=24)
        pad.pack(fill="both", expand=True)

        # Header
        title = "Edit Applicant" if self.is_edit else "Add New Applicant"
        tk.Label(pad, text=title, font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=(0, 24))

        self.vars = {}

        # ── Section: Personal Info ─────────────────────────────────────────
        self._section(pad, "Personal Information")
        row1 = tk.Frame(pad, bg=BG_MAIN)
        row1.pack(fill="x", pady=(0, 12))
        self._field(row1, "First Name",  "firstName",  side="left", expand=True)
        tk.Frame(row1, bg=BG_MAIN, width=16).pack(side="left")
        self._field(row1, "Last Name",   "lastName",   side="left", expand=True)

        row2 = tk.Frame(pad, bg=BG_MAIN)
        row2.pack(fill="x", pady=(0, 12))
        self._field(row2, "Age",         "age",        side="left", width=80)
        tk.Frame(row2, bg=BG_MAIN, width=16).pack(side="left")
        self._dropdown(row2, "Gender",   "gender",     GENDER_OPTIONS, side="left", expand=True)
        tk.Frame(row2, bg=BG_MAIN, width=16).pack(side="left")
        self._field(row2, "Contact No.", "contact",    side="left", expand=True)

        self._field(pad, "Email Address", "email")

        # ── Section: Job Application ───────────────────────────────────────
        self._section(pad, "Job Application")
        self._dropdown(pad, "Position Applied For", "position", POSITIONS)

        row3 = tk.Frame(pad, bg=BG_MAIN)
        row3.pack(fill="x", pady=(0, 12))
        self._dropdown(row3, "Educational Attainment", "education", EDUCATION_LEVELS, side="left", expand=True)
        tk.Frame(row3, bg=BG_MAIN, width=16).pack(side="left")
        self._dropdown(row3, "Years of Experience", "experience", EXPERIENCE_LEVELS, side="left", expand=True)

        # ── Section: Skills ────────────────────────────────────────────────
        self._section(pad, "Technical Skills (Select all that apply)")
        skills_frame = tk.Frame(pad, bg=BG_CARD, padx=16, pady=16)
        skills_frame.pack(fill="x", pady=(0, 12))
        self.skill_vars = {}
        existing_skills = self.edit_data.get("skills", []) if self.edit_data else []
        cols = 3
        for i, skill in enumerate(SKILLS_LIST):
            var = tk.BooleanVar(value=(skill in existing_skills))
            self.skill_vars[skill] = var
            cb = tk.Checkbutton(skills_frame, text=skill, variable=var,
                                font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRIMARY,
                                selectcolor=BG_INPUT, activebackground=BG_CARD,
                                activeforeground=ACCENT)
            cb.grid(row=i//cols, column=i%cols, sticky="w", padx=8, pady=4)

        # ── Section: Certifications ────────────────────────────────────────
        self._section(pad, "Certifications (Select all that apply)")
        cert_frame = tk.Frame(pad, bg=BG_CARD, padx=16, pady=16)
        cert_frame.pack(fill="x", pady=(0, 24))
        self.cert_vars = {}
        existing_certs = self.edit_data.get("certifications", []) if self.edit_data else []
        for i, cert in enumerate(CERTS_LIST):
            var = tk.BooleanVar(value=(cert in existing_certs))
            self.cert_vars[cert] = var
            cb = tk.Checkbutton(cert_frame, text=cert, variable=var,
                                font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRIMARY,
                                selectcolor=BG_INPUT, activebackground=BG_CARD,
                                activeforeground=ACCENT)
            cb.grid(row=i//3, column=i%3, sticky="w", padx=8, pady=4)

        # ── Buttons ────────────────────────────────────────────────────────
        btn_frame = tk.Frame(pad, bg=BG_MAIN)
        btn_frame.pack(fill="x", pady=(0, 32))

        if self.is_edit:
            cancel_btn = tk.Button(btn_frame, text="Cancel",
                                   font=FONT_H3, bg=BG_CARD, fg=TEXT_SECONDARY,
                                   relief="flat", cursor="hand2", padx=24, pady=12,
                                   command=lambda: self.modal.destroy())
            cancel_btn.pack(side="left", padx=(0, 12))

        save_lbl = "Update Applicant" if self.is_edit else "Save Applicant"
        save_btn = tk.Button(btn_frame, text=f"💾  {save_lbl}",
                             font=FONT_H3, bg=ACCENT, fg=TEXT_DARK,
                             relief="flat", cursor="hand2", padx=24, pady=12,
                             command=self._save)
        save_btn.pack(side="left")

        if not self.is_edit:
            clear_btn = tk.Button(btn_frame, text="🔄  Clear Form",
                                  font=FONT_H3, bg=BG_CARD, fg=TEXT_SECONDARY,
                                  relief="flat", cursor="hand2", padx=24, pady=12,
                                  command=self._clear)
            clear_btn.pack(side="left", padx=12)

        # Pre-fill for edit
        if self.edit_data:
            self._prefill()

    def _section(self, parent, title):
        f = tk.Frame(parent, bg=BG_MAIN)
        f.pack(fill="x", pady=(16, 8))
        tk.Label(f, text=title, font=FONT_H2,
                 bg=BG_MAIN, fg=ACCENT).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(12, 0), pady=6)

    def _field(self, parent, label, key, side="top", expand=False, width=None):
        container = tk.Frame(parent, bg=BG_MAIN)
        if side == "left":
            container.pack(side="left", expand=expand, fill="x")
        else:
            container.pack(fill="x", pady=(0, 12))

        tk.Label(container, text=label.upper(), font=("Segoe UI", 8, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")
        var = tk.StringVar()
        kw = {"font": FONT_BODY, "bg": BG_INPUT, "fg": TEXT_PRIMARY,
              "insertbackground": ACCENT, "relief": "flat",
              "highlightthickness": 1, "highlightbackground": BORDER,
              "highlightcolor": ACCENT, "textvariable": var}
        if width:
            kw["width"] = width
        e = tk.Entry(container, **kw)
        e.pack(fill="x", ipady=9, pady=(4, 0))
        self.vars[key] = var

    def _dropdown(self, parent, label, key, options, side="top", expand=False):
        container = tk.Frame(parent, bg=BG_MAIN)
        if side == "left":
            container.pack(side="left", expand=expand, fill="x")
        else:
            container.pack(fill="x", pady=(0, 12))

        tk.Label(container, text=label.upper(), font=("Segoe UI", 8, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")
        var = tk.StringVar(value=options[0])
        from tkinter import ttk
        style = ttk.Style()
        style.configure("GT.TCombobox", fieldbackground=BG_INPUT, background=BG_INPUT,
                         foreground=TEXT_PRIMARY, arrowcolor=ACCENT)
        cb = ttk.Combobox(container, textvariable=var, values=options,
                          font=FONT_BODY, state="readonly", style="GT.TCombobox")
        cb.pack(fill="x", ipady=8, pady=(4, 0))
        self.vars[key] = var

    def _prefill(self):
        d = self.edit_data
        for key, var in self.vars.items():
            if key in d:
                var.set(str(d[key]))

    def _clear(self):
        if not messagebox.askyesno("Clear Form", "Are you sure you want to clear all fields?"):
            return
        for var in self.vars.values():
            var.set("")
        for v in self.skill_vars.values():
            v.set(False)
        for v in self.cert_vars.values():
            v.set(False)

    def _save(self):
        # Validation
        required = ["firstName", "lastName", "age", "contact", "email", "position", "education", "experience"]
        for key in required:
            val = self.vars.get(key, tk.StringVar()).get().strip()
            if not val:
                messagebox.showwarning("Incomplete Form", f"Please fill in: {key.replace('_',' ').title()}")
                return

        try:
            age = int(self.vars["age"].get().strip())
            if not (16 <= age <= 70):
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Age", "Please enter a valid age (16–70).")
            return

        data = {
            "firstName":      self.vars["firstName"].get().strip(),
            "lastName":       self.vars["lastName"].get().strip(),
            "age":            age,
            "gender":         self.vars["gender"].get(),
            "contact":        self.vars["contact"].get().strip(),
            "email":          self.vars["email"].get().strip(),
            "position":       self.vars["position"].get(),
            "education":      self.vars["education"].get(),
            "experience":     self.vars["experience"].get(),
            "skills":         [s for s, v in self.skill_vars.items() if v.get()],
            "certifications": [c for c, v in self.cert_vars.items() if v.get()],
        }

        if self.is_edit:
            update_applicant(self.edit_data["applicantID"], data)
            messagebox.showinfo("Updated", f"Applicant {data['firstName']} {data['lastName']} has been updated successfully!")
            if self.on_save:
                self.on_save()
            self.modal.destroy()
        else:
            app_id = add_applicant(data)
            messagebox.showinfo("Saved", f"Applicant {data['firstName']} {data['lastName']} added successfully!\nApplicant ID: #{app_id}")
            self._clear()
