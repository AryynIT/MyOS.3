import tkinter as tk
from tkinter import filedialog, messagebox
from theme import THEME

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class ImageViewerApp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=THEME.get("window"))
        self.frame.pack(fill="both", expand=True)

        topbar = tk.Frame(self.frame, bg=THEME.get("window_hdr"))
        topbar.pack(fill="x")

        tk.Button(
            topbar, text="📂 Open Image", bg=THEME.get("button"),
            fg=THEME.get("text"), relief="flat",
            font=("Courier", 9), padx=10, pady=5, cursor="hand2",
            command=self.open_image
        ).pack(side="left", padx=3, pady=3)

        self.info = tk.Label(
            topbar, text="", bg=THEME.get("window_hdr"),
            fg=THEME.get("text_dim"), font=("Courier", 9)
        )
        self.info.pack(side="left", padx=10)

        self.canvas = tk.Canvas(
            self.frame, bg="#000", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)

        self.image = None
        self.photo = None

        if not HAS_PIL:
            self.canvas.create_text(
                250, 100,
                text="Pillow tidak terinstall.\n\npip install Pillow",
                fill="#e74c3c", font=("Courier", 11), justify="center"
            )
        self.canvas.bind("<Configure>", lambda e: self.render())

    def open_image(self):
        if not HAS_PIL:
            messagebox.showerror("Error",
                "Install Pillow dulu:\n\npip install Pillow")
            return
        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("All", "*.*"),
            ]
        )
        if not path:
            return
        try:
            self.image = Image.open(path)
            self.info.config(
                text=f"{self.image.size[0]}x{self.image.size[1]}  |  {path.split('/')[-1]}"
            )
            self.render()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def render(self):
        if not self.image:
            return
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            return

        img = self.image.copy()
        img.thumbnail((w - 10, h - 10))
        self.photo = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(w // 2, h // 2, image=self.photo)
