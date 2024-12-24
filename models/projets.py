import os
import sys
import json
from dotenv import load_dotenv
import sqlite3
from pathlib import Path
# Charger les variables d'environnement
load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))
# Récupérer la variable PATH_DATA de l'environnement
path_data = os.getenv("PATH_DATA")


class Projet:
    def __init__(self):
        self.name = None
        self.description = None
        self.manager = None
        self.create_date = None
        self.status = None
        self.status_code = 0

    def add_projet(self, name, description, manager, create_date, status, documents=None):
        """
        Ajoute un nouveau projet avec ses documents
        """
        try:
            self.name = name
            self.description = description
            self.manager = manager
            self.create_date = create_date
            self.status = status
            self.status_code = 0 if status == "IN PROGRESS" else (1 if status == "DONE" else 2)

            # Connexion à la base de données SQLite
            db_path = os.path.join(path_data, "PLM.db")
            connection = sqlite3.connect(db_path) 
            curseur = connection.cursor()

            # Requete insertion en base info projet
            curseur.execute("""
            INSERT INTO project (NAME, DESCRIPTION, MANAGER_NAME, CREATE_DATE, STATUS, STATUS_CODE)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (self.name, self.description, self.manager, self.create_date, self.status, self.status_code))
            connection.commit()

            # Récupérer l'ID du projet nouvellement créé
            project_id = curseur.lastrowid
            curseur.close()
            connection.close()

            ### TRAVAIL SUR LES JSON
            json_path = os.path.join(path_data, "projet.json")

            try:
                if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
                    with open(json_path, 'r') as file:
                        data_previous = json.load(file)
                        if not isinstance(data_previous, list):
                            raise ValueError("le fichier json ne contient pas une liste valide")
                else:
                    data_previous = []
            except Exception as e:
                print(f"Error : {e}")
                data_previous = []

            # Définition du nouveau projet
            data_now = {
                "id": project_id,
                "name": self.name,
                "description": self.description,
                "manager": self.manager,
                "create_date": self.create_date,
                "status": self.status,
                "status_code": self.status_code,
                "documents": documents or [],
                "Boms": []
            }

            # Merge fichier JSON
            data_previous.append(data_now)

            # Sauvegarde du fichier JSON
            with open(json_path, "w") as f:
                json.dump(data_previous, f, indent=4)

            return project_id

        except Exception as e:
            print(f"ERROR - INSERT : {e}")
            raise e

# METHODE ---- AFFICHER LES PROJETS
    def show_projet(self):
        try:
            db_path=os.path.join(path_data,"PLM.db")
            connection = sqlite3.connect(db_path) 
            curseur=connection.cursor()
        #Affichage de tout les projet
            curseur.execute("""
                    SELECT * FROM project
            """)
            result=curseur.fetchall()
            curseur.close()
            connection.close()
            
            for row in result:
                print(f"ID: {row[0]}, Name: {row[1]}, Description: {row[2]}, Manager: {row[3]}, Create Date: {row[4]}, Status: {row[5]}, Status Code: {row[6]}")
            return result
        except Exception as e:
            print(f"ERROR CODE : {e}")

    def get_last_project_id(self):
        try:
            db_path = os.path.join(path_data, "PLM.db")
            connection = sqlite3.connect(db_path)
            curseur = connection.cursor()
            curseur.execute("SELECT MAX(ID) FROM project")
            last_id = curseur.fetchone()[0]
            curseur.close()
            connection.close()
            return last_id if last_id is not None else 0
        except Exception as e:
            print(f"Erreur lors de la récupération du dernier ID: {e}")
            return 0

    def load_projects(self):
        """
        Charge les projets depuis le fichier JSON.
        Retourne une liste vide si le fichier n'existe pas ou en cas d'erreur.
        """
        try:
            json_path = os.path.join(path_data, "projet.json")
            if not os.path.exists(json_path):
                return []
                
            with open(json_path, "r", encoding="utf-8") as f:
                projects = json.load(f)
                if not isinstance(projects, list):
                    return []
                return projects
        except Exception as e:
            print(f"Erreur lors du chargement des projets: {e}")
            return []

#init=Projet()
#name="Malaga"
#description="Premier projet que l'on test"
#manager="ines abdi"
#create_date="16/11/2024"
#status="InProgess"
#init.add_projet(name,description,manager,create_date,status)
#init.show_projet()

