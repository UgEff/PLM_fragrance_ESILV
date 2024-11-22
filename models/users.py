import os
import sys
from dotenv import load_dotenv
import sqlite3
# Charger les variables d'environnement
load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))
# Récupérer la variable PATH_DATA de l'environnement
path_data = os.getenv("PATH_DATA")



class User:
    def __init__(self):
        self.username=None
        self.password=None
        self.role=None


#METHODE: ------ CREATION DES USERS
    def create_user(self,username,password,role):
        self.username=username
        self.password=password
        self.role=role
        role_code = 2 if role=='manager' else 3
        try:
            # Connexion à la base de données SQLite
            db_path=os.path.join(path_data,"PLM.db")
            connection = sqlite3.connect(db_path) 
            curseur=connection.cursor()

            curseur.execute(f"""
                INSERT INTO users(USERNAME,PASSWORD,ROLE,ROLE_CODE) VALUES 
                ('{self.username}','{self.password}','{self.role}','{role_code}');
            """)
            connection.commit()
            curseur.close()
            connection.close()
            print("CREATION USER DONE")
        except Exception as e:
            print(f"ERROR - INSERT USER : {e}")
        

#METHODE : ------ VERIFICATION CONNEXION 
    def valid_connection(self,username,password):
        self.username=username
        self.password=password
        try:
            # Connexion à la base de données SQLite
            db_path=os.path.join(path_data,"PLM.db")
            connection = sqlite3.connect(db_path) 
            curseur=connection.cursor()

            curseur.execute(f"""
                SELECT username,
                        password 
                FROM users 
                WHERE  username== ? and password== ?;
            """,(self.username,self.password))
            result=curseur.fetchone()
            curseur.close()
            connection.close()

            if result:
                coin=1
                return coin
            else:
                coin=0
                print(f"USERNAMES OR PASSWORD DOESN'T MATCH: {coin}")
                return coin
        except Exception as e:
            print(f"ERREUR DE RECUPERATION DE DATA : {e}")

#init=User()
#init.create_user("idir","bonjour","manager")
#init.valid_connection("idir","admin")
#init.valid_connection("admin","admin")