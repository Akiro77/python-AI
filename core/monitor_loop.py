# core/monitor_loop.py
import time
import threading
from core.system_monitor import get_system_stats
from core.logger import log_command
from core.speaker import Speaker
import pythoncom

speaker = Speaker()

def start_monitor(interval=5):
    """
    Monitor systemu działający w tle.
    Pobiera statystyki co `interval` sekund.
    Wywołuje ostrzeżenia głosowe w przypadku krytycznych wartości.
    """
    # Wątek musi zainicjalizować COM
    pythoncom.CoInitialize()
    while True:
        stats = get_system_stats()

        # Ostrzeżenia głosowe dla CPU/GPU jeśli temperatura krytyczna
        if stats.get("cpu_status") == "CRITICAL":
            speaker.speak(f"Uwaga! CPU gorące: {stats.get('cpu_temp')} stopni, użycie {stats.get('cpu_usage')}%")
        if stats.get("gpu_status") == "CRITICAL":
            speaker.speak(f"Uwaga! GPU gorące: {stats.get('gpu_temp')} stopni, użycie {stats.get('gpu_usage')}%")

        time.sleep(interval)