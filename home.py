# useful bash commands = cls - clear console, deactivate - get out of virtual environment
# BBCweather6969!
# username = Cameron789
# env\Scripts\activate
# set FLASK_APP=Home
from flask import request
from flask import Flask
from flask import render_template
import requests
# initializes the app (__name__ = the file name)
app = Flask(__name__)

# defines the index

@app.route('/')
def index():
    return render_template("index.html")

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

@app.route('/User')
def User():
    return "User Page here"

