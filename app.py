from flask import Flask, render_template, request, redirect, url_for, flash
from models.users import User
from models.projets import Projet
from models.bom import Bom
from models.load_projet import Load_projet

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    init = User()
    try:
        if request.method == "POST":
            donnees = request.form
            user = donnees.get('nom')
            mdp = donnees.get("mdp") 
            verif_co = init.valid_connection(user, mdp) 
            if verif_co == 1:
                print("CONNEXION ETABLIE") 
                return render_template('menu.html')
            else:
                flash("Connexion échouée. Veuillez vérifier vos identifiants.", "warning")
                return redirect(url_for('home'))
        else:
            return render_template('login.html')
    except Exception as e:
        flash(f"Erreur : {e}", "danger")
        return redirect(url_for('home'))

@app.route('/init_project', methods=["GET", "POST"])
def init_project():
    init=Projet()
    if request.method == "POST":

        donnees = request.form
        print(f"les données de notre projets:{donnees}")
        titre = donnees.get('titre')
        description = donnees.get('description')
        manager = donnees.get('manager')
        create_date = donnees.get('create_date')
        status=donnees.get('status')
        init.add_projet(titre,description,manager,create_date,status)
        message="ADD PROJET"
        flash(message, "success")

        return redirect('bom')
    return render_template('init_project.html')

@app.route("/bom",methods=["GET","POST"])
def bom():
    init=Bom()
    try:
        if request.method=="POST":
            donnees = request.form
            nameBom=donnees.get('bom_name')
            descriptionBom=donnees.get('description_bom')
            composantBom=donnees.getlist('components[]')
            specBom=donnees.get('spec')

            init.add_bom_project(nameBom,descriptionBom,composantBom,specBom)
            return redirect(url_for('menu'))
        else:
            print("ERROR")
            return render_template(url_for('bom'))
            
    except Exception as e:
        print(f"ERROR : {e}")
    return render_template("bom.html")

@app.route('/project_list',methods=["GET","POST"])
def project_list():
    init=Load_projet()
    projet=init.load_projet()
    return render_template("project_list.html",posts=projet)

@app.route('/bom_list/<int:project_id>', methods=["GET"])
def project_bom(project_id):
    init = Load_projet()
    projets = init.load_projet()
    
    # Trouver le projet par ID
    projet = next((p for p in projets if p["id"] == project_id), None)
    if projet:
        return render_template("bom_list.html", project=projet)
    else:
        return "Projet introuvable", 404
