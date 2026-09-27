import tkinter as tk
from tkinter import filedialog, messagebox
from theme import THEME

# Pygame optional — kalau error, jangan crash
HAS_PYGAME = False
pygame = None
try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except Exception as e:
    HAS_PYGAME = False
    _pygame_error = str(e)


class MusicApp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=THEME.get("window"))
        self.frame.pack(fill="both", expand=True)

        if not HAS_PYGAME:
            tk.Label(
                self.frame,
                text="🎵 Music Player\n\n"
                     "pygame tidak bisa dimuat.\n"
                     "Kemungkinan konflik versi SDL.\n\n"
                     "Fix:\n"
                     "  pip3 uninstall pygame\n"
                     "  sudo apt install python3-pygame\n\n"
                     "Atau skip aja — fitur ini opsional.",
                bg=THEME.get("window"), fg=THEME.get("text"),
                font=("Courier", 10), justify="center"
            ).pack(expand=True)
            return

        self.playing = False
        self.current = None

        tk.Label(
            self.frame, text="🎵 Music Player",
            bg=THEME.get("window"), fg=THEME.get("accent"),
            font=("Courier", 18, "bold")
        ).pack(pady=20)

        self.track_label = tk.Label(
            self.frame, text="No track loaded",
            bg=THEME.get("window"), fg=THEME.get("text"),
            font=("Courier", 10)
        )
        self.track_label.pack(pady=10)

        btns = tk.Frame(self.frame, bg=THEME.get("window"))
        btns.pack(pady=20)

        for text, cmd in [
            ("📂 Load", self.load),
            ("▶ Play", self.play),
            ("⏸ Pause", self.pause),
            ("⏹ Stop", self.stop),
        ]:
            tk.Button(
                btns, text=text, bg=THEME.get("button"),
                fg=THEME.get("text"), relief="flat",
                font=("Courier", 10), padx=15, pady=8, cursor="hand2",
                command=cmd
            ).pack(side="left", padx=5)

    def load(self):
        path = filedialog.askopenfilename(
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.flac"), ("All", "*.*")]
        )
        if path:
            self.current = path
            self.track_label.config(text=f"♪ {path.split('/')[-1]}")

    def play(self):
        if not self.current:
            messagebox.showinfo("Info", "Load track dulu")
            return
        try:
            pygame.mixer.music.load(self.current)
            pygame.mixer.music.play()
            self.playing = True
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
        else:
            pygame.mixer.music.unpause()
            self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
