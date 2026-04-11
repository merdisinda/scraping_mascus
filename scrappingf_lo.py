import requests
from bs4 import BeautifulSoup
import time
import csv 
import pandas as pd
import re 

base_url = "https://www.mascus.com/transportation/trucks"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

results = []
page = 1
max_pages = 588 

print("Début du scraping multi-pages...\n")

while True:
    url = f"{base_url}?page={page}"
    print(f"Scraping de la page {page} : {url} ...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        trucks = soup.find_all("div", class_="SearchResult_searchResultItemWrapper__VVVnZ")

        if not trucks:
            print("Aucun camion trouvé sur cette page. Fin du catalogue atteinte.")
            break

        for truck in trucks:
            nom_tag = truck.find("h3", class_="SearchResult_brandmodel__04K2L")
            nom = nom_tag.get_text(strip=True) if nom_tag else "Nom non trouvé"
            
            infos_tag = truck.find("p", class_="basicText2Style")
            infos = infos_tag.get_text(strip=True) if infos_tag else "Pas d'information"
            
            prix_tag = truck.find("div", class_="heading5")
            prix = prix_tag.get_text(strip=True) if prix_tag else "Pas de prix"
            
            results.append({
                "nom": nom,
                "info": infos,
                "prix": prix
            })

        if page >= max_pages:
            print(f"\n Arrêt au bout de {max_pages} pages.")
            break

        page += 1
        time.sleep(3)

    except Exception as e:
        print(f"Erreur critique lors du scraping de la page {page} : {e}")
        break

print(f"\n--- SCRAPING TERMINÉ ---")
print(f"Total récupéré : {len(results)} camions.")

df = pd.DataFrame(results)

print(f"Il y a {len(df)} camions à nettoyer et trier.")

types = []
annees = []
kilometrages = []
localisations = []

mots_vendeurs = ['marketplace', 'ritchie', 'bros', 'machinery', 'auction', 'equipment', 'sales']

for index, row in df.iterrows():
    info_brute = str(row['info'])
    morceaux = [m.strip() for m in info_brute.split('•')]
    t = "Non spécifié"
    a = "Non spécifiée"
    k = "Non spécifié"
    l = "Non spécifiée"

    for i, morceau in enumerate(morceaux):
        morceau_min = morceau.lower()
        
        if i == 0 and not re.match(r'^(19|20)\d{2}$', morceau):
            t = morceau
            
        elif re.match(r'^(19|20)\d{2}$', morceau):
            a = morceau
            
        elif 'mil' in morceau_min or 'km' in morceau_min or ' h' in morceau_min:
            k = re.sub(r'[^\d]', '', morceau) 
            
        elif i > 0:
            est_un_vendeur = any(mot in morceau_min for mot in mots_vendeurs)
            
            if not est_un_vendeur:
                mots_separes = morceau_min.replace(',', '').split()
                if ',' in morceau or 'us' in mots_separes or 'usa' in mots_separes:
                    l = morceau
    
    types.append(t)
    annees.append(a)
    kilometrages.append(k)
    localisations.append(l)

df['type'] = types
df['annee'] = annees
df['kilometrage'] = kilometrages
df['localisation'] = localisations

df = df.drop(columns=['info'])

print(df.head(10))

nom_fichier_nettoye = "camions_mascus_nettoye_test.csv"
df.to_csv(nom_fichier_nettoye, index=False, encoding="utf-8-sig")