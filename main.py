from flask import Flask, render_template, request, flash, redirect, url_for
from replit import web
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, login_required, logout_user, current_user, LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.String(500))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  notes = db.relationship('Note')


events = [{
  'todo': 'irrigate day 1',
  'start': '2023-03-03T10:30:00',
  'end': '2023-03-03T12:30:00',
  'area': 'Garden A'
}, {
  'todo': 'irrigate day 2',
  'start': '2023-03-04T10:30:00',
  'end': '2023-03-04T12:30:00',
  'area': 'Garden B'
}, {
  'todo': 'irrigate day 3',
  'start': '2023-02-16',
  'end': '2023-02-17',
  'area': 'Orchard A'
}, {
  'todo': 'irrigate day 4',
  'start': '2023-02-16',
  'end': '2023-02-17',
  'area': 'Orchard B'
}, {
  'todo': 'irrigate day 5',
  'start': '2023-03-07T13:00:00',
  'end': '2023-03-07T15:00:00',
  'area': 'Garden A'
}, {
  'todo': 'irrigate day 6',
  'start': '2023-03-08T10:00:00',
  'end': '2023-03-08T12:00:00',
  'area': 'Garden B'
}, {
  'todo': 'irrigate day 7',
  'start': '2023-03-09T09:00:00',
  'end': '2023-03-09T11:00:00',
  'area': 'Orchard A'
}, {
  'todo': 'irrigate day 8',
  'start': '2023-03-10T13:00:00',
  'end': '2023-03-10T15:00:00',
  'area': 'Orchard B'
}, {
  'todo': 'irrigate day 9',
  'start': '2023-03-13T10:00:00',
  'end': '2023-03-13T12:00:00',
  'area': 'Garden A'
}, {
  'todo': 'irrigate day 10',
  'start': '2023-03-14T13:00:00',
  'end': '2023-03-14T15:00:00',
  'area': 'Garden B'
}, {
  'todo': 'irrigate day 11',
  'start': '2023-03-15T10:00:00',
  'end': '2023-03-15T12:00:00',
  'area': 'Orchard A'
}, {
  'todo': 'irrigate day 12',
  'start': '2023-03-16T13:00:00',
  'end': '2023-03-16T15:00:00',
  'area': 'Orchard B'
}, {
  'todo': 'irrigate day 13',
  'start': '2023-03-17T10:00:00',
  'end': '2023-03-17T12:00:00',
  'area': 'Garden A'
}, {
  'todo': 'irrigate day 14',
  'start': '2023-03-20T13:00:00',
  'end': '2023-03-20T15:00:00',
  'area': 'Garden B'
}, {
  'todo': 'irrigate day 15',
  'start': '2023-03-21T10:00:00',
  'end': '2023-03-21T12:00:00',
  'area': 'Orchard A'
}, {
  'todo': 'irrigate day 16',
  'start': '2023-03-22T13:00:00',
  'end': '2023-03-22T15:00:00',
  'area': 'Orchard B'
}, {
  'todo': 'irrigate day 17',
  'start': '2023-03-23T10:00:00',
  'end': '2023-03-23T12:00:00',
  'area': 'Garden A'
}, {
  'todo': 'irrigate day 18',
  'start': '2023-03-24T13:00:00',
  'end': '2023-03-24T15:00:00',
  'area': 'Garden B'
}, {
  'todo': 'irrigate day 19',
  'start': '2023-03-27T10:00:00',
  'end': '2023-03-27T12:00:00',
  'area': 'Orchard A'
}, {
  'todo': 'irrigate day 20',
  'start': '2023-03-28T13:00:00',
  'end': '2023-03-28T15:00:00',
  'area': 'Orchard B'
}]


@app.route('/', methods=['GET', 'POST'])
# @login_required
def index():
  return render_template("Home.html")


@app.route('/about')
def about():
  return render_template("About.html")


@app.route('/home')
def home():
  return render_template("Home.html")


# @app.route('/logout')
# @login_required
# def logout():
# logout_user()
#   return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  # data = request.form
  # print(data)
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        print("correct password")
        flash('login successfully', category='success')
        # login_user(user, remember=True)
        print("login success")
        # return redirect(url_for('home'))
        return render_template("Home.html")
      else:
        flash('incorrect password', category='error')
        print("wrong password")
    else:
      flash('Email does not exist', category='error')
      print("email not exist")
  return render_template("Login.html", boolean=True)


@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
      flash('email already exist', category='error')
      print("email exist")
    elif len(email) < 4:
      flash('email must be greater than 4 characters', category='error')
      print("not short")
    elif len(password) < 5:
      flash('password must be greater than 5 characters', category='error')
    else:
      new_user = User(email=email,
                      password=generate_password_hash(password,
                                                      method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      # login_user(user, remember=True)
      flash('Account created', category='success')
      print("account create")
      return render_template("Home.html")
  return render_template("Sign-Up.html")


@app.route('/sustainable-practices')
def sustainablePractices():
  return render_template("Sustainable-Practices.html")


@app.route('/schedule')
def schedule():
  return render_template("Schedule.html", events=events)


# @app.route('/socheata', methods=['GET', 'POST'])
# def socheata():
#   NDVI = 0
#   if request.method == 'POST':
#     NIR = request.form.get('NIR')
#     print(NIR)
#     RGB = request.form.get('RGB')
#     print(RGB)
#     NDVI = (float(NIR) - float(RGB)) / (float(NIR) + float(RGB))
#     print(NDVI)
#   return render_template("socheata.html", NDVI=NDVI)

# create_database(app)
if not path.exists('website/' + DB_NAME):
  with app.app_context():
    db.create_all()
    print("create database")

# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(id):
#   return User.query.get(int(id))

web.run(app)

# def create_database(app):
