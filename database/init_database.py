#-----------------------------------------------------
#           Code pour init table sql
# init admin role 
#-----------------------------------------------------
import sqlite3
import os
import sys
from dotenv import load_dotenv


# Charger les variables d'environnement
load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))

# Récupérer la variable PATH_DATA de l'environnement
path_data = os.getenv("PATH_DATA")

if path_data is None:
    raise ValueError("La variable d'environnement PATH_DATA n'est pas définie.")

# Connexion à la base de données SQLite
db_path=os.path.join(path_data,"PLM.db")
connection = sqlite3.connect(db_path)
print("Connexion réussie à la base de données.")

try:

    cursor=connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            USERNAME TEXT,
            PASSWORD TEXT,
            ROLE TEXT,
            ROLE_CODE INT);
        """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            NAME TEXT,
            DESCRIPTION TEXT,
            MANAGER_NAME TEXT,
            CREATE_DATE TEXT,
            STATUS TEXT,
            STATUS_CODE
            );
        """)

    cursor.execute(""" 
        INSERT INTO users(USERNAME,PASSWORD,ROLE,ROLE_CODE) VALUES ('admin','admin','admin',1);
    """)    
    

    connection.commit()
    connection.close()

except Exception as e:
    print(f"Error {e}")