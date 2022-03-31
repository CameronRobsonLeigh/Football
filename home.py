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
    'host': '34.89.109.27'
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

@app.route('/displayTeams', methods=['GET','POST'])
def displayTeams():
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {"league":"39","season":"2021"}

    headers = {
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "e2f9bcef3dmshedc9edd9a76d470p15b2f2jsnf4de69c73518"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    responseJSON = response.json()

    return responseJSON


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    teamID = request.form['favouriteTeam']

    config['database'] = 'footballdb'  # add new database to config dict
    con = mysql.connector.connect(**config)


    cursor = con.cursor()
    cursor.execute("INSERT INTO Users (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
    con.commit()  # and commit changes

    cursor = con.cursor()
    cursor.execute("SELECT UserId FROM Users WHERE email = %s", ([email]))
    out = cursor.fetchall()


    grabTeams = ""
    for row in out:
         cursor = con.cursor()
         cursor.execute("INSERT INTO FavouriteTeam (userID, teamID) VALUES (%s, %s)", (row[0], teamID))
         con.commit()  # and commit changes

         cursor = con.cursor()
         cursor.execute("SELECT * FROM FavouriteTeam WHERE userId = %s", ([row[0]]))
         grabTeams = cursor.fetchone()

    id ,user, team = grabTeams

    return "User ID " + str(user) + "Users Favourite team ID " + team


@app.route('/userlogin', methods=['POST'])
def userlogin():
    email = request.form['email']
    password = request.form['password']

    config['database'] = 'footballdb'  # add new database to config dict
    con = mysql.connector.connect(**config)

    cursor = con.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (email, password))
    out = cursor.fetchall()

    if len(out) == 0:
        return render_template("login.html", errorMessage = "Invalid Credentials")
    else:
        return render_template("index.html")
