import tkinter as tk
from theme import THEME

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class SysMonApp:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=THEME.get("window"))
        self.frame.pack(fill="both", expand=True)

        self.text = tk.Text(
            self.frame, bg=THEME.get("entry_bg"),
            fg=THEME.get("accent"), font=("Courier", 10),
            relief="flat", wrap="word"
        )
        self.text.pack(fill="both", expand=True, padx=5, pady=5)

        if not HAS_PSUTIL:
            self.text.insert("end",
                "psutil tidak terinstall.\n\n"
                "Install dengan:\n\n"
                "  sudo apt install python3-psutil\n"
                "  # atau\n"
                "  pip install psutil"
            )
            return
        self.update()

    def update(self):
        if not HAS_PSUTIL:
            return
        self.text.delete("1.0", "end")

        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()

        lines = [
            "═══ SYSTEM MONITOR ═══",
            "",
            f"CPU Usage   : {cpu:5.1f}%",
            f"CPU Cores   : {psutil.cpu_count()}",
            "",
            f"RAM Total   : {ram.total / (1024**3):.2f} GB",
            f"RAM Used    : {ram.used / (1024**3):.2f} GB ({ram.percent}%)",
            f"RAM Free    : {ram.available / (1024**3):.2f} GB",
            "",
            f"Disk /      : {disk.used / (1024**3):.2f} / {disk.total / (1024**3):.2f} GB ({disk.percent}%)",
            "",
            f"Net Sent    : {net.bytes_sent / (1024**2):.2f} MB",
            f"Net Recv    : {net.bytes_recv / (1024**2):.2f} MB",
            "",
            "═══ TOP PROCESSES ═══",
            f"{'NAME':<24} {'CPU%':>6} {'MEM%':>6}",
            "-" * 40,
        ]

        try:
            procs = []
            for p in psutil.process_iter(["name", "cpu_percent", "memory_percent"]):
                try:
                    procs.append(p.info)
                except Exception:
                    pass
            procs.sort(key=lambda x: x.get("cpu_percent") or 0, reverse=True)
            for p in procs[:8]:
                name = (p.get("name") or "?")[:23]
                cpu_p = p.get("cpu_percent") or 0
                mem_p = p.get("memory_percent") or 0
                lines.append(f"{name:<24} {cpu_p:>6.1f} {mem_p:>6.1f}")
        except Exception:
            pass

        self.text.insert("end", "\n".join(lines))
        self.frame.after(2000, self.update)
