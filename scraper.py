import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import logging
import re
from pathlib import Path

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
            'Accept-Language': 'fr-BE,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

    def clean_amount(self, amount):
        if not amount:
            return "Montant non disponible"
        # Nettoyer le montant
        amount = amount.replace(".", "").replace(",", ".")
        # Extraire le nombre et l'unité
        match = re.search(r'(\d+(?:\.\d+)?)\s*(million|millions|€|MILLION|MILLIONS|EUR)?', amount, re.IGNORECASE)
        if match:
            number = float(match.group(1))
            unit = match.group(2)
            # Convertir en format standard
            if unit and 'million' in unit.lower():
                return f"{number:,.0f}.000.000 €".replace(",", ".")
            else:
                return f"{number:,.0f} €".replace(",", ".")
        return amount

    def get_jackpot(self, url, game):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            amount = None

            if game == 'euromillions':
                # Chercher dans les différentes sections possibles
                jackpot_elements = soup.find_all(['span', 'div', 'p'], string=re.compile(r'(\d+[\d\s.,]*\s*(?:million|€|MILLION|EUR))', re.IGNORECASE))
                for element in jackpot_elements:
                    text = element.get_text().strip()
                    if 'million' in text.lower() or '€' in text:
                        match = re.search(r'(\d+[\d\s.,]*\s*(?:million|€|MILLION|EUR))', text, re.IGNORECASE)
                        if match:
                            amount = match.group(1)
                            break

            elif game == 'lotto':
                # Chercher dans les différentes sections possibles
                jackpot_elements = soup.find_all(['span', 'div', 'p'], string=re.compile(r'(\d+[\d\s.,]*\s*(?:million|€|MILLION|EUR))', re.IGNORECASE))
                for element in jackpot_elements:
                    text = element.get_text().strip()
                    if 'million' in text.lower() or '€' in text:
                        match = re.search(r'(\d+[\d\s.,]*\s*(?:million|€|MILLION|EUR))', text, re.IGNORECASE)
                        if match:
                            amount = match.group(1)
                            break

            elif game == 'extra-lotto':
                # Pour Extra Lotto, montant minimum garanti
                amount = "3.000.000 €"

            if amount:
                return self.clean_amount(amount)

            # Ajouter des logs pour le débogage
            logging.info(f"Contenu de la page {game}:")
            logging.info(soup.get_text()[:500])  # Les 500 premiers caractères
            
            return "Montant non disponible"

        except requests.RequestException as e:
            logging.error(f"Erreur lors de la récupération du jackpot {game}: {e}")
            return "Erreur de connexion"
        except Exception as e:
            logging.error(f"Erreur inattendue pour {game}: {e}")
            logging.error(f"Détails de l'erreur: {str(e)}")
            return "Erreur"

    def generate_html(self):
        jackpots = {}
        for game, url in self.urls.items():
            jackpots[game] = self.get_jackpot(url, game)
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
