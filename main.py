from core.listener import Listener
from core.speaker import Speaker
from datetime import datetime
from core.memory import Memory

listener = Listener()
speaker = Speaker()
memory = Memory()

speaker.speak("Lucy uruchomiona. Słucham.")

while True:
    text = listener.listen()
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

    elif text_lower.strip() == "":
        continue

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