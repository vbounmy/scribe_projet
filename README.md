# Scribe

Scribe est un outil en ligne de commande qui transforme un enregistrement audio en compte rendu écrit et structuré.

## Description

Scribe fonctionne en trois étapes :

1. l'utilisateur fournit un fichier audio ;
2. un modèle de transcription Speech-to-Text (STT) convertit l'audio en texte brut ;
3. un modèle de langage (LLM) reformule ce texte en compte rendu propre avec un titre, un résumé, des points clés et des décisions/actions.

Les deux modèles sont appelés via l'API serverless de Groq. Aucune phase d'entraînement n'est nécessaire : le projet intègre des briques existantes.

## Arborescence

- `src/` : code source Python
- `audio/` : exemples d'audio et fichiers de test
- `output/` : comptes rendus générés
- `.env.example` : modèle de configuration des variables d'environnement
- `requirements.txt` : dépendances Python

## Installation

1. Cloner le dépôt :
   ```bash
   git clone <url-du-depot>
   cd scribe_projet
   ```
2. Créer et activer un environnement virtuel Python :
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Copier le fichier de configuration :
   ```bash
   copy .env.example .env
   ```
5. Remplir `.env` avec votre clé Groq et, si besoin, les noms de modèles.

## Configuration

Le projet charge la configuration depuis `src/config.py`.

Variables attendues dans `.env` :

- `GROQ_API_KEY` : clé API Groq
- `GROQ_STT_MODEL` : modèle STT à utiliser
- `GROQ_LLM_MODEL` : modèle LLM à utiliser

> Le fichier `.env.example` est fourni pour documenter les variables attendues sans exposer de secret.

## Utilisation

Depuis la racine du projet :

```bash
python src/code.py <chemin/fichier_audio>
```

Le programme réalise la transcription, génère un compte rendu et sauvegarde une version Markdown dans `output/`.

## Questions TP

### Q1 : Pourquoi le .gitignore doit-il exister avant d'écrire la moindre ligne de code manipulant des secrets ?

- Le fichier `.gitignore` doit exister avant d'écrire la moindre ligne de code manipulant des secrets pour éviter de committer par erreur `.env`, les clés API ou l'environnement virtuel.
- Cela garantit aussi que la clé API n'est jamais stockée dans le dépôt.

### Q2 : Quels modèles STT et LLM propose Groq aujourd'hui, et lesquels choisissez-vous ? Justifiez (qualité, vitesse, coût).

Pour ce projet, nous choisissons :

- STT : `whisper-large-v3-turbo` car il offre une bonne qualité de transcription et une prise en charge du français.
- LLM : `llama-3.3-70b-versatile` pour un bon équilibre entre compréhension, génération structurée et robustesse.

Justification :

- qualité : ces modèles sont bien adaptés au texte et à la structure attendue ;
- vitesse : ils restent raisonnables en temps de réponse pour un usage CLI ;
- coût : le niveau de modèle est plus élevé pour la qualité, mais il est possible de choisir un modèle plus léger en fonction du budget.

### Q3 : Que renvoie exactement l'API en plus du texte (langue détectée, segments, horodatage...) ? Qu'est-ce qui pourrait être utile pour une évolution future de Scribe ?

L'API peut renvoyer plusieurs métadonnées utiles :

- langue détectée ;
- segments ou timestamps ;
- probabilités ou score de confiance ;
- format de réponse détaillé (`verbose_json`).

Ces données sont utiles pour des évolutions futures, par exemple :

- superposer le texte avec la timeline de l'audio ;
- permettre la recherche par segment ;
- générer des sous-titres ou des résumés basés sur des intervalles temporels.

### Q4 : Quelle température choisissez-vous pour cet usage, et pourquoi ?

Pour ce type d'usage, une température basse est recommandée (`0.0` ou `0.2`). Cela limite les hallucinations et favorise des résultats factuels et stables, ce qui est important pour transformer une transcription en compte rendu structuré.

### Q5 : Votre prompt système est envoyé à chaque requête : quel lien avec la notion de tokens en cache vue en cours ?

Le prompt système est envoyé à chaque requête. Il compte parmi les tokens transmis à l'API et influence donc le coût et la taille du contexte. Un prompt stable et bien conçu réduit le risque de variations inutiles. Les fournisseurs peuvent mettre en cache des contextes courts, mais chaque appel inclut toujours les tokens du message système, donc il faut rester concis et pertinent.

## Notes

Ne stockez jamais votre clé API dans le dépôt.
