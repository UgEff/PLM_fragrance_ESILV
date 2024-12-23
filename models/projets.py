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
        self.name=None
        self.description=None
        self.manager=None
        self.create_date=None
        self.status=None
        self.status_code=0

# METHODE : ------- CREATION DE PROJET 
    def add_projet(self,name,description,manager,create_date,status):
        self.name=name
        self.description=description
        self.manager=manager
        self.create_date=create_date
        self.status=status
        self.status_code

        try:
            # Connexion à la base de données SQLite
            db_path=os.path.join(path_data,"PLM.db")
            connection = sqlite3.connect(db_path) 
            curseur=connection.cursor()

            #  Requete insertion en base info projet
            curseur.execute("""
            INSERT INTO project (NAME, DESCRIPTION, MANAGER_NAME, CREATE_DATE, STATUS, STATUS_CODE)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (self.name, self.description, self.manager, self.create_date, self.status, self.status_code))
            connection.commit()

            #Requete pour recuperer les infos des projets
            curseur.execute("""
                    SELECT * FROM project
            """)
            result=curseur.fetchall()
            # init list vide
            lst_id=[]

            for row in result:
                lst_id.append(row[0])
            curseur.close()
            connection.close()

            print("INSERT IS DONE")
            last_element=lst_id[-1]
            print(f"last_element : {last_element}")

            ### TRAVAIL SUR LES JSON
            json_path = os.path.join(path_data, "projet.json")

            try:
                if os.path.exists(json_path) and os.path.getsize(json_path)>0:
                    #load json file
                    with open(path_data+"projet.json",'r') as file:
                        data_previous=json.load(file)
                        if not isinstance(data_previous,list):
                            raise ValueError("le fichier json ne content pas une liste valide")
                
                else:
                    data_previous=[]
            except Exception as e:
                print(f"Error : {e}")
                data_previous=[]

        

            #defintion d'un dico vide
            data_now={
                "id":last_element,
                "name":self.name,
                "description":self.description,
                "manager":self.manager,
                "create_date":self.create_date,
                "status":self.status,
                "status_code":self.status_code,
                "Boms": []
            }

            ### MERGE FICHIER JSON
            data_previous.append(data_now)
            
            try:
                # creation d'un fichier json
                with open(path_data+"projet.json","w") as f:
                    json.dump(data_previous,f,indent=4)
                print("le fichier JSON est mis a jour")
            except Exception as e:
                print(f"Error lors de la mise a jour du fichier : {e}")
                
        except Exception as e:
            print(f"ERROR - INSERT  : {e}")

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

