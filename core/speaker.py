import pyttsx3
import queue
import threading
import time

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('rate', 170)
        # szukamy polskiego głosu
        voices = self.engine.getProperty('voices')
        for v in voices:
            if "pl" in v.id.lower():
                self.engine.setProperty('voice', v.id)
                break

        self.q = queue.Queue()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while True:
            text = self.q.get()
            if text is None:
                break
            self.engine.say(text)
            self.engine.runAndWait()
            time.sleep(0.05)  # mała pauza dla stabilności

    def speak(self, text):
        print(f"Lucy: {text}")
        self.q.put(text)