# KS-Ω Orchestrator v1.1 — Meta-IA multi-modèles (futuriste)

Nouveau dans 1.1 :
- **LLM Judge** optionnel (fusion par modèle juge) + heuristique fallback
- **Budget Guard** (cap global via .env)
- **Telegram Notifier** (caps / erreurs)
- **Prompt Cache local** (SQLite) avec TTL
- **Fallback résilient** (ignore providers en échec, continue)

## Démarrage
```
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # remplir si LIVE souhaité
uvicorn apps.api.main:app --reload
# Dashboard :
streamlit run dashboard/app.py
```

## Utilisation (POST /orchestrate)
Voir `apps/api/main.py` pour le schéma d'entrée/sortie. Logs dans `data/logs/app.log`.
