import sounddevice as sd
import numpy as np
import whisper

class Listener:
    def __init__(self):
        print("🔄 Ładowanie Whisper...")
        self.model = whisper.load_model("tiny")
        print("✅ Whisper gotowy")

        self.samplerate = 16000
        self.threshold = 0.01
        self.silence_limit = 1.0

    def listen(self):
        print("🎤 Lucy słucha...")

        recording = []
        silence_time = 0
        is_recording = False

        def callback(indata, frames, time, status):
            nonlocal silence_time, is_recording

            volume = np.linalg.norm(indata) / len(indata)

            if volume > self.threshold:
                is_recording = True
                recording.append(indata.copy())
                silence_time = 0
            elif is_recording:
                recording.append(indata.copy())
                silence_time += frames / self.samplerate

        # 🔥 stream tylko na jedną wypowiedź
        with sd.InputStream(samplerate=self.samplerate,
                            channels=1,
                            dtype='float32',
                            callback=callback):

            while True:
                if is_recording and silence_time > self.silence_limit:
                    break

        if len(recording) == 0:
            return ""

        audio = np.concatenate(recording, axis=0).flatten()

        print("🧠 Przetwarzam...")
        result = self.model.transcribe(audio, language="pl", fp16=False)
        text = result.get("text", "").strip()

        return text