
from pathlib import Path

import groq
from groq import Groq

from src.config import GROQ_API_KEY, LLM_MODEL


SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "summary_system.txt"


def _load_system_prompt(path: Path = SYSTEM_PROMPT_PATH) -> str:
    """Charge le prompt système depuis le fichier texte."""
    try:
        prompt = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Prompt système introuvable : {path}. "
            "Vérifie la constante SYSTEM_PROMPT_PATH."
        ) from exc
    if not prompt:
        raise ValueError(f"Le prompt système est vide : {path}")
    return prompt


def summarize(transcription: str) -> str:
    """
    Reçoit une transcription brute et retourne un compte rendu structuré
    (titre, résumé, points clés, décisions/actions) produit par le LLM.
    """
    if not transcription or not transcription.strip():
        raise ValueError("La transcription est vide, rien à résumer.")

    system_prompt = _load_system_prompt()
    client = Groq(api_key=GROQ_API_KEY)

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": transcription},     
            ],
            temperature=0.2,  
        )
    except groq.APIError as exc:
        raise RuntimeError(f"Échec de l'appel à l'API Groq : {exc}") from exc

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("Réponse vide de l'API Groq.")
    return content.strip()


if __name__ == "__main__":
  
    exemple = (
        "Bonjour à tous, point hebdo. On a validé le budget marketing. "
        "Marie doit envoyer le devis au prestataire avant vendredi."
    )
    print(summarize(exemple))
