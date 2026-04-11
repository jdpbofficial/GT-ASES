"""
GT-ASES — Globe Telecom Applicant Screening and Evaluation System
Phase 2: Local Desktop Application
Entry point — run this file to start the app.
"""

import tkinter as tk
from login import LoginWindow

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide root, login manages its own window
    app = LoginWindow(root)
    root.mainloop()
