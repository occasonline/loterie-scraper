from flask import Flask, send_from_directory
import os
import schedule
import time
from threading import Thread
from scraper import LoterieScraper

app = Flask(__name__)

def run_scraper():
    scraper = LoterieScraper()
    scraper.run()

@app.route('/')
def home():
    return send_from_directory('output', 'index.html')

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Premier scraping au démarrage
    run_scraper()
    
    # Planification du scraping toutes les heures
    schedule.every(1).hours.do(run_scraper)
    
    # Démarrage du planificateur dans un thread séparé
    scheduler_thread = Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Démarrage du serveur Flask
    app.run(host='0.0.0.0', port=5000)
