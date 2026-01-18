# 📊 Global CO2 Emissions Dashboard (1970–2024)

Ce dashboard interactif permet de visualiser l'évolution des émissions de dioxyde de carbone (CO₂) à l'échelle mondiale sur plus de 50 ans. Il met en lumière les disparités régionales et l'évolution historique des principaux émetteurs mondiaux.

## 📈 Gestion et Traitement des Données

Le projet repose sur les données de la base **EDGAR (Emissions Database for Global Atmospheric Research)**. La structure des fichiers est la suivante :

* **Source de données originale (`Edgar_data_CO2.csv`)** : Ce fichier contient les données brutes extraites du site officiel d'EDGAR. C'est sur ce fichier source que toute l'étape de **Data Processing** (nettoyage, gestion des valeurs manquantes, filtrage et formatage) a été effectuée.
* **Fichier de production (`co2_data_clean.csv`)** : Il s'agit du jeu de données final après traitement. Le dashboard utilise exclusivement ce fichier pour garantir une performance optimale et un affichage précis des résultats.

## 🚀 Comment lancer le dashboard localement

Suivez ces étapes pour installer et lancer l'application sur votre environnement Python local :

### 1. Cloner le dépôt
```bash
git clone [https://github.com/VOTRE_NOM_UTILISATEUR/Global-Co2-emissions-dashboard.git](https://github.com/VOTRE_NOM_UTILISATEUR/Global-Co2-emissions-dashboard.git)
cd Global-Co2-emissions-dashboard  

### 2.Installer les dépendances
Il est recommandé d'utiliser un environnement virtuel. Installez les bibliothèques requises ```bash:
pip install -r requirements.txt  

### 3. Lancer l'application :
Exécutez le script principal ```bash : python app.py  
Une fois le serveur lancé, accédez au dashboard via votre navigateur à l'adresse : http://127.0.0.1:7860

## 🔗 Accès Direct (Cloud)
Vous pouvez tester le dashboard directement en ligne sans aucune installation via Hugging Face Spaces :  
👉 **[Dashboard CO2 Emissions - Mahmoud TOURKI](https://huggingface.co/spaces/tourki24/dashboard-co2-emissions)**