import time
from core.system_monitor import get_system_stats
from core.logger import log_system

def start_monitor(interval=60):
    while True:
        stats = get_system_stats()
        log_system(stats)

        if stats.get("cpu_status") == "CRITICAL":
            print("🔥 CPU się gotuje!")

        time.sleep(interval)