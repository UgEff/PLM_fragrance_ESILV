from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
from models.users import User
from models.projets import Projet
from models.bom import Bom
from models.load_projet import Load_projet
from datetime import datetime
import os
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Charger les variables d'environnement
load_dotenv()
# Récupérer la variable PATH_DATA de l'environnement
path_data = os.getenv("PATH_DATA")

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Définir les extensions autorisées
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_project_directories(project_name):
    """Crée les répertoires nécessaires pour un nouveau projet"""
    base_path = os.path.join(path_data, "doc", secure_filename(project_name))
    os.makedirs(base_path, exist_ok=True)
    return base_path

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/menu')
def menu():
    if 'username' not in session:
        return redirect(url_for('home'))
    role_code = session.get('role_code')
    return render_template('menu.html', 
                        is_admin=(role_code == 1),
                        is_manager=(role_code == 2))

@app.route('/login', methods=["GET", "POST"])
def login():
    init = User()
    try:
        if request.method == "POST":
            donnees = request.form
            user = donnees.get('nom')
            mdp = donnees.get("mdp")
            result = init.valid_connection(user, mdp)
            if result["success"]:
                # Stocker les informations de l'utilisateur dans la session
                session['username'] = user
                session['role_code'] = result["role_code"]
                print("CONNEXION ETABLIE")
                return redirect(url_for('menu'))
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
    if 'username' not in session or (session.get('role_code') != 1 and session.get('role_code') != 2):
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))

    init = Projet()
    if request.method == "POST":
        try:
            donnees = request.form
            titre = donnees.get('titre')
            description = donnees.get('description')
            manager = donnees.get('manager')
            create_date = donnees.get('create_date')
            status = donnees.get('status')

            # Créer les répertoires du projet
            project_path = create_project_directories(titre)

            # Gérer les documents du projet
            documents = []
            if 'documents' in request.files:
                files = request.files.getlist('documents')
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(project_path, filename)
                        file.save(file_path)
                        documents.append({
                            "name": filename,
                            "path": os.path.relpath(file_path, path_data),
                            "upload_date": datetime.now().strftime("%Y-%m-%d")
                        })

            # Ajouter le projet avec ses documents
            project_id = init.add_projet(titre, description, manager, create_date, status, documents)
            
            flash("Projet créé avec succès", "success")
            return redirect(url_for('add_bom', project_id=project_id))

        except Exception as e:
            flash(f"Erreur lors de la création du projet : {str(e)}", "error")
            return render_template('init_project.html')

    return render_template('init_project.html')

@app.route("/bom", methods=["GET", "POST"])
def bom():
    if 'username' not in session:
        return redirect(url_for('home'))

    init = Bom()
    try:
        if request.method == "POST":
            donnees = request.form
            project_id = int(donnees.get('project_id'))
            nameBom = donnees.get('bom_name')
            descriptionBom = donnees.get('description_bom')
            composantBom = donnees.getlist('components[]')
            specBom = donnees.get('spec')
            linkProduct = donnees.get('linkProduct')

            init.add_bom_project(project_id, nameBom, descriptionBom, composantBom, specBom, linkProduct)
            return redirect(url_for('project_bom', project_id=project_id))
        else:
            project_id = request.args.get('project_id')
            if not project_id:
                flash("ID du projet manquant", "error")
                return redirect(url_for('project_list'))
            return render_template('bom.html', project_id=project_id)

    except Exception as e:
        flash(f"Erreur lors de l'ajout du BOM : {str(e)}", "error")
        return redirect(url_for('project_list'))

@app.route('/project_list')
def project_list():
    # Tous les utilisateurs peuvent voir la liste des projets
    if 'username' not in session:
        flash("Accès non autorisé", "error")
        return redirect(url_for('home'))
    
    projet = Projet()
    projects_list = projet.load_projects()
    if projects_list is None:
        projects_list = []
    return render_template("project_list.html", 
                         posts=projects_list,
                         is_admin=(session.get('role_code') == 1),
                         is_manager=(session.get('role_code') == 2))

@app.route("/change_status", methods=["GET", "POST"])
def change_status():
    print(f"Info URL (formulaire) : {request.form.to_dict()}")  # Debug
    project_id = int(request.form.get("project_id"))
    new_status = request.form.get("new_status")
    print(f"ID du projet : {project_id}, Nouveau statut : {new_status}")  # Debug
    
    init = Load_projet()
    init.modif_status_project(project_id, new_status)
    
    return redirect(url_for("project_list"))

@app.route('/bom_list/<int:project_id>', methods=["GET"])
def project_bom(project_id):
    init = Load_projet()
    projets = init.load_projet()
    projet = next((p for p in projets if p["id"] == project_id), None)
    if projet:
        return render_template("bom_list.html", project=projet)
    else:
        return "Projet introuvable", 404

@app.route('/add_boms/<int:project_id>', methods=['GET', 'POST'])
def add_boms(project_id):
    # Seuls admin et manager peuvent ajouter des BOMs
    if 'username' not in session or (session.get('role_code') != 1 and session.get('role_code') != 2):
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))

    init = Bom()
    if request.method == "POST":
        try:
            # Récupérer les données des BOMs
            bom_names = request.form.getlist('bom_name[]')
            descriptions = request.form.getlist('description_bom[]')
            components = request.form.getlist('components[]')
            specs = request.form.getlist('spec[]')
            links = request.form.getlist('linkProduct[]')

            # Ajouter chaque BOM
            for i in range(len(bom_names)):
                # Convertir la chaîne de composants en liste
                component_list = [c.strip() for c in components[i].split(',')]
                
                init.add_bom_project(
                    project_id,
                    bom_names[i],
                    descriptions[i],
                    component_list,
                    specs[i],
                    links[i]
                )

            flash("BOMs ajoutés avec succès", "success")
            return redirect(url_for('project_bom', project_id=project_id))
            
        except Exception as e:
            flash(f"Erreur lors de l'ajout des BOMs : {str(e)}", "error")
            return redirect(url_for('add_boms', project_id=project_id))

    return render_template('add_boms.html', project_id=project_id)

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    # Tous les utilisateurs peuvent voir et ajouter des commentaires
    if 'username' not in session:
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))
    
    projet = Projet()
    projects = projet.load_projects()
    if projects is None:
        projects = []
    comments = load_comments()
    if comments is None:
        comments = []
    return render_template('comments.html', 
                         projects=projects, 
                         comments=comments,
                         is_admin=(session.get('role_code') == 1),
                         is_manager=(session.get('role_code') == 2))

@app.route('/get_boms/<int:project_id>')
def get_boms(project_id):
    init = Load_projet()
    projects = init.load_projet()
    project = next((p for p in projects if p["id"] == project_id), None)
    if project:
        return jsonify(project.get('Boms', []))
    return jsonify([])

@app.route('/add_comment', methods=['POST'])
def add_comment():
    try:
        project_id = request.form.get('project_id')
        bom_name = request.form.get('bom_name')
        comment_text = request.form.get('comment')
        
        # Récupérer le nom du projet depuis le fichier JSON
        json_path = os.path.join(path_data, "projet.json")
        with open(json_path, 'r') as file:
            projects = json.load(file)
            project = next((p for p in projects if p["id"] == int(project_id)), None)
            project_name = project["name"] if project else "Projet inconnu"
        
        # Créer le commentaire
        new_comment = {
            "project_id": int(project_id),
            "project_name": project_name,
            "bom_name": bom_name,
            "content": comment_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id": None,  # sera défini dans save_comment
            "status": "Non traité"
        }
        
        # Sauvegarder le commentaire
        save_comment(new_comment)
        
        flash("Commentaire ajouté avec succès", "success")
        return redirect(url_for('comments'))
    except Exception as e:
        flash(f"Erreur lors de l'ajout du commentaire : {str(e)}", "error")
        return redirect(url_for('comments'))

@app.route('/update_comment_status', methods=['POST'])
def update_comment_status():
    # Seuls admin et manager peuvent changer le statut des commentaires
    if 'username' not in session or (session.get('role_code') != 1 and session.get('role_code') != 2):
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))

    try:
        comment_id = request.form.get('comment_id')
        json_path = os.path.join(path_data, "comments.json")
        
        with open(json_path, 'r') as file:
            comments = json.load(file)
        
        # Mettre à jour le statut du commentaire
        for comment in comments:
            if comment['id'] == int(comment_id):
                comment['status'] = 'Traité'
                break
        
        # Sauvegarder les modifications
        with open(json_path, 'w') as file:
            json.dump(comments, file, indent=4)
        
        flash("Statut du commentaire mis à jour", "success")
        return redirect(url_for('view_comments'))
    except Exception as e:
        flash(f"Erreur lors de la mise à jour du statut : {str(e)}", "error")
        return redirect(url_for('view_comments'))

def save_comment(comment):
    json_path = os.path.join(path_data, "comments.json")
    try:
        if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
            with open(json_path, 'r') as file:
                comments = json.load(file)
                # Générer un nouvel ID pour le commentaire
                max_id = max([c['id'] for c in comments]) if comments else 0
                comment['id'] = max_id + 1
        else:
            comments = []
            comment['id'] = 1
        
        # Ajouter le statut initial
        comment['status'] = 'Non traité'
        comments.append(comment)
        
        with open(json_path, 'w') as file:
            json.dump(comments, file, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du commentaire : {e}")
        raise e

def load_comments():
    json_path = os.path.join(path_data, "comments.json")
    try:
        if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
            with open(json_path, 'r') as file:
                return json.load(file)
        return []
    except Exception as e:
        print(f"Erreur lors du chargement des commentaires : {e}")
        return []

@app.route('/view_comments')
def view_comments():
    comments = load_comments()
    # Trier les commentaires par date (plus récents en premier)
    comments.sort(key=lambda x: x['date'], reverse=True)
    return render_template('view_comments.html', comments=comments)

@app.route('/logout')
def logout():
    # Effacer la session
    session.clear()
    # Rediriger vers la page de connexion avec un message
    flash("Vous avez été déconnecté avec succès.", "success")
    return redirect(url_for('home'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # Vérifier si l'utilisateur est connecté et est admin
    if 'username' not in session or session.get('role_code') != 1:
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')

            user = User()
            user.create_user(username, password, role)
            
            flash("Utilisateur créé avec succès", "success")
            return redirect(url_for('menu'))
        except Exception as e:
            flash(f"Erreur lors de la création de l'utilisateur : {str(e)}", "error")
            return render_template('create_user.html')
    
    return render_template('create_user.html')

@app.route('/user_list')
def user_list():
    # Vérifier si l'utilisateur est connecté et est admin
    if 'username' not in session or session.get('role_code') != 1:
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))
    
    try:
        user = User()
        users = user.get_all_users()
        return render_template('user_list.html', users=users)
    except Exception as e:
        flash(f"Erreur lors du chargement des utilisateurs : {str(e)}", "error")
        return redirect(url_for('menu'))

@app.route('/delete_user/<username>', methods=['POST'])
def delete_user(username):
    # Vérifier si l'utilisateur est connecté et est admin
    if 'username' not in session or session.get('role_code') != 1:
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))
    
    try:
        user = User()
        user.delete_user(username)
        flash(f"L'utilisateur {username} a été supprimé avec succès", "success")
    except Exception as e:
        flash(f"Erreur lors de la suppression : {str(e)}", "error")
    
    return redirect(url_for('user_list'))

@app.route('/add_bom_document/<int:project_id>/<string:bom_name>', methods=['POST'])
def add_bom_document(project_id, bom_name):
    if 'username' not in session or (session.get('role_code') != 1 and session.get('role_code') != 2):
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))

    try:
        # Charger le projet
        init = Load_projet()
        projects = init.load_projet()
        project = next((p for p in projects if p["id"] == project_id), None)
        
        if not project:
            flash("Projet non trouvé", "error")
            return redirect(url_for('project_list'))

        # Créer le répertoire BOM s'il n'existe pas
        bom_path = os.path.join(path_data, "doc", 
                               secure_filename(project["name"]),
                               "bom_" + secure_filename(bom_name))
        os.makedirs(bom_path, exist_ok=True)

        # Gérer les fichiers
        if 'documents' in request.files:
            files = request.files.getlist('documents')
            documents = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(bom_path, filename)
                    file.save(file_path)
                    documents.append({
                        "name": filename,
                        "path": os.path.relpath(file_path, path_data),
                        "upload_date": datetime.now().strftime("%Y-%m-%d")
                    })

            # Mettre à jour le BOM dans le projet
            for bom in project["Boms"]:
                if bom["nameBom"] == bom_name:
                    if "documents" not in bom:
                        bom["documents"] = []
                    bom["documents"].extend(documents)

            # Sauvegarder les modifications
            with open(os.path.join(path_data, "projet.json"), "w") as f:
                json.dump(projects, f, indent=4)

            flash("Documents ajoutés avec succès", "success")
        else:
            flash("Aucun document fourni", "warning")

        return redirect(url_for('project_bom', project_id=project_id))

    except Exception as e:
        flash(f"Erreur lors de l'ajout des documents : {str(e)}", "error")
        return redirect(url_for('project_bom', project_id=project_id))

@app.route('/add_bom/<int:project_id>', methods=['GET', 'POST'])
def add_bom(project_id):
    if 'username' not in session or (session.get('role_code') != 1 and session.get('role_code') != 2):
        flash("Accès non autorisé", "error")
        return redirect(url_for('menu'))

    try:
        if request.method == "POST":
            donnees = request.form
            nameBom = donnees.get('bom_name')
            descriptionBom = donnees.get('description_bom')
            composantBom = donnees.getlist('components[]')
            specBom = donnees.get('spec')
            linkProduct = donnees.get('linkProduct')

            init = Bom()
            init.add_bom_project(project_id, nameBom, descriptionBom, composantBom, specBom, linkProduct)
            
            flash("BOM ajouté avec succès", "success")
            return redirect(url_for('project_bom', project_id=project_id))
        
        # GET request
        return render_template('bom.html', project_id=project_id)

    except Exception as e:
        flash(f"Erreur lors de l'ajout du BOM : {str(e)}", "error")
        return redirect(url_for('project_list'))

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        # Vérifier si l'utilisateur est connecté
        if 'username' not in session:
            flash("Accès non autorisé", "error")
            return redirect(url_for('home'))
        
        # Vérifier si le fichier existe
        file_path = os.path.join(path_data, filename)
        if not os.path.exists(file_path):
            flash("Le fichier demandé n'existe pas", "error")
            return redirect(url_for('project_list'))
            
        # Le chemin du répertoire sera le dossier parent du fichier
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        # Envoyer le fichier
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        flash(f"Erreur lors du téléchargement : {str(e)}", "error")
        return redirect(url_for('project_list'))
