import sounddevice as sd
import numpy as np
import whisper
import time

class Listener:
    def __init__(self):
        print("🔄 Ładowanie Whisper...")
        self.model = whisper.load_model("base")
        print("✅ Whisper gotowy")

        self.max_record_time = 3.0      # max nagranie 3 sek
        self.samplerate = 16000
        self.threshold = 0.01           # czułość nagrywania
        self.silence_limit = 1.2        # czas ciszy w sekundach

    def listen(self):
        print("🎤 Lucy słucha...")
        recording = []
        silence_time = 0
        is_recording = False

        def callback(indata, frames, time_info, status):
            nonlocal silence_time, is_recording
            volume = np.linalg.norm(indata) / len(indata)
            if volume > self.threshold:
                is_recording = True
                recording.append(indata.copy())
                silence_time = 0
            elif is_recording:
                recording.append(indata.copy())
                silence_time += frames / self.samplerate

        with sd.InputStream(samplerate=self.samplerate,
                            channels=1,
                            dtype='float32',
                            callback=callback):
            start_time = time.time()
            while True:
                if is_recording and silence_time > self.silence_limit:
                    break
                if time.time() - start_time > self.max_record_time:
                    break
                time.sleep(0.01)

        if len(recording) == 0:
            return ""

        audio = np.concatenate(recording, axis=0).flatten()
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio))

        print("🧠 Przetwarzam...")
        result = self.model.transcribe(
            audio,
            language="pl",
            task="transcribe",
            fp16=False,
            temperature=0
        )
        text = result.get("text", "").strip()
        return text