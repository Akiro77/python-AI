def classify(value, warning, critical):
    if value >= critical:
        return "CRITICAL"
    elif value >= warning:
        return "WARNING"
    return "OK"


def classify_system(stats, config):
    return {
        "cpu_status": classify(stats["cpu"], config.CPU_WARNING, config.CPU_CRITICAL),
        "ram_status": classify(stats["ram"], config.RAM_WARNING, config.RAM_CRITICAL),
        "disk_status": classify(stats["disk"], config.DISK_WARNING, config.DISK_CRITICAL),
    }