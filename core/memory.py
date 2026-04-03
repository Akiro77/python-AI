import os
import json
from config.settings import MEMORY_PATH


class Memory:
    def __init__(self):
        self.file_path = MEMORY_PATH

        # upewnij się że folder istnieje
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # wczytaj pamięć
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save()

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()

    def clear(self):
        self.data = {}
        self._save()

    def _save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except IOError:
            print("Błąd zapisu pamięci 😅")