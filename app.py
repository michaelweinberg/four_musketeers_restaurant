from flask import Flask, render_template
import datetime
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', utc_dt=datetime.datetime.utcnow())

@app.route('/login')
def about():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)