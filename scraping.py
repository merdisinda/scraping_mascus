import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://www.mascus.com/+/catalogs=cargo-transport&itemtype=usedad&categories=trucks&continentcodes=150/1,relevance,search.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Scraping et nettoyage en cours...")

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    ads = soup.find_all("div", class_=re.compile("SearchResult_searchResultItemWrapper")) 
    
    results = []
    seen_trucks = set() 
    
    for ad in ads:
        try:
            # --- 1. GESTION DU PRIX ---
            price_tag = ad.find("div", class_="heading5")
            raw_price = price_tag.text.strip() if price_tag else ""
            
            # Filtrer "On request" et les prix vides
            if not raw_price or "request" in raw_price.lower():
                continue 
            
            # Nettoyage : on enlève "USD", les virgules, et on supprime les espaces
            clean_price = raw_price.replace("USD", "").replace(",", "").strip()
            
            # --- 2. RÉCUPÉRATION DU RESTE DES INFOS ---
            title_tag = ad.find("h3", class_=re.compile("SearchResult_brandmodel"))
            title = title_tag.text.strip() if title_tag else "Non renseigné"
            
            details_tag = ad.find("p", class_="basicText2Style")
            truck_type, year, mileage, location = "Non", "Non", "Non", "Non"
            
            if details_tag:
                parts = [part.strip() for part in details_tag.text.split("•")]
                if len(parts) >= 1: truck_type = parts[0]
                if len(parts) >= 2: year = parts[1]
                if len(parts) >= 3: 
                    # Nettoyage du kilométrage : on enlève "mil" et on supprime les espaces
                    mileage = parts[2].replace("mil", "").strip()
                if len(parts) >= 4: location = parts[3]

            # --- 3. FILTRE ANTI-DOUBLONS ---
            truck_signature = f"{title}-{clean_price}-{mileage}"
            if truck_signature in seen_trucks:
                continue 
            seen_trucks.add(truck_signature)

            # --- 4. PHOTOS ---
            image_wrapper = ad.find("div", class_=re.compile("SearchResult_searchResultImageWrapper"))
            image_url = "Pas d'image"
            if image_wrapper:
                img_tag = image_wrapper.find("img")
                if img_tag:
                    image_url = img_tag.get("src", "Lien introuvable")
            
            # On ajoute le camion avec les nouveaux noms de colonnes
            results.append({
                "Marque et modèle": title,
                "Année": year,
                "Kilométrage/mil": mileage,
                "Prix (USD)": clean_price,
                "Type de camion": truck_type,
                "Localisation": location,
                "Lien photo": image_url
            })
            
        except Exception as e:
            continue

    # --- 5. ENREGISTREMENT CSV ---
    # Mise à jour des en-têtes de colonnes
    colonnes = ["Marque et modèle", "Année", "Kilométrage/mil", "Prix (USD)", "Type de camion", "Localisation", "Lien photo"]
    
    with open("camions_mascus.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"✅ Terminé ! {len(results)} camions enregistrés.")
else:
    print(f"❌ Échec de la requête. Code HTTP : {response.status_code}")