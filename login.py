import tkinter as tk
from config import CONFIG


class LoginScreen:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

        self.frame = tk.Frame(root, bg="#0a0a0f")
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        container = tk.Frame(
            self.frame, bg="#1a1a2e",
            highlightthickness=2, highlightbackground="#00d4ff"
        )
        container.place(relx=0.5, rely=0.5, anchor="center",
                        width=360, height=380)

        tk.Label(container, text="⚡", fg="#00d4ff", bg="#1a1a2e",
                 font=("Courier", 40, "bold")).pack(pady=(30, 5))

        tk.Label(container, text="MiniOS", fg="#fff", bg="#1a1a2e",
                 font=("Courier", 22, "bold")).pack()

        tk.Label(container, text="Login to continue", fg="#888",
                 bg="#1a1a2e", font=("Courier", 10)).pack(pady=(5, 25))

        tk.Label(container, text="Username", fg="#ccc", bg="#1a1a2e",
                 font=("Courier", 10), anchor="w").pack(fill="x", padx=40)

        self.user_entry = tk.Entry(
            container, bg="#0a0a0f", fg="#fff",
            font=("Courier", 11), insertbackground="#00d4ff",
            relief="flat", highlightthickness=1,
            highlightbackground="#333", highlightcolor="#00d4ff"
        )
        self.user_entry.pack(fill="x", padx=40, pady=(2, 15), ipady=6)
        self.user_entry.insert(0, CONFIG.get("username", "user"))

        tk.Label(container, text="Password", fg="#ccc", bg="#1a1a2e",
                 font=("Courier", 10), anchor="w").pack(fill="x", padx=40)

        self.pass_entry = tk.Entry(
            container, bg="#0a0a0f", fg="#fff", show="●",
            font=("Courier", 11), insertbackground="#00d4ff",
            relief="flat", highlightthickness=1,
            highlightbackground="#333", highlightcolor="#00d4ff"
        )
        self.pass_entry.pack(fill="x", padx=40, pady=(2, 5), ipady=6)

        self.msg = tk.Label(container, text="", fg="#e74c3c", bg="#1a1a2e",
                            font=("Courier", 9))
        self.msg.pack()

        tk.Button(
            container, text="  LOGIN  ", bg="#00d4ff", fg="#000",
            font=("Courier", 11, "bold"), relief="flat",
            cursor="hand2", padx=20, pady=8,
            command=self.try_login
        ).pack(pady=15)

        self.pass_entry.bind("<Return>", lambda e: self.try_login())
        self.user_entry.bind("<Return>", lambda e: self.pass_entry.focus())
        self.pass_entry.focus_set()

    def try_login(self):
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get()
        expected = CONFIG.get("password", "")

        if pw == expected:
            CONFIG.set("username", user)
            self.frame.destroy()
            self.on_success()
        else:
            self.msg.config(text="Password salah!")
            self.pass_entry.delete(0, "end")
