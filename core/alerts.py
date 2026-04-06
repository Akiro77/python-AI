def classify(value, warning, critical):
    if value is None:
        return "UNKNOWN"
    if value >= critical:
        return "CRITICAL"
    elif value >= warning:
        return "WARNING"
    return "OK"


def classify_system(stats, config):
    return {
        "cpu_status": classify(stats.get("cpu_temp"),
                               config.CPU_TEMP_WARNING,
                               config.CPU_TEMP_CRITICAL),

        "gpu_status": classify(stats.get("gpu_temp"),
                               config.GPU_TEMP_WARNING,
                               config.GPU_TEMP_CRITICAL),

        "ram_status": classify(stats.get("ram_usage"),
                               config.RAM_WARNING,
                               config.RAM_CRITICAL)
    }