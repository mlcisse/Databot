# DataBot

Cette plateforme permet de créer des **bots intelligents** capables de répondre à des questions concernant une **source de données spécifique (CSV)**.
Elle est basée sur **Streamlit**, **pandas**, et un **modèle d’intentions SVM** pour comprendre et exécuter des requêtes en langage naturel.
	
# Prérequis

- **Python 3.11**
- **Git** installé sur la machine 
- **pip** (généralement installé avec Python)
- Recommandé : créer un environnement virtuel
  👉 [Documentation officielle `venv`](https://docs.python.org/3/library/venv.html) 
  👉 [Documentation `conda` (optionnel)](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
  
### Cloner le projet et accéder au dossier

- git clone "url_du_repo"
- cd databot

### Créer et activer l'environnement virtuel (Linux/Ubuntu) 

- python3 -m venv .venv
- source .venv/bin/activate

### Installer les dépendances dans l'environnement
(Assurez vous d'être dans l'environnement virtuel activé)

- pip install -r requirements.txt

### Ajouter la clé API
(Dans la racine du projet, copiez le fichier d’exemple pour créer le fichier de configuration réel puis ajoutez la clé entre les guillements "")

- cp databot_config.example.json databot_config.json

### Lancer l'application

streamlit run main.py

L’interface du Databot s’ouvre automatiquement dans votre navigateur (sinon, ouvrez manuellement l’URL indiquée dans le terminal, par défaut http://localhost:8501).

Aller dans l’onglet Admin

- Cliquez sur Browse pour charger le fichier dataset.csv
- Lancez l’entraînement du modèle
- Une fois l’entraînement terminé, cliquez sur Execute pour démarrer le Databot

Aller dans l’onglet Playground

- Vous pouvez poser toutes les questions concernant les données. 
- Le Databot peut répondre sous forme de texte et générer des graphiques lorsque c’est pertinent.


Voici quelques exemples de questions que de tests.

- Display rent distribution across all cities
- Which heating type has the highest total monthly rent? Show it with a bar chart
- Show a scatter plot of rent vs surface area
- What is the average monthly rent for each city ?
- Calculate the rent increase percentage per year
- Which type of housing is the most affordable?
- What is the maximum rent?
- Show rent distribution for different property types


### Évaluer le modèle d'intentions 

python eval_intents.py --csv eval_intents.csv --outdir eval_results


