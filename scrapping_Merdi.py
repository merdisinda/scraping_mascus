
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.mascus.com"

driver = webdriver.Chrome()
driver.get("https://www.mascus.com/+/catalogs=cargo-transport&continentcodes=150/1,relevance,search.html")

# Attendre que les annonces apparaissent
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='SearchResult_searchResultItemWrapper']"))
)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

items = soup.select("div[class*='SearchResult_searchResultItemWrapper']")
print("Camions trouvés :", len(items))

donnees_camions = []

for item in items:

    # --- Image ---
    img = item.select_one("div[class*='SearchResult_searchResultImageWrapper'] img")
    photo_url = BASE_URL + img["src"] if img and img.get("src") else None

    # --- Marque + modèle ---
    title = item.select_one("h3[class*='SearchResult_brandmodel']")
    marque, modele = None, None
    if title:
        parts = title.text.strip().split(" ", 1)
        marque = parts[0]
        modele = parts[1] if len(parts) > 1 else None

    # --- Lien vers la fiche ---
    link = item.select_one("a[class*='SearchResult_assetHeaderUrl']")
    url_fiche = BASE_URL + link["href"] if link else None

    # --- Prix ---
    price = item.select_one("div.heading5")
    price = price.text.strip() if price else None

    # --- Description ---
    desc = item.select_one("p.basicText2Style")
    type_camion = annee = kilometrage = localisation = None

    if desc:
        parts = [p.strip() for p in desc.text.strip().split("•")]
        if len(parts) >= 4:
            type_camion, annee, kilometrage, localisation = parts[:4]

    donnees_camions.append({
        "marque": marque,
        "modele": modele,
        "annee": annee,
        "kilometrage": kilometrage,
        "prix": price,
        "type_camion": type_camion,
        "localisation": localisation,
        "photo": photo_url,
        "url_fiche": url_fiche
    })

# --- Export CSV ---
if donnees_camions:
    with open("camion.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=donnees_camions[0].keys())
        writer.writeheader()
        writer.writerows(donnees_camions)
    print("CSV généré avec succès.")
else:
    print("Aucune donnée trouvée.")