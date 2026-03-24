import sounddevice as sd
import numpy as np
import whisper
import queue

class Listener:
    def __init__(self):
        print("🔄 Ładowanie modelu Whisper...")
        self.model = whisper.load_model("tiny")  # CPU
        print("✅ Whisper gotowy")

        self.samplerate = 16000
        self.blocksize = 2048
        self.q_audio = queue.Queue()

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q_audio.put(indata.copy())

    def listen(self):
        print("🎤 Lucy słucha...")

        with sd.InputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            channels=1,
            dtype='float32',
            callback=self._callback
        ):
            buffer = np.zeros((0,), dtype=np.float32)

            while True:
                data = self.q_audio.get()
                buffer = np.concatenate([buffer, data.flatten()])

                # co ~1 sekunda analizujemy
                if len(buffer) > self.samplerate:
                    result = self.model.transcribe(
                        buffer,
                        language="pl",
                        fp16=False
                    )

                    text = result.get("text", "").strip()
                    buffer = np.zeros((0,), dtype=np.float32)

                    if text:
                        return text