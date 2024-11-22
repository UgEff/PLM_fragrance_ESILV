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
