from groq import Groq
import os
from src.config import GROQ_API_KEY, STT_MODEL


# Transcribe audio file
def speech_to_text(audio_path, language="fr"):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model=STT_MODEL,
            prompt="Extrait le texte de l'audio de la manière la plus factuelle possible",
            response_format="verbose_json",
            language=language,
            temperature=0.0
        )
        return transcription.text

if __name__ == "__main__":
    audio_path = "./audio/scribe_test_30s.wav"
    text = speech_to_text(audio_path, language="fr")
    print("Transcription :", text)