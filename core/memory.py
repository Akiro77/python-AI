import os
import json

class Memory:
    def __init__(self):
        # folder 'memory' w głównym katalogu projektu
        self.folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "memory")
        os.makedirs(self.folder, exist_ok=True)
        self.file_path = os.path.join(self.folder, "memory.json")

        # wczytanie istniejącej pamięci lub inicjalizacja pustej
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = {}
        else:
            self.data = {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save()

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)