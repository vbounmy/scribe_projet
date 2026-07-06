from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Transcribe audio file
def speech_to_text(audio_path, language="fr"):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    api_key = os.environ.get("GROQ_API_KEY_1")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    client = Groq(api_key=api_key)
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo",
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