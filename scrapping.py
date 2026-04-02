from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd


def sleep(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))



# CONFIG
NB_PAGES = 358
BASE_URL = "https://www.mascus.com/transportation/trucks?page={}"

driver = webdriver.Chrome()
all_links = []


# ETAPE 1 : LIENS
#print("Récupération des liens...")



for page in range(1, NB_PAGES + 1):
    driver.get(BASE_URL.format(page))
    sleep(4, 5)  #  pause plus longue pour chargement
    trucks = driver.find_elements(By.CSS_SELECTOR, "div[class*='SearchResult_searchResultItemWrapper']")

    
    for truck in trucks:
        try:
            link = truck.find_element(By.CSS_SELECTOR, "a[href*='/transportation/']").get_attribute("href")
            if link:
                all_links.append(link)
        except:
                 pass

# petite pause entre pages

    sleep(2, 4)
    # sauvegarde

    if page % 20 == 0:
        pd.DataFrame(all_links, columns=["link"]).to_csv("liens_recuperes.csv", index=False)



# enlever doublons
all_links = list(set(all_links))
print(f"i{len(all_links)} liens récupérés")



# ETAPE 2 : DETAILS

data = []
for i, link in enumerate(all_links):
    driver.get(link)
    sleep(4,6)
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
        price = None
        items = driver.find_elements(By.CSS_SELECTOR, "div.key-value-wrapper")
        for item in items:
            try:
                label = item.find_element(By.CLASS_NAME, "key-value-label").text.strip()
        
                if "Price Including Tax" in label:
                    price = item.find_element(By.CLASS_NAME, "key-value-value").text.strip()
            except:
                 pass


        data.append({

            "titre": title,
            "prix": price,
            "annee": info.get("Year"),
            "Km": info.get("Meter read-out"),
            "pays": info.get("Country"),
             "type": info.get("Category"),
            "modele": info.get("Brand / model"),
             "lien": link

        })

    except Exception as e:
        print("Erreur :", e)

# pause entre chaque camion
sleep(3, 5)
# sauvegarde
if i % 50 == 0:
    pd.DataFrame(data).to_csv("mascus_camions.csv", index=False)

driver.quit()



# EXPORT FINAL
df = pd.DataFrame(data)
df.to_csv("camions_mascus.csv", index=False)
print(" Scrapping terminé ") 