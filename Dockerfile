FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Créer le dossier output
RUN mkdir -p output

# Définir les variables d'environnement
ENV PORT=10000

# Commande de démarrage
CMD gunicorn --workers=2 --bind=0.0.0.0:$PORT app:app
