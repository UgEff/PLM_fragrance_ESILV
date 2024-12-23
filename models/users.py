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
            db_path = os.path.join(path_data, "PLM.db")
            connection = sqlite3.connect(db_path)
            curseur = connection.cursor()

            curseur.execute("""
                SELECT username, password, role_code
                FROM users 
                WHERE username = ? AND password = ?;
            """, (self.username, self.password))
            
            result = curseur.fetchone()
            curseur.close()
            connection.close()

            if result:
                # Stocker le rôle dans la session
                return {"success": True, "role_code": result[2]}
            return {"success": False, "role_code": None}
        except Exception as e:
            print(f"ERREUR DE RECUPERATION DE DATA : {e}")
            return {"success": False, "role_code": None}

    def get_user_role(self, username):
        try:
            db_path = os.path.join(path_data, "PLM.db")
            connection = sqlite3.connect(db_path)
            curseur = connection.cursor()

            curseur.execute("""
                SELECT role, role_code
                FROM users 
                WHERE username = ?;
            """, (username,))
            
            result = curseur.fetchone()
            curseur.close()
            connection.close()

            if result:
                return {"role": result[0], "role_code": result[1]}
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération du rôle : {e}")
            return None

    def get_all_users(self):
        try:
            db_path = os.path.join(path_data, "PLM.db")
            connection = sqlite3.connect(db_path)
            curseur = connection.cursor()

            curseur.execute("""
                SELECT username, role, role_code
                FROM users
                ORDER BY role_code, username;
            """)
            
            users = curseur.fetchall()
            curseur.close()
            connection.close()

            # Convertir en liste de dictionnaires pour plus de clarté
            users_list = [
                {
                    "username": user[0],
                    "role": user[1],
                    "role_code": user[2]
                }
                for user in users
            ]
            
            return users_list
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []

    def delete_user(self, username):
        try:
            # Ne pas permettre la suppression de l'admin principal
            if username == "admin":
                raise Exception("Impossible de supprimer l'administrateur principal")

            db_path = os.path.join(path_data, "PLM.db")
            connection = sqlite3.connect(db_path)
            curseur = connection.cursor()

            curseur.execute("""
                DELETE FROM users 
                WHERE username = ? AND username != 'admin';
            """, (username,))
            
            connection.commit()
            curseur.close()
            connection.close()
            
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            raise e

#init=User()
#init.create_user("idir","bonjour","manager")
#init.valid_connection("idir","admin")
#init.valid_connection("admin","admin")