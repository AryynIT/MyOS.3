#!/usr/bin/env python3
"""
MiniOS v3.0 - Desktop Environment berbasis Tkinter
Jalan di terminal Linux. Support window & fullscreen mode.
"""
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CONFIG
from splash import Splash
from login import LoginScreen
from window_manager import WindowManager


class MiniOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MiniOS v3.0")

        w, h = CONFIG.get("window_size", [1024, 700])
        self.root.geometry(f"{w}x{h}")
        self.root.configure(bg="#0a0a0f")

        # Hotkeys global
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.wm = None
        self.show_splash()

    def show_splash(self):
        Splash(self.root, self.show_login)

    def show_login(self):
        # Kalau password kosong, langsung skip login
        if not CONFIG.get("password", ""):
            self.start_desktop()
        else:
            LoginScreen(self.root, self.start_desktop)

    def start_desktop(self):
        self.wm = WindowManager(self.root, self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        current = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MiniOS().run()
