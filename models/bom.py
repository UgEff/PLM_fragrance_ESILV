import os
import sys
import json
from dotenv import load_dotenv
# Charger les variables d'environnement
load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))
# Récupérer la variable PATH_DATA de l'environnement
path_data = os.getenv("PATH_DATA")

class Bom:
    def __init__(self):
        self.nameBom=None
        self.descriptionBom=None
        self.composantBom=[]
        self.specBom=None
        self.linkProduct=None
                    

    
    def add_bom_project(self, project_id, nameBom, descriptionBom, composantBom, specBom, linkProduct):
        json_path = os.path.join(path_data, "projet.json")

        try:
            # Charger le fichier JSON existant
            with open(json_path, 'r') as file:
                projects = json.load(file)

            # Trouver le projet correspondant
            for project in projects:
                if project["id"] == int(project_id):
                    # S'assurer que la liste Boms existe
                    if "Boms" not in project:
                        project["Boms"] = []
                    
                    # Créer un nouveau BOM
                    new_bom = {
                        "nameBom": nameBom,
                        "descriptionBom": descriptionBom,
                        "composantBom": composantBom,
                        "specBom": specBom,
                        "linkProduct": linkProduct
                    }
                    
                    # Ajouter le BOM à la liste des BOMs du projet
                    project["Boms"].append(new_bom)
                    break

            # Sauvegarder les modifications
            with open(json_path, "w") as file:
                json.dump(projects, file, indent=4)
            print(f"BOM ajouté au projet ID {project_id} avec succès.")
        
        except Exception as e:
            print(f"Error : {e}")
            raise e

#init=Bom()
#init.add_bom_project('test1','test2','test3','test4')