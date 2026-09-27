import json
import os

CONFIG_PATH = os.path.expanduser("~/.minios_config.json")

DEFAULT_CONFIG = {
    "theme": "dark",
    "wallpaper": None,
    "username": "user",
    "password": "",          # kosong = no login
    "autostart": ["terminal"],
    "show_widgets": True,
    "window_size": [1024, 700],
}

class Config:
    def __init__(self):
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH) as f:
                    self.data.update(json.load(f))
            except Exception:
                pass

    def save(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()


CONFIG = Config()
