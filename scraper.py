import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import logging
import re
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class LoterieScraper:
    def __init__(self):
        self.urls = {
            'euromillions': 'https://www.loterie-nationale.be/nos-jeux/euromillions',
            'lotto': 'https://www.loterie-nationale.be/nos-jeux/lotto',
            'extra-lotto': 'https://www.loterie-nationale.be/nos-jeux/extra-lotto'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'fr-BE,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def extract_amount(self, text):
        # Motif pour trouver les montants (ex: 1.000.000 € ou 17 millions €)
        amount_pattern = re.compile(r'(\d+[\d.,]*\s*(million|€|euros|MILLION|EUROS))', re.IGNORECASE)
        match = amount_pattern.search(text)
        if match:
            return match.group(1)
        return None

    def get_jackpot(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Recherche dans les éléments <b> et <p> contenant des montants
            for element in soup.find_all(['b', 'p']):
                if element.string:
                    amount = self.extract_amount(element.string)
                    if amount:
                        return amount
            return "Montant non disponible"

        except requests.RequestException as e:
            logging.error(f"Erreur lors de la récupération du jackpot: {e}")
            return "Erreur de connexion"
        except Exception as e:
            logging.error(f"Erreur inattendue: {e}")
            return "Erreur"

    def generate_html(self):
        jackpots = {}
        for game, url in self.urls.items():
            jackpots[game] = self.get_jackpot(url)
            logging.info(f"Jackpot {game}: {jackpots[game]}")

        html_template = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Montants Loterie Nationale</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    text-align: center;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                .jackpot-container {{
                    background-color: white;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    transition: transform 0.3s ease;
                }}
                .jackpot-container:hover {{
                    transform: translateY(-5px);
                }}
                .game-title {{
                    color: #e4003a;
                    margin-bottom: 10px;
                    font-size: 1.5em;
                }}
                .jackpot-amount {{
                    font-size: 2.5em;
                    color: #000;
                    font-weight: bold;
                    margin: 15px 0;
                }}
                .update-time {{
                    color: #666;
                    font-size: 0.9em;
                    margin-top: 30px;
                    border-top: 1px solid #ddd;
                    padding-top: 20px;
                }}
                @media (max-width: 600px) {{
                    body {{
                        padding: 10px;
                    }}
                    .jackpot-amount {{
                        font-size: 2em;
                    }}
                }}
            </style>
        </head>
        <body>
            <h1 style="color: #e4003a;">Montants Loterie Nationale</h1>
            
            <div class="jackpot-container">
                <div class="game-title">EuroMillions</div>
                <div class="jackpot-amount">{jackpots['euromillions']}</div>
            </div>
            
            <div class="jackpot-container">
                <div class="game-title">Lotto</div>
                <div class="jackpot-amount">{jackpots['lotto']}</div>
            </div>
            
            <div class="jackpot-container">
                <div class="game-title">Extra Lotto</div>
                <div class="jackpot-amount">{jackpots['extra-lotto']}</div>
            </div>
            
            <div class="update-time">
                Dernière mise à jour: {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </div>
        </body>
        </html>
        """

        return html_template

    def save_html(self, html_content):
        try:
            output_dir = Path('output')
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / 'index.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logging.info(f"Fichier HTML généré avec succès: {output_file}")
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde du fichier HTML: {e}")
            return False

    def run(self):
        logging.info("Début du scraping...")
        html_content = self.generate_html()
        if html_content:
            success = self.save_html(html_content)
            if success:
                logging.info("Scraping terminé avec succès")
                return True
        logging.error("Échec du scraping")
        return False

if __name__ == "__main__":
    scraper = LoterieScraper()
    scraper.run()
