from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import requests
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

SECRET_KEY = 'fehiu4y74gh894hg49t8t484'
SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"

app = Flask(__name__)

# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# db = SQLAlchemy(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

@app.route('/')
def home():
    return render_template('home.html', utc_dt=datetime.datetime.utcnow())

@app.route('/login')
def login():
    print("loggin in")
    return render_template('login.html')

@app.route('/menu')
def menu():
    print("getting menu")
    return render_template('menu.html')    

@app.route('/contact')
def contact():
    print("getting contact")
    return render_template('contact.html')        

@app.route('/about')
def about():
    print("getting about")
    return render_template('about.html')        

@app.route('/comp')
def comp():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)