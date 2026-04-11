# Scraper Mascus - Camions d'occasion

## Description

Ce projet est un script Python conçu pour extraire de manière automatisée les annonces de camions d'occasion depuis le site Mascus.com.

Il ne se contente pas de récupérer les données brutes : il intègre un pipeline de Data Cleaning à la volée grâce à la bibliothèque Pandas, afin de fournir un fichier CSV structuré, le propre et prêt pour l'analyse de données.

## Fonctionnalités principales

1. **Scrapping Multi-pages Automatisé :** 
    Parcours dynamiquement les pages de résultats jusqu'à atteindre la limite définie ou la fin du catalogue.

2. **Robustesse & Anti-Ban :**
    - Utilisation d'un `User-Agent` pour simuler un navigateur réel.
    - Implémentation de pauses (`time.sleep`) entre les requêtes pour respecter le serveur cible.
    - Gestion des erreurs de connexion.

3. **Nettoyage Intelligent des Données (Data Cleaning):**
    - Extraction précise de l'année via des expressions régulières (Regex).
    - Identification et formatage du kilométrage (suppression du texte pour ne gardeer que la valeur numérique).
    - Déduction de la localisation et exclusion automatique des noms de vendeurs.

4. **Tri et Export :** 
    Les données sont triées par année (de la plus récente à la plus acienne) et par modèle, puis exportées dans un format `.csv` standard (`utf-8-sig`) lisible directement dans Excel.

## Prérequis et Installation

Pour faire fonctionner ce script, vous devez avoir Python 3 installé sur votre machine.

1. Cloner le dépôt (ou télécharger le fichier `scrappingf_lo.py`).

2. **Installer les dépendances requises :**
    Ouvrez votre terminal et exécutez la commande suivante:
```bash
    pip install requests beautifulsoup4 pandas
```

## Utilisation

1. Ouvrez le fichier `scrappingf_lo.py` avec votre éditeur de code.

2. (Optionnel) Modifiez la variable `max_pages` à la ligne 15 pour définir le nombre de pages à scraper (par défaut: 5 pour les tests).

3. Lancez le script depuis votre terminal:
```bash
    python scrappingf_lo.py
```
Le script va afficher sa progression dans le terminal. Une fois terminé, un fichier nommé camions_mascus_nettoye.csv sera généré dans le même dossier.

Structure des données en sortie

Le fichier CSV généré contient les colonnes suivantes :

| nom | prix | type | annee |
| :--- | :---: | :---: | ---: |
| Freighliner Cascadia | 45,000 USD| Sleeper Trucks | 2018 |
| Volvo VNL | Pas de prix | Sleeper Trucks | 2015 |


## Avertissement

Ce script a été à des fins éducatives. Le web scraping peut être soumis aux Conditions Générales d'Utilisation (CGU) du site cible. Assurez-vous d'utiliser cet outil de manière responsable, en ne surchargeant pas les serverus (maintenez les délais `time.sleep`) et en respectant les règles locales sur la collecte de données.
