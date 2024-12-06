from flask import Flask, send_from_directory, render_template_string
import os
from scraper import LoterieScraper
from pathlib import Path

app = Flask(__name__)

# Créer le dossier output s'il n'existe pas
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

def run_scraper():
    scraper = LoterieScraper()
    return scraper.run()

@app.route('/')
def home():
    # Exécuter le scraper à chaque requête
    run_scraper()
    
    # Retourner le fichier HTML généré
    try:
        return send_from_directory('output', 'index.html')
    except Exception as e:
        # En cas d'erreur, retourner un message simple
        return f"<h1>Service en cours de démarrage...</h1><p>Veuillez rafraîchir dans quelques secondes.</p>"

if __name__ == '__main__':
    # Démarrage du serveur Flask
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
