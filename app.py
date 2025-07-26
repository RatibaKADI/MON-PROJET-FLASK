import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# On récupère la clé secrète depuis .env
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise ValueError("No SECRET_KEY set for Flask application. Check your .env file")

csrf = CSRFProtect(app)

# Configuration base de données
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# Formulaire avec validation
class TaskForm(FlaskForm):
    title = StringField('Nouvelle tâche', validators=[DataRequired(message="La tâche ne peut pas être vide."), Length(max=100, message="La tâche est trop longue (max 100 caractères).")])
    submit = SubmitField('Ajouter')

# Page principale
@app.route('/')
def index():
    form = TaskForm()
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks, form=form)

# Ajouter une tâche
@app.route('/add', methods=['POST'])
def add():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(title=form.title.data)
        db.session.add(new_task)
        db.session.commit()
    else:
        # Tu peux afficher les erreurs dans le HTML, donc pas besoin de faire autre chose ici
        pass
    return redirect('/')

# Supprimer une tâche
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
