from .core import *

class SaveManager:
    def __init__(self):
        self.path = os.path.join(PROJECT_DIR, "data", "savegame.json")

    def has_save(self):
        return os.path.isfile(self.path)

    def save(self, data):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            temp = self.path + ".tmp"
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp, self.path)
            return True
        except (OSError, TypeError, ValueError) as exc:
            print(f"[SAVE] Failed: {exc}")
            return False

    def load(self):
        if not self.has_save():
            return None
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[SAVE] Load failed: {exc}")
            return None


