from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd

# FONCTION PAUSE
def human_sleep(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))


# CONFIG
NB_PAGES = 358
BASE_URL = "https://www.mascus.com/transportation/trucks?page={}"

driver = webdriver.Chrome()

all_links = []


# ETAPE 1 : LIENS
#print("🔎 Récupération des liens...")

for page in range(1, NB_PAGES + 1):
    #print(f"Page {page}/{NB_PAGES}")
    
    driver.get(BASE_URL.format(page))
    human_sleep(4, 7)  #  pause plus longue pour chargement

    trucks = driver.find_elements(By.CSS_SELECTOR, "div[class*='SearchResult_searchResultItemWrapper']")

    for truck in trucks:
        try:
            link = truck.find_element(By.CSS_SELECTOR, "a[href*='/transportation/']").get_attribute("href")
            if link:
                all_links.append(link)
        except:
            pass

    # petite pause entre pages
    human_sleep(2, 4)

    # sauvegarde
    if page % 20 == 0:
        pd.DataFrame(all_links, columns=["link"]).to_csv("backup_links.csv", index=False)

# enlever doublons
all_links = list(set(all_links))

print(f"i{len(all_links)} liens récupérés")


# ETAPE 2 : DETAILS
data = []

for i, link in enumerate(all_links):
    #print(f"{i+1}/{len(all_links)}")

    driver.get(link)
    human_sleep(3, 6)

    try:
        info = {}
        items = driver.find_elements(By.CSS_SELECTOR, "div.key-value-wrapper")

        for item in items:
            try:
                label = item.find_element(By.CLASS_NAME, "key-value-label").text.strip()
                value = item.find_element(By.CLASS_NAME, "key-value-value").text.strip()
                info[label] = value
            except:
                pass

        # titre
        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
        except:
            title = None

        # prix
        try:
            price = driver.find_element(By.CSS_SELECTOR, "div.heading5").text
        except:
            price = None

        data.append({
            "titre": title,
            "prix": price,
            "annee": info.get("Year"),
            "km": info.get("Meter read-out"),
            "pays": info.get("Country"),
            "type": info.get("Category"),
            "modele": info.get("Brand / model"),
            "lien": link
        })

    except Exception as e:
        print("Erreur :", e)

    # pause entre chaque camion
    human_sleep(2, 5)

    # sauvegarde
    if i % 50 == 0:
        pd.DataFrame(data).to_csv("backup_links.csv", index=False)

driver.quit()

# EXPORT FINAL
df = pd.DataFrame(data)
df.to_csv("camions_mascus.csv", index=False)

print(" Scraping terminé ")