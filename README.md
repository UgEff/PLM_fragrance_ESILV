# PLM Projet ESILV

## 📖 Description

**PLM Projet ESILV** est une application Flask de gestion de cycle de vie des produits (PLM). Elle permet une gestion complète des projets, des BOM (Bill of Materials) et des utilisateurs avec différents niveaux d'accès.

---

## ✨ Fonctionnalités

### 🔐 Gestion des Utilisateurs
- **Système de Rôles :**
  - **Admin :** Accès complet à toutes les fonctionnalités
  - **Manager :** Gestion des projets et des BOM
  - **Utilisateur :** Consultation et commentaires
- **Authentification sécurisée**
- **Gestion des utilisateurs** (création, suppression, liste)

### 📝 Gestion des Projets
- **Création de projets** (Admin et Manager)
  - Ajout d'informations de base (titre, description, manager, date)
  - Upload de documents multiples (PDF, DOC, DOCX, XLS, XLSX, PNG, JPG, JPEG)
  - Création automatique d'une structure de dossiers
- **Liste des projets** (tous les utilisateurs)
- **Suivi des statuts** (IN PROGRESS, DONE, CANCEL)
- **Gestion des documents**
  - Téléchargement des documents
  - Visualisation de la date d'upload
  - Organisation par projet et par BOM
- **Gestion des BOM** avec spécifications
- **Liens vers les fichiers SolidWorks**

### 💬 Système de Commentaires
- **Ajout de commentaires** (tous les utilisateurs)
- **Visualisation des commentaires**
- **Gestion des statuts** des commentaires (Admin et Manager)

### 🔒 Contrôle d'Accès
- **Restrictions basées sur les rôles**
- **Sessions sécurisées**
- **Protection des routes sensibles**

---

## 🖥️ Installation

### Prérequis
- Python 3.8+
- Flask
- SQLite3
- Environnement virtuel Python (recommandé)

### Configuration

1. **Cloner le dépôt**
   ```bash
   git clone <URL_DU_DEPOT>
   cd PLM_PROJET
   ```

2. **Créer et activer l'environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration de l'environnement**
   ```bash
   mkdir database
   cp .env.example .env
   ```
   Éditez `.env` avec votre chemin de données :
   ```
   PATH_DATA=<chemin_vers_repertoire_data>
   ```

5. **Initialiser la base de données**
   ```bash
   python database/init_database.py
   ```

6. **Lancer l'application**
   ```bash
   python main.py
   ```

---

## 🚀 Utilisation

### Accès à l'application
- URL : http://127.0.0.1:5000
- Compte admin par défaut :
  - Utilisateur : admin
  - Mot de passe : admin

### Niveaux d'accès

#### 👑 Administrateur
- Gestion complète des utilisateurs
- Création et gestion des projets
- Gestion des BOM
- Gestion des commentaires
- Modification des statuts

#### 👨‍💼 Manager
- Création et gestion des projets
- Gestion des BOM
- Ajout et gestion des commentaires
- Modification des statuts

#### 👤 Utilisateur Standard
- Consultation des projets
- Consultation des BOM
- Ajout de commentaires
- Consultation des commentaires

---

## 📂 Structure du Projet

```bash
PLM_PROJET/
├── database/               # Gestion des bases de données
│   ├── init_database.py    # Initialisation SQLite
│   ├── PLM.db             # Base de données SQLite
│   └── projet.json        # Données JSON des projets
│
├── doc/                    # Documents des projets
│   ├── projet1/           # Documents du projet 1
│   │   ├── documents/     # Documents généraux
│   │   └── bom/          # Documents des BOMs
│   └── projet2/           # Documents du projet 2
│
├── models/                 # Logique métier
│   ├── bom.py             # Gestion des BOM
│   ├── load_projet.py     # Chargement des projets
│   ├── projets.py         # Gestion des projets
│   └── users.py           # Gestion des utilisateurs
│
├── static/                 # Ressources statiques
│   └── style.css          # Styles CSS
│
├── templates/             # Templates HTML
│   ├── bom.html           # Création de BOM
│   ├── bom_list.html      # Liste des BOM
│   ├── comments.html      # Gestion des commentaires
│   ├── create_user.html   # Création d'utilisateur
│   ├── init_project.html  # Création de projet
│   ├── login.html         # Page de connexion
│   ├── menu.html          # Menu principal
│   ├── project_list.html  # Liste des projets
│   ├── user_list.html     # Liste des utilisateurs
│   └── view_comments.html # Vue des commentaires
│
├── .env                   # Variables d'environnement
├── app.py                 # Application Flask
├── main.py               # Point d'entrée
└── requirements.txt      # Dépendances Python
```

---

## 🔄 Base de Données

### SQLite (PLM.db)
- Table Users : Gestion des utilisateurs et rôles
- Table Projects : Informations de base des projets
- Autres tables selon besoins

---

## ⚖️ Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
