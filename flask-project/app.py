from curses import flash
from datetime import datetime
from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from wsgiref import validate
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from yelp import find_coffee
import uuid
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel, RestaurantModel, MenuModel, OrderModel

class loginForm(FlaskForm):
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Login")

class registerForm(FlaskForm):
    name=StringField(label="Enter name", validators=[DataRequired(), Length(min=1,max=16)])
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    address=StringField(label="Enter address", validators=[DataRequired(), Length(min=6,max=100)])
    phone=StringField(label="Enter phone", validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Register")

class addmenuForm(FlaskForm):
    name=StringField(label="Enter name", validators=[DataRequired(),Length(min=1,max=160)])
    price=StringField(label="Enter price",validators=[DataRequired(), Length(min=1,max=16)])
    restaurant=StringField(label="Enter restaurant", validators=[DataRequired(),Length(min=1,max=160)])

    submit=SubmitField(label="Login")

# class confirmForm(FlaskForm):
#     order=OrderModel.query.filter_by(user_id=current_user.id,order_status="not complete").all()
#     name=SelectField(label="name", validators=[DataRequired()],choices=order)
#     submit=SubmitField(label="Confirm")

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
@app.route("/home")
@login_required
def findCoffee():
    return render_template("home.html", myData=find_coffee())

@app.route("/")
def redirectToLogin():
    return redirect("/login")

@app.route("/login",methods=['GET','POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(email = email).first()
            if user is not None and user.check_password(pw) :
                login_user(user)
                return redirect('/menu')
    return render_template("login.html",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route("/register",methods=['GET','POST'])
def register():
    form=registerForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            name=request.form["name"] 
            address=request.form["address"]
            phone=request.form["phone"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(email = email).first()
            print(user)
            if user is not None and user.check_password(pw) :
                login_user(user)
                return redirect('/menu')
            elif user is not None and not user.check_password(pw) :
                return redirect('/login')
            else:
                addUser(name, email, pw, address, phone)
                return redirect('/login')
    # return render_template("register.html")
    return render_template("register.html",form=form)



def addRestaurant(name, email, password, address, phone):
    #check if email or username exits
    user=UserModel()
    user.set_password(password)
    user.email=email
    user.name=name
    user.address=address
    user.phone=phone
    db.session.add(user)
    db.session.commit()

@app.route("/restaurantregister",methods=['GET','POST'])
def restaurantregister():
    form=registerForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            name=request.form["name"] 
            address=request.form["address"]
            phone=request.form["phone"]
            pw=request.form["password"]
            restaurants = RestaurantModel.query.filter_by(email = email).first()
            print(restaurants)
            if restaurants is not None and restaurants.check_password(pw) :
                login_user(restaurants)
                return redirect('/restaurantsaddmenu')
            elif restaurants is not None and not restaurants.check_password(pw) :
                return redirect('/restaurantslogin')
            else:
                addRestaurant(name, email, pw, address, phone)
                return redirect('/restaurantslogin')
    # return render_template("register.html")
    return render_template("restaurantsregister.html",form=form)

@app.route("/restaurantslogin",methods=['GET','POST'])
def restaurantslogin():
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            pw=request.form["password"]
            restaurants = RestaurantModel.query.filter_by(email = email).first()
            if restaurants is not None and restaurants.check_password(pw) :
                login_user(restaurants)
                return redirect('/restaurantsaddmenu')
    return render_template("restaurantslogin.html",form=form)

def addmenu(name, price, restaurant):
    menu=MenuModel()
    menu.name=name
    menu.price=price
    menu.restaurant=restaurant
    db.session.add(menu)
    db.session.commit()

@app.route("/restaurantsaddmenu",methods=['GET','POST'])
def restaurantsaddmenu():
    form=addmenuForm()
    if form.validate_on_submit():
        if request.method == "POST":
            name=request.form["name"]
            price=request.form["price"]
            restaurant =request.form["restaurant"]
            addmenu(name,price,restaurant)
            myData=MenuModel.query.all()
            return render_template("menu.html", myData=myData)
    return render_template("restaurantsaddmenu.html",form=form)

@app.route("/menu",methods=['GET','POST'])
# @login_required
def showMenu():
    print('cccccccc')
    myData=MenuModel.query.all()
    return render_template("menu.html", myData=myData)

def addorder(order_id,product_id, product_name, product_quantity, price_each, restaurant, user_id, order_status):
    order=OrderModel()
    order.order_id=order_id
    order.product_id=product_id
    order.product_name=product_name
    order.product_quantity=product_quantity
    order.price_each=price_each
    order.restaurant=restaurant
    order.user_id=user_id
    order.order_status=order_status
    db.session.add(order)
    db.session.commit()

@app.route("/order",methods=['GET','POST'])
@login_required
def myOrder():
    print('bbbbbbbbb')
    myData=MenuModel.query.all()
    
    if request.method == "POST":
        print('aaaaaaaaaa')
        s_option=request.form.getlist("s_option")
        print(s_option)
        user_id=current_user.id
        order_id=uuid.uuid1()
        for product_id in s_option:
            print(product_id)
            item=MenuModel.query.filter_by(id=product_id).first()
            product_name=item.name
            product_quantity=1
            price_each= item.price
            restaurant=item.restaurant
            order_status="not complete"
            addorder(order_id,product_id, product_name, product_quantity, price_each, restaurant, user_id, order_status)
        return redirect('/checkout')
    return render_template("myorder.html", myData=myData)

@app.route("/checkout",methods=['GET','POST'])
@login_required
def checkout():
    user_id=current_user.id
    # order_status="not complete"
    Data=OrderModel.query.filter_by(user_id=user_id, order_status='not complete').all()
    # name=SelectField(label="confirm", validators=[DataRequired()],choices=order)
    
    # submit=SubmitField(label="Confirm")
    # form=confirmForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        if request.form['submit']=="1":
            for item in Data:
                item.change_status("dilevering")
                db.session.commit()
                # flash('Order Success!')
                return redirect('/map')
        # elif request.form['update']=="1":
        #     res=request.form.getlist("numrequest")
        #     flash(res)
        #     for item in Data:
        #         num=res[0]
        #         item.change_product_quantity(num)
        #         db.session.commit()
    return render_template("checkout.html", Data=Data)    

@app.route("/map",methods=['GET','POST'])
def maptime():
    user=current_user
    cur_order=OrderModel.query.filter_by(user_id=user.id, order_status='dilevering').first()
    
    rest_name=cur_order.restaurant
    restaurant=RestaurantModel.query.filter_by(name=rest_name).first()
    rest_add=restaurant.address
    user_add=user.address
    mes=""
    mes+=rest_add
    mes+="-->"
    mes+=user_add
    return render_template("map.html",message=mes)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
