import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.mascus.com/transportation/trucks"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print(f"Scraping de la page : {url} ...")

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Vérifie si la requête a réussi

    soup = BeautifulSoup(response.text, "html.parser")

    # On cherche tous les conteneurs d'annonces
    trucks = soup.find_all("div", class_="SearchResult_searchResultItemWrapper__VVVnZ")

    results = []

    for truck in trucks:
        # On récupère la balise du nom
        nom_tag = truck.find("h3", class_="SearchResult_brandmodel__04K2L")
        
        # .get_text() permet de ne garder que le texte propre sans les balises HTML
        nom = nom_tag.get_text(strip=True) if nom_tag else "Nom non trouvé"
        
        infos_tag = truck.find("p", class_="basicText2Style")
        infos = infos_tag.get_text(strip = True) if infos_tag else "Pas d'information"
        
        prix_tag = truck.find("div", class_="heading5")
        prix = prix_tag.get_text(strip = True) if prix_tag else "Pas de prix"
        results.append({
            "nom": nom,
            "info": infos,
            "prix": prix
        })

    # Affichage des résultats
    for r in results:
        print(r)
    
    print(f"\nTotal trouvé sur la page 1 : {len(results)} camions.")

except Exception as e:
    print(f"Erreur lors du scraping : {e}")

