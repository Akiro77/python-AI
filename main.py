import queue
import threading
from core.listener import Listener
from datetime import datetime
import time
from core.speaker import Speaker
speaker = Speaker()
from core.memory import Memory

# -----------------------------
# Kolejka komunikatów
# -----------------------------
text_queue = queue.Queue()
is_speaking = False

# -----------------------------
# Inicjalizacja
# -----------------------------
listener = Listener()
speaker = Speaker()
memory = Memory()

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
        safe_speak("Wyłączam się. Do zobaczenia.")
        break

    elif "cześć" in text_lower:
        safe_speak("Cześć. Jak mogę pomóc?")

    elif any(word in text_lower for word in ["godzina", "godzin", "dzina", "zina"]):
        now = datetime.now().strftime("%H:%M")
        safe_speak(f"Jest {now}")

    elif "mam na imię" in text_lower:
        name = text_lower.replace("mam na imię", "").strip()
        memory.set("name", name)
        safe_speak(f"Miło Cię poznać {name}")

    elif "moje imię to" in text_lower:
        name = memory.get("name")
        if name:
            safe_speak(f"Masz na imię {name}")
        else:
            safe_speak("Jeszcze mi nie powiedziałeś jak masz na imię")

    else:
        safe_speak("Nie rozumiem jeszcze, ale się uczę.")