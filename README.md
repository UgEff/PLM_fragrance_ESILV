# PLM Projet ESILV

## 📖 Description

**PLM Projet ESILV** est une application Flask conçue pour gérer des projets et leurs BOM (Bill of Materials). Elle permet aux utilisateurs de :

- Créer et visualiser des projets.
- Associer des BOM avec des spécifications aux projets.
- Suivre l'évolution des statuts des projets.

L'application est idéale pour la gestion simplifiée de projets dans un environnement académique ou industriel.

---

## ✨ Fonctionnalités

- **🔐 Connexion utilisateur :** Interface pour se connecter et accéder aux fonctionnalités.
- **📝 Création de projets :** Ajout de projets avec des détails comme nom, description et manager.
- **📋 Gestion des BOM :** Associez des BOM (Bill of Materials) avec des spécificités à vos projets.
- **👀 Visualisation :** Affichez les projets créés et leurs BOM associés.
- **📊 Suivi des statuts :** Gestion des statuts des projets avec des mises à jour comme "IN PROGRESS", "DONE", ou "CANCEL".
- **🔗 Liens hypertextes :** Ajout d'hyperliens SolidWorks dans les projets pour un suivi avancé (fonctionnalité en cours de développement).

---

## 🖥️ Installation

### Prérequis

- Python 3.8+
- Flask
- Un environnement virtuel Python (optionnel mais recommandé)

## 🔧 Configuration

1. Clonez le dépôt Git

   ```bash
       git clone <URL_DU_DEPOT>
       cd PLM_PROJET
   ```

2. Installer les dépendances  
   Installez les dépendances nécessaires depuis le fichier requirements.txt

   ```bash
   pip install -r requirement.txt
   ```

3. Créer un répertoire data

   ```bash
   mkdir data
   cp .env.example .env
   ```

4. Copier le chemin du répertoire data dans le fichier .env

   ```makefile
       PATH_DATA=<chemin_vers_repertoire_data>
   ```

5. Initialiser la base de données

   ```bash
   python database/init_database.py
   ```

6. Lancer l'application depuis le main.py

   ```bash
   python main.py
   ```

---

## 🚀 Utilisation

Accédez à l'application à l'adresse : http://127.0.0.1:5000
Connectez-vous avec un compte utilisateur.
Créez et gérez vos projets et BOM via l'interface.

## 📂 Structure du projet

```bash
PLM_PROJET/
├── database/               # Gestion des données
│   ├── init_database.py    # Script d'initialisation de la base de données SQLite
│   ├── PLM.db              # Fichier de la base de données SQLite
│   └── projet.json         # Fichier JSON pour les données des projets (alternative ou complément à SQLite)
│
├── models/                 # Modèles Python pour la logique métier
│   ├── __init__.py         # Initialisation du package "models"
│   ├── bom.py              # Modèle pour la gestion des BOM
│   ├── load_projet.py      # Gestion du chargement des projets
│   ├── projets.py          # Modèle pour les projets
│   └── users.py            # Gestion des utilisateurs et des profils
│
├── static/                 # Ressources statiques (CSS, images, JS, etc.)
│   └── style.css           # Feuille de style pour l'interface utilisateur
│
├── templates/              # Templates HTML pour l'interface utilisateur
│   ├── bom.html            # Formulaire pour créer un BOM
│   ├── bom_list.html       # Liste des BOM
│   ├── init_project.html   # Formulaire pour créer un projet
│   ├── login.html          # Page de connexion utilisateur
│   ├── menu.html           # Menu principal
│   └── project_list.html   # Liste des projets
│
├── .env                    # Fichier des variables d'environnement (configurations sensibles)
├── app.py                  # Application Flask principale
├── main.py                 # Point d'entrée de l'application (exécution)
├── README.md               # Documentation du projet
└── requirements.txt        # Liste des dépendances Python nécessaires
```

## ⚖️ Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.
