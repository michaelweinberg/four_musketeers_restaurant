from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login = LoginManager()

class UserModel (UserMixin, db.Model):
    __tablename__ = 'CUSTOMER'
    
    username = db.Column(db.varchar(15), primary_key=True)
    address = db.Column(db.varchar(300), nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    phone = db.Column(db.varchar(15), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)   

@login.user_loader
def load_user(username):
    return UserModel.query.get(username)
    
    
