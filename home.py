# useful bash commands = cls - clear console, deactivate - get out of virtual environment
# username = Cameron789
# env\Scripts\activate
# set FLASK_APP=Home

from flask import request
from flask import Flask
from flask import render_template
import requests
import mysql.connector
from mysql.connector.constants import ClientFlag

# initializes the app (__name__ = the file name)
app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'hello123',
    'host': '34.89.79.78'
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Login')
def login():
    return render_template("login.html")

@app.route('/handle_data', methods=["POST"])
def handle_data():
    input = request.form['teams']

    url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"

    querystring = {"league":"39","season":"2020","team": input}

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "e2f9bcef3dmshedc9edd9a76d470p15b2f2jsnf4de69c73518"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']

    config['database'] = 'FootballDatabase'  # add new database to config dict
    con = mysql.connector.connect(**config)

    cursor = con.cursor()

    cursor.execute("INSERT INTO Users (userID, name, password, email) VALUES (1, %s, %s, %s)", (name, password, email))
    con.commit()  # and commit changes

    cursor.execute("SELECT * FROM Users")
    out = cursor.fetchall()
    for row in out:
        print(row)

    return email


@app.route('/userlogin', methods=['POST'])
def userlogin():
    email = request.form['email']
    password = request.form['password']

    config['database'] = 'FootballDatabase'  # add new database to config dict
    con = mysql.connector.connect(**config)

    cursor = con.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (email, password))
    out = cursor.fetchall()

    if len(out) == 0:
        return render_template("login.html", errorMessage = "Invalid Credentials")
    else:
        return render_template("index.html")
