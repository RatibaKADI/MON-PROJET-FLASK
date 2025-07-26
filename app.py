import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

app = Flask(__name__)

# Récupérer la clé secrète depuis .env
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("La clé secrète SECRET_KEY n'est pas définie dans .env")

csrf = CSRFProtect(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

class TaskForm(FlaskForm):
    title = StringField('Nouvelle tâche', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Ajouter')

@app.route('/')
def index():
    form = TaskForm()
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks, form=form)

@app.route('/add', methods=['POST'])
def add():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(title=form.title.data)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        # Crée les tables si elles n'existent pas (évite l'erreur "no such table")
        db.create_all()
    app.run(debug=True)
