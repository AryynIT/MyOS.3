import tkinter as tk
from theme import THEME


class CalculatorApp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=THEME.get("window"))
        self.frame.pack(fill="both", expand=True)

        self.expr = ""

        self.display = tk.Entry(
            self.frame, bg=THEME.get("entry_bg"),
            fg=THEME.get("accent"), font=("Courier", 20, "bold"),
            relief="flat", justify="right",
            insertbackground=THEME.get("accent")
        )
        self.display.pack(fill="x", padx=10, pady=10, ipady=10)

        buttons = [
            ["C", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "⌫", "="],
        ]

        grid = tk.Frame(self.frame, bg=THEME.get("window"))
        grid.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for r, row in enumerate(buttons):
            grid.grid_rowconfigure(r, weight=1)
            for c, label in enumerate(row):
                grid.grid_columnconfigure(c, weight=1)
                color = THEME.get("button")
                fg = THEME.get("text")
                if label == "=":
                    color = THEME.get("accent")
                    fg = "#000"
                elif label == "C":
                    color = "#e74c3c"
                    fg = "#fff"

                tk.Button(
                    grid, text=label, bg=color, fg=fg,
                    font=("Courier", 14, "bold"), relief="flat",
                    cursor="hand2",
                    command=lambda l=label: self.on_click(l)
                ).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

    def on_click(self, label):
        if label == "C":
            self.expr = ""
        elif label == "⌫":
            self.expr = self.expr[:-1]
        elif label == "=":
            try:
                allowed = {"__builtins__": {}}
                result = str(eval(self.expr, allowed, {}))
                self.expr = result
            except Exception:
                self.expr = "Error"
        else:
            if self.expr == "Error":
                self.expr = ""
            self.expr += label

        self.display.delete(0, "end")
        self.display.insert(0, self.expr)
