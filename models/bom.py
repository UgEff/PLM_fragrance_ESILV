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
                    

    
    def add_bom_project(self,nameBom,descriptionBom,composantBom,specBom,linkProduct):
            json_path = os.path.join(path_data, "projet.json")

            try:
                if os.path.exists(json_path) and os.path.getsize(json_path)>0:
                    #load json file
                    with open(path_data+"projet.json",'r') as file:
                        data_previous=json.load(file)
                        if not isinstance(data_previous,list):
                            raise ValueError("le fichier json ne content pas une liste valide")
                
                    print(f"data_previous: {data_previous}")
                
                else:
                    data_previous=[]

                tab_id=[]
                for project in data_previous:
                        tab_id.append(project['id'])

                if project["id"]==tab_id[-1]:
                    project["Bom"] = {
                    "nameBom": nameBom,
                    "descriptionBom": descriptionBom,
                    "composantBom": composantBom,
                    "specBom": specBom,
                    "linkProduct": linkProduct
                }

                # Sauvegarder les données mises à jour
                with open(json_path, "w") as file:
                    json.dump(data_previous, file, indent=4)
                print(f"BOM ajouté au projet ID {tab_id[-1]} avec succès.")
            
            except Exception as e:
                print(f"Error : {e}")
                data_previous=[]
            
#init=Bom()
#init.add_bom_project('test1','test2','test3','test4')