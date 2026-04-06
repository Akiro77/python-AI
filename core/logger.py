import json
import os
from datetime import datetime, timedelta
from config.settings import LOG_PATH

# ------------------------
# Ensure log file exists
# ------------------------
def _ensure_file():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

# ------------------------
# Read and write helpers
# ------------------------
def _read_logs():
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _write_logs(data):
    MAX_LOGS = 10000
    if len(data) > MAX_LOGS:
        data = data[-MAX_LOGS:]

    try:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError:
        print("Błąd zapisu logów 😅")

# ------------------------
# Logowanie komend i systemu
# ------------------------
def log_command(command, response):
    _ensure_file()
    entry = {
        "type": "command",
        "time": datetime.now().isoformat(),
        "command": command,
        "response": response
    }
    data = _read_logs()
    data.append(entry)
    _write_logs(data)

def log_system(stats):
    _ensure_file()
    entry = {
        "type": "system",
        **stats
    }
    data = _read_logs()
    data.append(entry)
    _write_logs(data)

# ------------------------
# Analiza logów
# ------------------------
def analyze(period="day", log_type=None):
    if not os.path.exists(LOG_PATH):
        return []

    data = _read_logs()
    now = datetime.now()
    days = {"day": 1, "week": 7, "month": 30}.get(period, 1)
    start = now - timedelta(days=days)

    filtered = []
    for entry in data:
        try:
            if datetime.fromisoformat(entry["time"]) >= start:
                filtered.append(entry)
        except:
            continue

    if log_type:
        filtered = [e for e in filtered if e.get("type") == log_type]

    return filtered

# ------------------------
# Pobranie alertów
# ------------------------
def get_alerts(period="day"):
    logs = analyze(period, log_type="system")
    return [
        log for log in logs
        if "CRITICAL" in (log.get("cpu_status"), log.get("ram_status"), log.get("disk_status"))
    ]