import tkinter as tk
from datetime import datetime
from config import CONFIG
from theme import THEME, lerp_color
from desktop_widgets import ClockWidget, SysMonWidget

from apps.terminal import TerminalApp
from apps.notepad import NotepadApp
from apps.filemanager import FileManagerApp
from apps.settings import SettingsApp
from apps.sysmon import SysMonApp
from apps.calculator import CalculatorApp
from apps.imageviewer import ImageViewerApp
from apps.music import MusicApp


class WindowManager:
    def __init__(self, root, fullscreen_cb):
        self.root = root
        self.fullscreen_cb = fullscreen_cb
        self.windows = {}

        self.setup_desktop()
        self.setup_taskbar()
        self.setup_startmenu()
        self.start_clock()

        # Lift taskbar & menu biar gak ketutup canvas
        self.taskbar.lift()
        self.startmenu.lift()

        # Widget desktop
        if CONFIG.get("show_widgets", True):
            ClockWidget(self.canvas)
            SysMonWidget(self.canvas)

        # Autostart apps
        for app in CONFIG.get("autostart", []):
            self.root.after(500, lambda a=app: self.launch_app(a))

    # ================= DESKTOP =================
    def setup_desktop(self):
        self.desktop = tk.Frame(self.root, bg=THEME.get("bg"))
        self.desktop.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self.desktop, bg=THEME.get("desktop_top"),
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_desktop_click)
        self.canvas.bind("<Button-3>", self.show_context_menu)
        self.canvas.bind("<Configure>", self.redraw_bg)

    def on_desktop_click(self, event):
        self.close_startmenu()
        self.close_context_menu()

    def show_context_menu(self, event):
        self.close_context_menu()
        self.ctx = tk.Menu(self.root, tearoff=0,
                           bg=THEME.get("window"), fg=THEME.get("text"),
                           activebackground=THEME.get("accent"))
        self.ctx.add_command(label="🔄 Refresh Desktop", command=self.redraw_bg)
        self.ctx.add_command(label="🌓 Toggle Theme", command=self.toggle_theme)
        self.ctx.add_separator()
        self.ctx.add_command(label="❌ Exit", command=self.root.quit)
        try:
            self.ctx.tk_popup(event.x_root, event.y_root)
        finally:
            self.ctx.grab_release()

    def close_context_menu(self):
        if hasattr(self, "ctx"):
            try:
                self.ctx.unpost()
            except Exception:
                pass

    def redraw_bg(self, event=None):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            return
        self.canvas.delete("bg")
        top = THEME.get("desktop_top")
        bot = THEME.get("desktop_bot")
        for i in range(40):
            ratio = i / 40
            color = lerp_color(top, bot, ratio)
            self.canvas.create_rectangle(
                0, h * ratio, w, h * (ratio + 0.03),
                fill=color, width=0, tags="bg"
            )
        self.taskbar.lift()
        if self.startmenu_visible:
            self.startmenu.lift()

    # ================= TASKBAR =================
    def setup_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg=THEME.get("taskbar"), height=40)
        self.taskbar.place(relx=0, rely=1, relwidth=1, anchor="sw", height=40)
        self.taskbar.pack_propagate(False)

        self.start_btn = tk.Button(
            self.taskbar, text="🪟 Start", bg=THEME.get("button"),
            fg=THEME.get("text"), activebackground=THEME.get("accent"),
            activeforeground="#000", relief="flat",
            font=("Courier", 10, "bold"), padx=15, cursor="hand2",
            command=self.toggle_startmenu
        )
        self.start_btn.pack(side="left", padx=5, pady=5)

        self.task_list = tk.Frame(self.taskbar, bg=THEME.get("taskbar"))
        self.task_list.pack(side="left", fill="x", expand=True)

        self.clock = tk.Label(
            self.taskbar, text="", bg=THEME.get("taskbar"),
            fg=THEME.get("accent"), font=("Courier", 11, "bold")
        )
        self.clock.pack(side="right", padx=15)

    def start_clock(self):
        def tick():
            now = datetime.now().strftime("%H:%M:%S  %d/%m/%Y")
            self.clock.config(text=now)
            self.root.after(1000, tick)
        tick()

    # ================= START MENU =================
    def setup_startmenu(self):
        self.startmenu = tk.Frame(
            self.root, bg=THEME.get("window"),
            highlightthickness=1, highlightbackground=THEME.get("accent")
        )
        self.startmenu_visible = False

        items = [
            ("💻  Terminal", "terminal"),
            ("📝  Notepad", "notepad"),
            ("📁  File Manager", "filemanager"),
            ("📊  System Monitor", "sysmon"),
            ("🧮  Calculator", "calculator"),
            ("🖼️  Image Viewer", "imageviewer"),
            ("🎵  Music Player", "music"),
            ("⚙️  Settings", "settings"),
            ("—", None),
            ("🌓  Toggle Theme", "theme"),
            ("⛶  Fullscreen", "fullscreen"),
            ("❌  Exit MiniOS", "exit"),
        ]

        for label, cmd in items:
            if cmd is None:
                tk.Frame(self.startmenu, bg=THEME.get("border"),
                         height=1).pack(fill="x", pady=3)
                continue
            btn = tk.Label(
                self.startmenu, text=label, bg=THEME.get("window"),
                fg=THEME.get("text"), anchor="w", padx=20, pady=8,
                cursor="hand2", font=("Courier", 10)
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=THEME.get("button_hover")))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=THEME.get("window")))
            btn.bind("<Button-1>", lambda e, c=cmd: self.menu_action(c))

    def toggle_startmenu(self):
        if self.startmenu_visible:
            self.close_startmenu()
        else:
            h = self.root.winfo_height()
            menu_h = 480
            self.startmenu.place(x=5, y=h - 40 - menu_h,
                                 width=220, height=menu_h)
            self.startmenu.lift()
            self.startmenu_visible = True

    def close_startmenu(self, event=None):
        if self.startmenu_visible:
            self.startmenu.place_forget()
            self.startmenu_visible = False

    def menu_action(self, cmd):
        self.close_startmenu()
        if cmd == "exit":
            self.root.quit()
        elif cmd == "fullscreen":
            self.fullscreen_cb()
        elif cmd == "theme":
            self.toggle_theme()
        else:
            self.launch_app(cmd)

    def toggle_theme(self):
        THEME.toggle()
        self.apply_theme()

    def apply_theme(self):
        self.desktop.config(bg=THEME.get("bg"))
        self.canvas.config(bg=THEME.get("desktop_top"))
        self.taskbar.config(bg=THEME.get("taskbar"))
        self.start_btn.config(bg=THEME.get("button"), fg=THEME.get("text"))
        self.task_list.config(bg=THEME.get("taskbar"))
        self.clock.config(bg=THEME.get("taskbar"), fg=THEME.get("accent"))
        self.startmenu.config(bg=THEME.get("window"))
        self.redraw_bg()

    # ================= WINDOW =================
    def launch_app(self, app_name):
        if app_name in self.windows:
            self.focus_window(app_name)
            return

        titles = {
            "terminal": "Terminal",
            "notepad": "Notepad",
            "filemanager": "File Manager",
            "settings": "Settings",
            "sysmon": "System Monitor",
            "calculator": "Calculator",
            "imageviewer": "Image Viewer",
            "music": "Music Player",
        }
        title = titles.get(app_name, app_name)

        win = tk.Toplevel(self.root, bg=THEME.get("window"))
        win.title(title)
        win.geometry(f"600x400+{100 + len(self.windows)*30}+{80 + len(self.windows)*30}")

        chrome = tk.Frame(win, bg=THEME.get("window_hdr"), height=32)
        chrome.pack(fill="x")
        chrome.pack_propagate(False)

        tk.Label(chrome, text=f"  {title}", bg=THEME.get("window_hdr"),
                 fg=THEME.get("text"),
                 font=("Courier", 10, "bold")).pack(side="left", padx=5)

        btn_frame = tk.Frame(chrome, bg=THEME.get("window_hdr"))
        btn_frame.pack(side="right", padx=5)

        tk.Button(btn_frame, text="−", bg="#f1c40f", fg="#000",
                  relief="flat", width=3, cursor="hand2",
                  command=lambda: self.minimize_window(app_name)
                  ).pack(side="left", padx=2)

        tk.Button(btn_frame, text="□", bg="#2ecc71", fg="#000",
                  relief="flat", width=3, cursor="hand2",
                  command=lambda: self.toggle_maximize(win, app_name)
                  ).pack(side="left", padx=2)

        tk.Button(btn_frame, text="×", bg="#e74c3c", fg="#fff",
                  relief="flat", width=3, cursor="hand2",
                  command=lambda: self.close_window(app_name)
                  ).pack(side="left", padx=2)

        content = tk.Frame(win, bg=THEME.get("window"))
        content.pack(fill="both", expand=True)

        apps = {
            "terminal": TerminalApp,
            "notepad": NotepadApp,
            "filemanager": FileManagerApp,
            "settings": SettingsApp,
            "sysmon": SysMonApp,
            "calculator": CalculatorApp,
            "imageviewer": ImageViewerApp,
            "music": MusicApp,
        }

        try:
            app_instance = apps[app_name](content)
        except Exception as e:
            tk.Label(content, text=f"Error launching {app_name}:\n{e}",
                     bg=THEME.get("window"), fg="#e74c3c",
                     font=("Courier", 10)).pack(expand=True)
            app_instance = None

        self.windows[app_name] = {
            "win": win, "content": content,
            "app": app_instance, "minimized": False,
            "maximized": False
        }

        self.add_taskbar_item(app_name, title)
        self.focus_window(app_name)

    def focus_window(self, app_name):
        data = self.windows[app_name]
        data["win"].lift()
        if data["minimized"]:
            data["win"].deiconify()
            data["minimized"] = False

    def minimize_window(self, app_name):
        data = self.windows[app_name]
        data["win"].withdraw()
        data["minimized"] = True

    def toggle_maximize(self, win, app_name):
        data = self.windows[app_name]
        if data["maximized"]:
            win.geometry(data["prev_geom"])
            data["maximized"] = False
        else:
            data["prev_geom"] = win.geometry()
            win.state("zoomed")
            data["maximized"] = True

    def close_window(self, app_name):
        data = self.windows[app_name]
        data["win"].destroy()
        del self.windows[app_name]
        self.remove_taskbar_item(app_name)

    # ================= TASKBAR ITEMS =================
    def add_taskbar_item(self, app_name, title):
        if hasattr(self, f"task_{app_name}"):
            return
        btn = tk.Button(
            self.task_list, text=title, bg=THEME.get("button"),
            fg=THEME.get("text"), relief="flat", font=("Courier", 9),
            padx=10, pady=4, cursor="hand2",
            command=lambda: self.focus_window(app_name)
        )
        btn.pack(side="left", padx=3, pady=5)
        setattr(self, f"task_{app_name}", btn)

    def remove_taskbar_item(self, app_name):
        if hasattr(self, f"task_{app_name}"):
            getattr(self, f"task_{app_name}").destroy()
            delattr(self, f"task_{app_name}")
