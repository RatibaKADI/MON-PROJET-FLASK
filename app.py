from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db') + '?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clé secrète pour sécuriser les formulaires CSRF
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')  # fallback pour dev local

db = SQLAlchemy(app)

# Modèle de données
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# Page d’accueil
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Ajouter une tâche
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title and title.strip():  # ignore les titres vides ou espaces seulement
        new_task = Task(title=title.strip())
        db.session.add(new_task)
        db.session.commit()
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
