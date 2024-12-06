# Loterie Nationale Scraper

Ce projet permet de récupérer automatiquement les montants des jackpots de la Loterie Nationale Belge et de les afficher sur une page web, idéale pour l'intégration avec Yodeck.

## Fonctionnalités

- Scraping automatique des montants EuroMillions, Lotto et Extra Lotto
- Mise à jour automatique toutes les heures
- Interface web responsive et moderne
- Logging des opérations pour le suivi

## Installation

1. Clonez ce dépôt :
```bash
git clone [URL_DU_REPO]
cd loterie-scraper
```

2. Créez un environnement virtuel Python et activez-le :
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Démarrez le serveur :
```bash
python app.py
```

2. Accédez à l'interface web :
- URL locale : http://localhost:5000
- Le scraper s'exécutera automatiquement toutes les heures

## Configuration Yodeck

1. Dans votre tableau de bord Yodeck, ajoutez un nouveau "Web Page Widget"
2. Configurez l'URL de votre serveur
3. Réglez le temps de rafraîchissement selon vos besoins

## Structure des fichiers

- `scraper.py` : Script principal de scraping
- `app.py` : Serveur web Flask
- `requirements.txt` : Dépendances du projet
- `output/index.html` : Page web générée

## Logs

Les logs sont enregistrés dans `scraper.log` pour le suivi des opérations et le débogage.

## Note importante

Les sélecteurs HTML dans `scraper.py` devront être ajustés en fonction de la structure réelle du site de la Loterie Nationale. Vérifiez et mettez à jour ces sélecteurs si nécessaire.
