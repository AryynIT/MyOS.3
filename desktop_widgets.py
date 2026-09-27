from datetime import datetime


class ClockWidget:
    def __init__(self, canvas):
        self.canvas = canvas
        self.update()

    def update(self):
        self.canvas.delete("clock_widget")
        w = self.canvas.winfo_width()
        if w < 10:
            self.canvas.after(1000, self.update)
            return

        now = datetime.now()
        self.canvas.create_text(
            w - 30, 30, anchor="ne",
            text=now.strftime("%H:%M"), fill="#00d4ff",
            font=("Courier", 48, "bold"), tags="clock_widget"
        )
        self.canvas.create_text(
            w - 30, 95, anchor="ne",
            text=now.strftime("%A, %d %B %Y"), fill="#888",
            font=("Courier", 12), tags="clock_widget"
        )
        self.canvas.after(1000, self.update)


class SysMonWidget:
    def __init__(self, canvas):
        self.canvas = canvas
        try:
            import psutil
            self.psutil = psutil
        except ImportError:
            self.psutil = None
        self.update()

    def update(self):
        self.canvas.delete("sysmon")
        if not self.psutil:
            self.canvas.after(2000, self.update)
            return

        try:
            cpu = self.psutil.cpu_percent(interval=None)
            ram = self.psutil.virtual_memory().percent
        except Exception:
            self.canvas.after(2000, self.update)
            return

        self.canvas.create_rectangle(20, 100, 220, 115,
                                     fill="#222", width=0, tags="sysmon")
        color = "#00ff88" if cpu < 70 else "#f1c40f" if cpu < 90 else "#e74c3c"
        self.canvas.create_rectangle(20, 100, 20 + 200 * (cpu / 100), 115,
                                     fill=color, width=0, tags="sysmon")
        self.canvas.create_text(20, 92, anchor="sw", text=f"CPU  {cpu:.0f}%",
                                fill="#00d4ff",
                                font=("Courier", 9, "bold"), tags="sysmon")

        self.canvas.create_rectangle(20, 135, 220, 150,
                                     fill="#222", width=0, tags="sysmon")
        self.canvas.create_rectangle(20, 135, 20 + 200 * (ram / 100), 150,
                                     fill="#00d4ff", width=0, tags="sysmon")
        self.canvas.create_text(20, 127, anchor="sw", text=f"RAM  {ram:.0f}%",
                                fill="#00d4ff",
                                font=("Courier", 9, "bold"), tags="sysmon")

        self.canvas.after(1500, self.update)
