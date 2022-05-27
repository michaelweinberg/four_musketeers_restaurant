from wsgiref import validate
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from yelp import find_coffee
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel, RestaurantModel, MenuModel, OrderModel
import datetime




DBUSER= 'lhhung'
DBPASS= 'password'
DBHOST= 'db'
DBPORT= '5432'
DBNAME= 'pglogindb'

app = Flask(__name__)
app.secret_key="a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
    user=DBUSER,
    passwd=DBPASS,
    host=DBHOST,
    port=DBPORT,
    db=DBNAME
)
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

@app.route('/')
def home():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route('/login')
def about():
    return render_template('login.html')

@app.route('/tester')
def test():
    userdata=UserModel.query.all()
    menudata=MenuModel.query.all()
    restaurantdata=RestaurantModel.query.all()
    orderdata=OrderModel.query.all()
    return render_template('test.html', userdata=userdata, menudata=menudata, restaurantdata=restaurantdata, orderdata=orderdata)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)