# core/system_plot.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from core.system_monitor import get_system_stats
from collections import deque
import multiprocessing

MAX_POINTS = 60

cpu_usage_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
cpu_temp_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
gpu_usage_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
gpu_temp_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
ram_usage_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
disk_usage_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)

def update(frame, lines):
    stats = get_system_stats()

    cpu_usage_data.append(stats["cpu_usage"])
    cpu_temp_data.append(stats["cpu_temp"])
    gpu_usage_data.append(stats["gpu_usage"])
    gpu_temp_data.append(stats["gpu_temp"])
    ram_usage_data.append(stats["ram_usage"])
    disk_usage_data.append(stats["disk_usage"])

    lines[0].set_ydata(cpu_usage_data)
    lines[1].set_ydata(cpu_temp_data)
    lines[2].set_ydata(gpu_usage_data)
    lines[3].set_ydata(gpu_temp_data)
    lines[4].set_ydata(ram_usage_data)
    lines[5].set_ydata(disk_usage_data)

    return lines

def _plot_loop():
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()

    ax.set_ylim(0, 100)
    ax.set_xlim(0, MAX_POINTS)
    ax.set_title("Lucy: Monitoring systemu (live)")
    ax.set_xlabel("Ostatnie próbki")
    ax.set_ylabel("Wartość (%) / Temperatura (°C)")

    line_cpu_usage, = ax.plot(cpu_usage_data, label="CPU Usage (%)", color="red")
    line_cpu_temp, = ax.plot(cpu_temp_data, label="CPU Temp (°C)", color="darkred")
    line_gpu_usage, = ax.plot(gpu_usage_data, label="GPU Usage (%)", color="blue")
    line_gpu_temp, = ax.plot(gpu_temp_data, label="GPU Temp (°C)", color="darkblue")
    line_ram_usage, = ax.plot(ram_usage_data, label="RAM Usage (%)", color="green")
    line_disk_usage, = ax.plot(disk_usage_data, label="Disk Usage (%)", color="orange")

    lines = [line_cpu_usage, line_cpu_temp, line_gpu_usage, line_gpu_temp, line_ram_usage, line_disk_usage]
    ax.legend(loc="upper left")

    ani = animation.FuncAnimation(fig, update, fargs=(lines,), interval=1000)
    plt.show()

def start_live_plot():
    """
    Uruchamia wykres w osobnym procesie, nie blokując Lucy.
    """
    p = multiprocessing.Process(target=_plot_loop)
    p.start()
    return p