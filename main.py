import queue
import threading
from core.listener import Listener
from core.speaker import Speaker
from core.memory import Memory
from datetime import datetime
import time

# kolejka komunikatów z mikrofonu
text_queue = queue.Queue()

listener = Listener()
speaker = Speaker()
memory = Memory()

speaker.speak("Lucy uruchomiona. Słucham.")

# wątek nasłuchu
def listen_thread():
    while True:
        text = listener.listen()
        if text:
            text_queue.put(text)

threading.Thread(target=listen_thread, daemon=True).start()

# główna pętla reagowania
while True:
    try:
        text = text_queue.get(timeout=0.5)  # nieblokujący get
    except queue.Empty:
        continue

    print(f"Ty: {text}")
    
    text_lower = text.lower()

    if "koniec" in text_lower:
        speaker.speak("Wyłączam się. Do zobaczenia.")
        break

    elif "cześć" in text_lower:
        speaker.speak("Cześć. Jak mogę pomóc?")

    elif "godzina" in text_lower:
        now = datetime.now().strftime("%H:%M")
        speaker.speak(f"Jest {now}")

    elif "mam na imię" in text_lower:
        name = text_lower.replace("mam na imię", "").strip()
        memory.set("name", name)
        speaker.speak(f"Miło Cię poznać {name}")

    elif "jak mam na imię" in text_lower:
        name = memory.get("name")
        if name:
            speaker.speak(f"Masz na imię {name}")
        else:
            speaker.speak("Jeszcze mi nie powiedziałeś jak masz na imię")

    else:
        speaker.speak("Nie rozumiem jeszcze, ale się uczę.")