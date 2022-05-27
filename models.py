from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login = LoginManager()

class UserModel (UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password) 

    # def set_address(self, address):
    #     self.address = address

    # def set_address(self, address):
    #     self.address = address

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


class RestaurantModel (UserMixin, db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password) 

    def __repr__(self) -> str:
        return super().__repr__()
    

class MenuModel (UserMixin, db.Model):
    __tablename__ = 'menu'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(80), nullable=False)
    restaurant = db.Column(db.String(80), nullable=False)

    def __repr__(self) -> str:
        return super().__repr__() 


class OrderModel (UserMixin, db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id= db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    product_quantity = db.Column(db.Integer)
    price_each = db.Column(db.String(80), nullable=False)
    restaurant = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    

    def __repr__(self) -> str:
        return super().__repr__() 