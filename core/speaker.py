import pyttsx3

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('rate', 170)

        voices = self.engine.getProperty('voices')
        for v in voices:
            if "pl" in v.id.lower():
                self.engine.setProperty('voice', v.id)
                break

    def speak(self, text):
        print(f"Lucy: {text}")
        self.engine.say(text)
        self.engine.runAndWait()