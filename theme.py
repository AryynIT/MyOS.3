from config import CONFIG

THEMES = {
    "dark": {
        "bg":           "#0a0a0f",
        "desktop_top":  "#1a1a2e",
        "desktop_bot":  "#0f3460",
        "taskbar":      "#0f0f1a",
        "window":       "#1e1e2e",
        "window_hdr":   "#2a2a3e",
        "text":         "#e0e0e0",
        "text_dim":     "#888888",
        "accent":       "#00d4ff",
        "button":       "#1e1e2e",
        "button_hover": "#2e2e4e",
        "entry_bg":     "#0a0a0f",
        "border":       "#333333",
    },
    "light": {
        "bg":           "#f0f0f5",
        "desktop_top":  "#d0d8e8",
        "desktop_bot":  "#a8c0e0",
        "taskbar":      "#ffffff",
        "window":       "#f8f8fc",
        "window_hdr":   "#e0e0e8",
        "text":         "#222222",
        "text_dim":     "#666666",
        "accent":       "#0078d4",
        "button":       "#ffffff",
        "button_hover": "#e0e8f0",
        "entry_bg":     "#ffffff",
        "border":       "#c0c0c8",
    },
}


class Theme:
    def __init__(self):
        self.current = CONFIG.get("theme", "dark")
        self.listeners = []

    def get(self, key):
        return THEMES[self.current].get(key, "#000000")

    def toggle(self):
        self.current = "light" if self.current == "dark" else "dark"
        CONFIG.set("theme", self.current)
        for cb in self.listeners:
            try:
                cb()
            except Exception:
                pass

    def on_change(self, callback):
        self.listeners.append(callback)


THEME = Theme()


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((
        int(r1 + (r2 - r1) * t),
        int(g1 + (g2 - g1) * t),
        int(b1 + (b2 - b1) * t),
    ))
