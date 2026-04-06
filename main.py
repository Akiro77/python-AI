import os
import queue
import threading
from core.listener import Listener
from datetime import datetime
import time
from core.speaker import Speaker
from core.memory import Memory
from core.monitor_loop import start_monitor
from core.system_monitor import get_system_stats
from core.logger import log_command
import multiprocessing
from core.system_plot import start_live_plot
import multiprocessing

plot_process = None

# -----------------------------
# Start monitoringu w tle
# -----------------------------
monitor_thread = threading.Thread(target=start_monitor, daemon=True)
monitor_thread.start()

# -----------------------------
# Inicjalizacja
# -----------------------------
speaker = Speaker()
listener = Listener()
memory = Memory()
is_speaking = False
text_queue = queue.Queue()

# Sprawdzenie pamięci
name = memory.get("name")
if name:
    print(f"Memory loaded: name = {name}")
else:
    print("Memory loaded: brak imienia")

# -----------------------------
# Funkcje pomocnicze
# -----------------------------
def safe_speak(text):
    global is_speaking
    is_speaking = True
    speaker.speak(text)
    is_speaking = False

def clean_text(text):
    text = text.replace("<|pl|>", "")
    return text.strip().lower()

def open_plot():
    p = multiprocessing.get_context('spawn').Process(target=start_live_plot)
    p.start()
    return p

# -----------------------------
# Wątek nasłuchu
# -----------------------------
def listen_thread():
    while True:
        if is_speaking:
            time.sleep(0.1)
            continue
        text = listener.listen()
        if text:
            text_queue.put(text)

threading.Thread(target=listen_thread, daemon=True).start()

# -----------------------------
# Start Lucy
# -----------------------------
safe_speak("Lucy uruchomiona. Słucham.")

# -----------------------------
# Główna pętla
# -----------------------------
while True:
    try:
        text = text_queue.get(timeout=0.5)
    except queue.Empty:
        continue

    print(f"Ty: {text}")
    text_lower = clean_text(text)

    if len(text_lower) > 100:
        print("⚠️ Za długi tekst - ignoruję")
        continue

    print(f"DEBUG: {text_lower}")

    # -------------------------
    # Komendy
    # -------------------------
    if "koniec" in text_lower:
        response = "Wyłączam się. Do zobaczenia."
        safe_speak(response)
        log_command(text, response)
        break

    elif "pokaż system" in text_lower:
        stats = get_system_stats()

        response = (
            f"CPU {stats['cpu_usage']} procent, {stats['cpu_temp']} stopni. "
            f"GPU {stats['gpu_usage']} procent, {stats['gpu_temp']} stopni. "
            f"RAM {stats['ram_usage']} procent."
        )

        safe_speak(response)
        log_command(text, response)

    elif "wykres" in text_lower or "monitor wykres" in text_lower:
        safe_speak("Otwieram wykresy systemu")
        if plot_process is None or not plot_process.is_alive():
            plot_process = start_live_plot()

    elif "zamknij wykres" in text_lower:
        safe_speak("Zamykam wykresy")
    if plot_process and plot_process.is_alive():
        plot_process.terminate()
        plot_process = None

        for proc in multiprocessing.active_children():
            proc.terminate()

    elif "cześć" in text_lower:
        response = "Cześć. Jak mogę pomóc?"
        safe_speak(response)
        log_command(text, response)

    elif any(word in text_lower for word in ["godzina", "godzin", "dzina", "zina"]):
        now = datetime.now().strftime("%H:%M")
        response = f"Jest {now}"
        safe_speak(response)
        log_command(text, response)

    elif "mam na imię" in text_lower:
        name = text_lower.replace("mam na imię", "").strip()
        memory.set("name", name)

        response = f"Miło Cię poznać {name}"
        safe_speak(response)
        log_command(text, response)

    elif "moje imię to" in text_lower or "jak mam na imię" in text_lower:
        name = memory.get("name")

        if name:
            response = f"Masz na imię {name}"
        else:
            response = "Jeszcze mi nie powiedziałeś jak masz na imię"

        safe_speak(response)
        log_command(text, response)

    else:
        response = "Nie rozumiem jeszcze, ale się uczę."
        safe_speak(response)
        log_command(text, response)