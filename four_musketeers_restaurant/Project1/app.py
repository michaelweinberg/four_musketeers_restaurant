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
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), unique=True, nullable=False)
    password = db.Column(db.String(90), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"User('{self.username}')"

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class MainAppForm(FlaskForm):
    birth_date = DateField("date", format='%Y-%m-%d',
                           validators=[DataRequired()])
    how_many = DecimalField("how many", validators=[
        DataRequired(), NumberRange(1, 20)])
    submit = SubmitField("submit")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")


class SignupForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = MainAppForm()
    birth_date = form.birth_date.data
    how_many = form.how_many.data

    birthdays = []

    if form.validate_on_submit():

        day = birth_date.day
        month = birth_date.month
        year = birth_date.year
        how_many = int(form.how_many.data)

        birthdays = get_birthdays(year, month, day, how_many)
        if len(birthdays) == 0:
            flash(
                "Some birthdays in this date don't have thumbnails. please try a different date.")

        return render_template("index.html", form=form, birthdays=birthdays, len=len)

    return render_template("index.html", form=form, birthdays=birthdays, len=len)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            flash("Logged in successfully")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password. Please try again")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            flash("username already in use. Try again with a different username")
            return redirect(url_for('signup'))
        else:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            flash("User created successfully")
            return redirect(url_for('login'))

    return render_template("signup.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("index"))


def get_birthdays(year, month, day, how_many):
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/births/{month}/{day}"
    data = requests.get(url).json()
    births = data["births"]
    births.sort(key=lambda x: abs(int(x["year"])-int(year)))

    del births[how_many:]

    essential_data = []

    try:

        for birth in births:
            essential_data.append(
                {"name": birth["text"], "year": birth["year"], "thumbnail": birth["pages"][0]["thumbnail"]["source"]})
    except:
        pass

    return essential_data


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
