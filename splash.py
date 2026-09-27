import tkinter as tk

BOOT_LOGO = r"""
    __  __ _       _  ____  ____  
   |  \/  (_)_ __ (_)/ __ \/ ___| 
   | |\/| | | '_ \| | |  | \___ \ 
   | |  | | | | | | | |__| |___) |
   |_|  |_|_|_| |_|_|\____/|____/ 
"""


class Splash:
    def __init__(self, root, on_done):
        self.root = root
        self.on_done = on_done
        self.frame = tk.Frame(root, bg="#000000")
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.logo_label = tk.Label(
            self.frame, text="", fg="#00d4ff", bg="#000000",
            font=("Courier", 10, "bold"), justify="left"
        )
        self.logo_label.pack(pady=(60, 20))
        self.status = tk.Label(
            self.frame, text="", fg="#00ff88", bg="#000000",
            font=("Courier", 11), justify="left", anchor="w"
        )
        self.status.pack(fill="x", padx=40, pady=10)
        self.progress = tk.Canvas(
            self.frame, width=500, height=8,
            bg="#111111", highlightthickness=0
        )
        self.progress.pack(pady=20)
        self.bar = self.progress.create_rectangle(
            0, 0, 0, 8, fill="#00d4ff", width=0
        )
        self.animate_logo(0)

    def animate_logo(self, idx):
        if idx <= len(BOOT_LOGO):
            self.logo_label.config(text=BOOT_LOGO[:idx])
            self.root.after(15, lambda: self.animate_logo(idx + 2))
        else:
            self.root.after(200, lambda: self.run_boot_sequence(0))

    def run_boot_sequence(self, step):
        steps = [
            ("[ OK ] Mounting filesystem...", 15),
            ("[ OK ] Loading kernel modules...", 30),
            ("[ OK ] Starting window manager...", 50),
            ("[ OK ] Initializing GUI engine...", 70),
            ("[ OK ] Loading user preferences...", 85),
            ("[ OK ] Starting desktop environment...", 100),
        ]
        if step >= len(steps):
            self.root.after(400, self.finish)
            return
        text, pct = steps[step]
        current = self.status.cget("text")
        self.status.config(text=current + "\n" + text)
        self.progress.coords(self.bar, 0, 0, 500 * (pct / 100), 8)
        self.root.after(350, lambda: self.run_boot_sequence(step + 1))

    def finish(self):
        self.frame.destroy()
        self.on_done()
