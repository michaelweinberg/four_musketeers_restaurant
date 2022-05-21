from flask import Flask, render_template
import datetime
app = Flask(__name__)

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