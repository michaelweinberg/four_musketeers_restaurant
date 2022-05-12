from flask import Flask, render_template
import datetime
from models import db, login, UserModel

DBUSER = 'tcss506'
DBPASS = 'Tcss_506_restaurant!'
DBHOST = 'database-sql.c9xp7kbwvtsm.us-east-1.rds.amazonaws.com'
DBPORT = '3306'
DBNAME = 'tcss506'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{user}:{passwd}@{host}:{port}/{db}'.format(
    user=DBUSER,
    passwd=DBPASS,
    host=DBHOST,
    port=DBPORT,
    db=DBNAME
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def addUser(username,address, password,phone):
    #check if email or username exits
    user=UserModel()
    user.set_password(password)
    user.username=username
    user.address=address
    user.phone=phone
    db.session.add(user)
    db.session.commit()

@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(username = "testcustomer").first()
    if user is None:
        addUser("testcustomer", "university of washington tacoma", "00000000", "111-111-1111")   


@app.route('/')
def home():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route('/login')
def about():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)