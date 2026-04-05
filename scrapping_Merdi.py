from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
driver.get("https://www.mascus.com/+/catalogs=cargo-transport&categories=tractortrucksmain&continentcodes=150/1,relevance,search.html")

time.sleep(5)  # attendre le chargement JS

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

items = soup.select("div[data-index]")
print("Camions trouvés :", len(items))

donnees_camions = []
#boucle pour extraire les données de chaque camion
for item in items:
    # --- Marque + Modèle ---
    title = item.select_one("h3.SearchResult_brandmodel__04K2L")
    marque, modele = None, None
    if title:
        parts = title.text.strip().split(" ", 1)
        marque = parts[0]
        modele = parts[1] if len(parts) > 1 else None

    # --- Prix ---
    price = item.select_one("div.heading5")
    price = price.text.strip() if price else None

    # --- Texte principal (année, km, localisation, type camion) ---
    desc = item.select_one("p.basicText2Style")
    if desc:
        text = desc.text.strip()
        parts = [p.strip() for p in text.split("•")]

        type_camion = parts[0]
        annee = parts[1]
        kilometrage = parts[2]
        localisation = parts[3]
    else:
        type_camion = annee = kilometrage = localisation = None

    # --- Photo principale ---
    img = item.select_one("div.SearchResult_searchResultImageWrapper__2Rrn4 img")
    photo_url = img["src"] if img else None

    donnees_camions.append({
        "marque": marque,
        "modele": modele,
        "annee": annee,
        "kilometrage": kilometrage,
        "prix": price,
        "type_camion": type_camion,
        "localisation": localisation,
        "photo": photo_url
    })

import csv

# Sécurité : vérifier que la liste n'est pas vide
if not donnees_camions:
    print("Aucune donnée à écrire dans le CSV.")
else:
    with open("camions.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=donnees_camions[0].keys())
        writer.writeheader()
        writer.writerows(donnees_camions)
    print("CSV généré avec succès.")

