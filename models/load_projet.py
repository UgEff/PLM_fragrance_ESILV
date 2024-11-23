import os
import sys
import json
from dotenv import load_dotenv
# Charger les variables d'environnement
load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))
# Récupérer la variable PATH_DATA de l'environnement
path_data = os.getenv("PATH_DATA")


class Load_projet:
    def __init__(self):
        self.tab={}

    def load_projet(self):
        try:
            with open(path_data+"projet.json",'r') as file:
                b=json.load(file)

            self.tab=b
            print(f"Retour de tab: {type(self.tab)}")
            print(f"Retour de tab: {self.tab[0].get('name')}")
            return self.tab
        except Exception as e:
            print(f"LODING ERROR : {e}")

        
    def modif_status_project(self, project_id, status_new):
        with open(path_data + "projet.json", 'r') as file:
            data_previous = json.load(file)
            if not isinstance(data_previous, list):
                raise ValueError("Le fichier JSON ne contient pas une liste valide")
        
        
        for project in data_previous:
            if project.get('id') == project_id:
                print(f"Projet trouvé avant modification : {project}")  # Avant modification
                project['status'] = status_new
                print(f"Projet trouvé après modification : {project}")  # Après modification
                break

        
        
        with open(path_data + "projet.json", 'w') as file:
            json.dump(data_previous, file, indent=4)
            print("Fichier JSON sauvegardé avec succès")

        print(f"Chemin du fichier JSON : {path_data+'projet.json'}")


                
        

