import psutil
from datetime import datetime
from core.alerts import classify_system
import config.settings as confige

def get_system_stats():
    return {
        "time": datetime.now().isoformat(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }

def get_system_stats():
    stats = {
        "time": datetime.now().isoformat(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }

    alerts = classify_system(stats, config)

    return {**stats, **alerts}    