import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise SystemExit(
        "Erreur : la variable GROQ_API_KEY est manquante. "
        "Créez un fichier .env avec votre clé avant de lancer Scribe."
    )


STT_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "llama-3.3-70b-versatile"