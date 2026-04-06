# core/hardware_monitor.py
import requests

# Adres Web Servera LibreHardwareMonitor
LHM_URL = "http://localhost:8085/data.json"

def get_all_stats():
    """
    Pobiera dane systemowe z LibreHardwareMonitor Web Server.
    Zwraca słownik z:
    cpu_usage, cpu_temp, gpu_usage, gpu_temp, ram_usage, disk_usage
    """
    try:
        response = requests.get(LHM_URL, timeout=2)
        data = response.json()
    except Exception as e:
        print(f"⚠️ LibreHardwareMonitor nie dostępny: {e}")
        return {
            "cpu_usage": None,
            "cpu_temp": None,
            "gpu_usage": None,
            "gpu_temp": None,
            "ram_usage": None,
            "disk_usage": None,
        }

    stats = {
        "cpu_usage": None,
        "cpu_temp": None,
        "gpu_usage": None,
        "gpu_temp": None,
        "ram_usage": None,
        "disk_usage": None,
    }

    def parse_sensors(sensors):
        for sensor in sensors:
            type_ = sensor.get("SensorType")
            name = sensor.get("Name")
            value = sensor.get("Value")
            if type_ == "Temperature" and "CPU Package" in name:
                stats["cpu_temp"] = value
            elif type_ == "Load" and "CPU Total" in name:
                stats["cpu_usage"] = int(value)
            elif type_ == "Temperature" and "GPU Core" in name:
                stats["gpu_temp"] = value
            elif type_ == "Load" and "GPU Core" in name:
                stats["gpu_usage"] = int(value)
            elif type_ == "Load" and "Memory" in name:
                stats["ram_usage"] = int(value)
            elif type_ == "Load" and "C:" in name:
                stats["disk_usage"] = int(value)

            # Rekurencyjnie przeszukujemy dzieci
            if "Children" in sensor:
                parse_sensors(sensor["Children"])

    if "Children" in data:
        parse_sensors(data["Children"])

    return stats