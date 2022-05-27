
from wsgiref import validate
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from yelp import find_coffee
from flask_sqlalchemy import SQLAlchemy
#from flask_login import current_user, login_user, login_required, logout_user
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, login, UserModel, RestaurantModel, MenuModel, OrderModel
import datetime


DBUSER= 'lhhung'
DBPASS= 'password'
DBHOST= 'db'
DBPORT= '5432'
DBNAME= 'pglogindb'

app = Flask(__name__)
SECRET_KEY = 'fehiu4y74gh894hg49t8t484'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
    user=DBUSER,
    passwd=DBPASS,
    host=DBHOST,
    port=DBPORT,
    db=DBNAME
)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

def addUser(name, email, password, address, phone):
    #check if email or username exits
    user=UserModel()
    user.set_password(password)
    user.email=email
    user.name=name
    user.address=address
    user.phone=phone
    db.session.add(user)
    db.session.commit()

@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = "lhhung@uw.edu").first()
    if user is None:
        addUser("lhhung", "lhhung@uw.edu","qwerty","university of washington tocama", "1111111111")    
        return 

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


#class MainAppForm(FlaskForm):
#    birth_date = DateField("date", format='%Y-%m-%d',
#                           validators=[DataRequired()])
#    how_many = DecimalField("how many", validators=[
#        DataRequired(), NumberRange(1, 20)])
#    submit = SubmitField("submit")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")


class SignupForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")
    

@app.route('/')
@login_required
def home():
    return render_template('home.html', utc_dt=datetime.datetime.utcnow())

@app.route('/login', methods=["GET", "POST"])
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

@app.route('/tester')
def test():
    userdata=UserModel.query.all()
    menudata=MenuModel.query.all()
    restaurantdata=RestaurantModel.query.all()
    orderdata=OrderModel.query.all()
    return render_template('test.html', userdata=userdata, menudata=menudata, restaurantdata=restaurantdata, orderdata=orderdata)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
