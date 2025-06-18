import torch
import whisper

class AudioTranscriber:
    def __init__(self, audio_path,transcription_path, model_size="base"):
        self.audio_path = audio_path
        self.transcription_path = transcription_path
        self.model_size = model_size

    def transcribe_audio(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🧠 Using device: {device}")
        model = whisper.load_model(self.model_size).to(device)
        result = model.transcribe(self.audio_path)
        with open(self.transcription_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print("✅ Transcription saved to " + self.transcription_path)
        return result["text"]

