from curses import flash
from datetime import datetime
from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from wsgiref import validate
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
import uuid
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel, RestaurantModel, MenuModel, OrderModel
from seeks import DBUSER, DBPASS, DBHOST, DBPORT, DBNAME


class LoginForm(FlaskForm):
    name = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")

class SignupForm(FlaskForm):
    name=StringField(label="Enter name", validators=[DataRequired(), Length(min=1,max=16)])
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    address=StringField(label="Enter address", validators=[DataRequired(), Length(min=6,max=100)])
    phone=StringField(label="Enter phone", validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Register")

class OrderForm(FlaskForm):
    name=StringField(label="name", validators=[DataRequired(),Length(min=1,max=160)])
    price=PasswordField(label="price",validators=[DataRequired(), Length(min=1,max=16)])
    restaurant=StringField(label="restaurant", validators=[DataRequired(),Length(min=1,max=160)])
    quanty=StringField(label="quanty", validators=[DataRequired(),Length(min=1,max=160)])
    submit=SubmitField(label="Add to cart")

# class addmenuForm(FlaskForm):
#     name=StringField(label="Enter name", validators=[DataRequired(),Length(min=1,max=160)])
#     price=StringField(label="Enter price",validators=[DataRequired(), Length(min=1,max=16)])
#     restaurant=StringField(label="Enter restaurant", validators=[DataRequired(),Length(min=1,max=160)])

#     submit=SubmitField(label="Login")

# class confirmForm(FlaskForm):
#     order=OrderModel.query.filter_by(user_id=current_user.id,order_status="not complete").all()
#     name=SelectField(label="name", validators=[DataRequired()],choices=order)
#     submit=SubmitField(label="Confirm")


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

# def addRestaurant(name, email, password, address, phone):
#     #check if email or username exits
#     user=UserModel()
#     user.set_password(password)
#     user.email=email
#     user.name=name
#     user.address=address
#     user.phone=phone
#     db.session.add(user)
#     db.session.commit()

# @app.route("/restaurantregister",methods=['GET','POST'])
# def restaurantregister():
#     form=registerForm()
#     if form.validate_on_submit():
#         if request.method == "POST":
#             email=request.form["email"]
#             name=request.form["name"] 
#             address=request.form["address"]
#             phone=request.form["phone"]
#             pw=request.form["password"]
#             restaurants = RestaurantModel.query.filter_by(email = email).first()
#             print(restaurants)
#             if restaurants is not None and restaurants.check_password(pw) :
#                 login_user(restaurants)
#                 return redirect('/restaurantsaddmenu')
#             elif restaurants is not None and not restaurants.check_password(pw) :
#                 return redirect('/restaurantslogin')
#             else:
#                 addRestaurant(name, email, pw, address, phone)
#                 return redirect('/restaurantslogin')
#     # return render_template("register.html")
#     return render_template("restaurantsregister.html",form=form)

# @app.route("/restaurantslogin",methods=['GET','POST'])
# def restaurantslogin():
#     form=loginForm()
#     if form.validate_on_submit():
#         if request.method == "POST":
#             email=request.form["email"]
#             pw=request.form["password"]
#             restaurants = RestaurantModel.query.filter_by(email = email).first()
#             if restaurants is not None and restaurants.check_password(pw) :
#                 login_user(restaurants)
#                 return redirect('/restaurantsaddmenu')
#     return render_template("restaurantslogin.html",form=form)

# def addmenu(name, price, restaurant):
#     menu=MenuModel()
#     menu.name=name
#     menu.price=price
#     menu.restaurant=restaurant
#     db.session.add(menu)
#     db.session.commit()

# @app.route("/restaurantsaddmenu",methods=['GET','POST'])
# def restaurantsaddmenu():
#     form=addmenuForm()
#     if form.validate_on_submit():
#         if request.method == "POST":
#             name=request.form["name"]
#             price=request.form["price"]
#             restaurant =request.form["restaurant"]
#             addmenu(name,price,restaurant)
#             myData=MenuModel.query.all()
#             return render_template("menu.html", myData=myData)
#     return render_template("restaurantsaddmenu.html",form=form)


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            name=request.form["name"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(name = name).first()
            if user is not None and user.check_password(pw) :
                login_user(user)
                return redirect('/menu')
    return render_template("login.html",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        email=form.email.data
        address=form.address.data
        phone=form.phone.data

        user = UserModel.query.filter_by(name=name).first()
        if user:
            flash("username already in use. Try again with a different username")
            return redirect(url_for('signup'))
        else:
            addUser(name, email, password, address, phone)
            flash("User created successfully")
            return redirect(url_for('login'))

    return render_template("signup.html", form=form) 

@app.route("/menu",methods=['GET','POST'])
# @login_required
def showMenu():   
    print("getting menu")
    return render_template('menu.html')    


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
def order():
    myData=MenuModel.query.all()
    
    if request.method == "POST":
        order_id=uuid.uuid1()
        user_id=current_user.id
        for key in request.form:
            if key is not None:
                product_id = int(key)
                product_quantity =request.form[key]
                item=MenuModel.query.filter_by(id=product_id).first()
                product_name=item.name
                price_each=item.price
                restaurant=item.restaurant
                order_status="not complete"
                if int(product_quantity)>0:
                    addorder(order_id,product_id, product_name, product_quantity, price_each, restaurant, user_id, order_status)
        return redirect('/checkout')
    return render_template("order.html", myData=myData)

@app.route("/checkout",methods=['GET','POST'])
@login_required
def checkout():
    user_id=current_user.id
    Data=OrderModel.query.filter_by(user_id=user_id, order_status='not complete').all()
    totalprice=0
    for item in Data:
        totalprice+=float(item.price_each)*int(item.product_quantity)
    if request.method == 'POST':
        if request.form["action"] == "conform":
            for item in Data:
                item.change_status("dilevering")
                db.session.commit()
                # flash('Order Success!')
            return redirect('/map')
        elif request.form['action']=="cancel":
            for item in Data:
                id=item.id
                OrderModel.query.filter_by(id=id).delete()
                db.session.commit()
            return redirect('/order')

    return render_template("checkout.html", Data=Data, totalprice=totalprice)    

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
    estiamtetime=" for 30mins"
    mes+=estiamtetime
    return render_template("map.html",message=mes)


@app.route('/contact')
def contact():
    print("getting contact")
    return render_template('contact.html')        

@app.route('/about')
def about():
    print("getting about")
    return render_template('about.html')        

# @app.route('/comp')
# def comp():
#     return render_template('index.html')


@app.route('/tester')
def test():
    userdata=UserModel.query.all()
    menudata=MenuModel.query.all()
    restaurantdata=RestaurantModel.query.all()
    orderdata=OrderModel.query.all()
    return render_template('test.html', userdata=userdata, menudata=menudata, restaurantdata=restaurantdata, orderdata=orderdata)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)