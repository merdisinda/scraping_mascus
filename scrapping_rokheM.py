# Scraping d'une page de Mascus pour tester

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#Paramètres
adresse_site = "https://www.mascus.com/transportation/trucks"

#Lancement du navigateur
parametres = Options()
parametres.add_argument("--window-size=1920,1080")
navigateur = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=parametres)

navigateur.get(adresse_site)
WebDriverWait(navigateur, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='SearchResult']"))
)
time.sleep(2)
navigateur.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

#Récupération des annonces
annonces = navigateur.find_elements(By.CSS_SELECTOR, "[class*='SearchResult_detailWrapper']")
print(f"{len(annonces)} annonces trouvées\n")

liste_donnees = []

for annonce in annonces:
    try:
        # Titre + lien
        lien_element = annonce.find_element(By.CSS_SELECTOR, "a[href*='/transportation/']")
        adresse_lien = lien_element.get_attribute("href")
        lien_complet = adresse_lien if adresse_lien.startswith("http") else "https://www.mascus.com" + adresse_lien
        try:
            titre = lien_element.find_element(By.CSS_SELECTOR, "h3").text.strip()
        except:
            titre = lien_element.text.strip()

        # Détails : type • année • kilométrage • ville  (ex: "Curtain Side • 2011 • 251034mil • Paris")
        details = []
        try:
            paragraphe = annonce.find_element(By.CSS_SELECTOR, "p[class*='basicText']")
            texte_brut = navigateur.execute_script(
                "return Array.from(arguments[0].childNodes)"
                ".filter(n => n.nodeType === 3)"
                ".map(n => n.textContent).join('').trim();", paragraphe
            ).strip().strip('"')
            details = [x.strip() for x in texte_brut.split("•") if x.strip()]
        except:
            pass

        # Prix
        prix = None
        try:
            prix = annonce.find_element(By.CSS_SELECTOR, "[class*='priceWrapper'] [role='button']").text.strip()
        except:
            try:
                prix = annonce.find_element(By.XPATH, ".//*[contains(text(),'USD') or contains(text(),'EUR')]").text.strip()
            except:
                pass

        liste_donnees.append({
            "titre":        titre,
            "lien":         lien_complet,
            "categorie":    details[0] if len(details) > 0 else None,
            "annee":        details[1] if len(details) > 1 else None,
            "kilometrage":  details[2] if len(details) > 2 else None,
            "ville":        details[3] if len(details) > 3 else None,
            "prix":         prix,
        })

    except Exception as erreur:
        print(f"Erreur sur une annonce : {erreur}")

navigateur.quit()

#Affichage 
for ligne in liste_donnees:
    print(ligne)
print(f"\n{len(liste_donnees)} annonces extraites")

#Export CSV 
with open("mascus.csv", "w", newline="", encoding="utf-8-sig") as fichier:
    colonnes = ["titre", "lien", "categorie", "annee", "kilometrage", "ville", "prix"]
    ecrivain = csv.DictWriter(fichier, fieldnames=colonnes)
    ecrivain.writeheader()
    ecrivain.writerows(liste_donnees)
