from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import os
from dotenv import load_dotenv

# Charge les variables d'environnement du fichier .env
load_dotenv()

app = Flask(__name__)

# Clé secrète pour Flask et CSRF (doit être dans ton .env)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey123')  # valeur par défaut pour dev

# Configuration base SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Modèle de données
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# Formulaire Flask-WTF pour sécuriser + valider l'ajout
class TaskForm(FlaskForm):
    title = StringField('Tâche', validators=[DataRequired(message="La tâche ne peut pas être vide"),
                                             Length(max=100, message="100 caractères max")])
    submit = SubmitField('Ajouter')

# Crée la base et les tables si besoin au premier chargement
@app.before_first_request
def create_tables():
    db.create_all()

# Page d’accueil
@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(title=form.title.data.strip())
        db.session.add(new_task)
        db.session.commit()
        flash("Tâche ajoutée avec succès!", "success")
        return redirect('/')
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks, form=form)

# Supprimer une tâche
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Tâche supprimée.", "info")
    else:
        flash("Tâche non trouvée.", "warning")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
