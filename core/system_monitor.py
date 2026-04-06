# core/system_monitor.py
from core.hardware_monitor import get_all_stats
from core.logger import log_system
from config.settings import CPU_WARNING, CPU_CRITICAL, RAM_WARNING, RAM_CRITICAL, DISK_WARNING, DISK_CRITICAL

def get_system_stats():
    """
    Pobiera aktualne statystyki systemowe i klasyfikuje alerty.
    Zwraca słownik z wartościami i statusami.
    """
    stats = get_all_stats()

    # Status CPU
    cpu_usage = stats.get("cpu_usage") or 0
    cpu_temp = stats.get("cpu_temp") or 0
    if cpu_temp >= CPU_CRITICAL:
        stats["cpu_status"] = "CRITICAL"
    elif cpu_temp >= CPU_WARNING:
        stats["cpu_status"] = "WARNING"
    else:
        stats["cpu_status"] = "OK"

    # Status RAM
    ram_usage = stats.get("ram_usage") or 0
    if ram_usage >= RAM_CRITICAL:
        stats["ram_status"] = "CRITICAL"
    elif ram_usage >= RAM_WARNING:
        stats["ram_status"] = "WARNING"
    else:
        stats["ram_status"] = "OK"

    # Status dysku
    disk_usage = stats.get("disk_usage") or 0
    if disk_usage >= DISK_CRITICAL:
        stats["disk_status"] = "CRITICAL"
    elif disk_usage >= DISK_WARNING:
        stats["disk_status"] = "WARNING"
    else:
        stats["disk_status"] = "OK"

    # Możesz tutaj dodać alerty dla GPU podobnie
    gpu_temp = stats.get("gpu_temp") or 0
    gpu_usage = stats.get("gpu_usage") or 0
    if gpu_temp >= CPU_CRITICAL:
        stats["gpu_status"] = "CRITICAL"
    elif gpu_temp >= CPU_WARNING:
        stats["gpu_status"] = "WARNING"
    else:
        stats["gpu_status"] = "OK"

    # Logujemy system
    log_system(stats)

    return stats