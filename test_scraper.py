import requests
from bs4 import BeautifulSoup
import json
import re

def analyze_page():
    # URLs des différents jeux
    urls = {
        'euromillions': 'https://www.loterie-nationale.be/nos-jeux/euromillions',
        'lotto': 'https://www.loterie-nationale.be/nos-jeux/lotto',
        'extra-lotto': 'https://www.loterie-nationale.be/nos-jeux/extra-lotto'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'fr-BE,fr;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    for game, url in urls.items():
        try:
            print(f"\nAnalyse de {game.upper()}...")
            print(f"URL: {url}")
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Recherche des éléments contenant des montants
            # Motif pour trouver les montants (ex: 1.000.000 € ou 17 millions €)
            amount_pattern = re.compile(r'(\d+[\d.,]*\s*(million|€|euros|MILLION|EUROS))', re.IGNORECASE)
            
            # Recherche dans tous les éléments textuels
            for element in soup.find_all(text=amount_pattern):
                parent = element.parent
                print(f"\n--- Montant trouvé ---")
                print(f"Texte: {element.strip()}")
                print(f"Balise parente: {parent.name}")
                
                # Afficher les classes du parent
                if parent.get('class'):
                    print(f"Classes: {' '.join(parent.get('class'))}")
                
                # Afficher l'ID du parent
                if parent.get('id'):
                    print(f"ID: {parent.get('id')}")
                
                # Afficher le chemin complet
                ancestors = []
                current = parent
                while current and current.name:
                    if current.get('class'):
                        ancestors.append(f"{current.name}.{' '.join(current.get('class'))}")
                    elif current.get('id'):
                        ancestors.append(f"{current.name}#{current.get('id')}")
                    else:
                        ancestors.append(current.name)
                    current = current.parent
                
                print("Chemin: " + " > ".join(reversed(ancestors)))
                print("-" * 50)

        except requests.RequestException as e:
            print(f"Erreur lors de la récupération de {game}: {e}")
        except Exception as e:
            print(f"Erreur inattendue pour {game}: {e}")

if __name__ == "__main__":
    analyze_page()
