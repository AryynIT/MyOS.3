import tkinter as tk
from tkinter import filedialog, messagebox
from config import CONFIG
from theme import THEME


class SettingsApp:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=THEME.get("window"))
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame, text="⚙️  MiniOS Settings",
            bg=THEME.get("window"), fg=THEME.get("accent"),
            font=("Courier", 16, "bold")
        ).pack(pady=15)

        # Section: Appearance
        self.section("Appearance")

        theme_row = self.row()
        tk.Label(theme_row, text="Theme:", bg=THEME.get("window"),
                 fg=THEME.get("text"), font=("Courier", 10),
                 width=20, anchor="w").pack(side="left", padx=20)
        self.theme_btn = tk.Button(
            theme_row, text=THEME.current.upper(),
            bg=THEME.get("button"), fg=THEME.get("text"),
            relief="flat", font=("Courier", 9), padx=10, cursor="hand2",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="left")

        # Section: User
        self.section("User")

        pass_row = self.row()
        tk.Label(pass_row, text="Password:", bg=THEME.get("window"),
                 fg=THEME.get("text"), font=("Courier", 10),
                 width=20, anchor="w").pack(side="left", padx=20)
        self.pass_entry = tk.Entry(
            pass_row, show="●", bg=THEME.get("entry_bg"),
            fg=THEME.get("text"), font=("Courier", 10),
            insertbackground=THEME.get("accent"), relief="flat"
        )
        self.pass_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
        tk.Button(
            pass_row, text="Save", bg=THEME.get("button"),
            fg=THEME.get("text"), relief="flat", font=("Courier", 9),
            padx=10, cursor="hand2", command=self.save_password
        ).pack(side="left", padx=5)

        # Section: Widgets
        self.section("Desktop")

        widget_row = self.row()
        tk.Label(widget_row, text="Show widgets:", bg=THEME.get("window"),
                 fg=THEME.get("text"), font=("Courier", 10),
                 width=20, anchor="w").pack(side="left", padx=20)
        self.widget_var = tk.BooleanVar(value=CONFIG.get("show_widgets", True))
        tk.Checkbutton(
            widget_row, variable=self.widget_var, bg=THEME.get("window"),
            activebackground=THEME.get("window"),
            command=self.toggle_widgets
        ).pack(side="left")

        # Section: Info
        self.section("System Info")

        info = [
            f"Version: MiniOS v3.0",
            f"Config: ~/.minios_config.json",
            f"User: {CONFIG.get('username', 'user')}",
            "",
            "Hotkeys:",
            "  F11  → Fullscreen",
            "  Esc  → Exit Fullscreen",
            "  Right-click desktop → Context menu",
        ]
        for line in info:
            tk.Label(
                self.frame, text=line, bg=THEME.get("window"),
                fg=THEME.get("text_dim"), font=("Courier", 9),
                anchor="w"
            ).pack(fill="x", padx=30, pady=1)

    def section(self, title):
        tk.Label(
            self.frame, text=f"─── {title} ───",
            bg=THEME.get("window"), fg=THEME.get("accent"),
            font=("Courier", 10, "bold")
        ).pack(pady=(15, 5))

    def row(self):
        f = tk.Frame(self.frame, bg=THEME.get("window"))
        f.pack(fill="x", pady=3)
        return f

    def toggle_theme(self):
        THEME.toggle()
        self.theme_btn.config(text=THEME.current.upper())

    def toggle_widgets(self):
        CONFIG.set("show_widgets", self.widget_var.get())

    def save_password(self):
        pw = self.pass_entry.get()
        CONFIG.set("password", pw)
        self.pass_entry.delete(0, "end")
        messagebox.showinfo("Saved", "Password updated!\nRestart MiniOS untuk efek.")
