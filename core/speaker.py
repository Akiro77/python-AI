# speaker.py
import tempfile
import os
import subprocess
import platform

class Speaker:
    def __init__(self):
        if platform.system() != "Windows":
            raise Exception("Ten speaker działa tylko w Windows")
        import win32com.client
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")

    def speak(self, text):
        print(f"Lucy: {text}")
        self.speaker.Speak(text)