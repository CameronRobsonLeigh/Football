# useful bash commands = cls - clear console, deactivate - get out of virtual environment
# username = Cameron789
# env\Scripts\activate
# set FLASK_APP=Home
from flask import Blueprint, render_template, request, flash, redirect, url_for

from flask import request
from flask import Flask
from flask import render_template
import requests
import mysql.connector
from mysql.connector.constants import ClientFlag
from flask import session
import regex

# initializes the app (__name__ = the file name)
app = Flask(__name__)
app.secret_key = 'sessionkey'

config = {
    'user': 'root',
    'password': 'hello123',
    'host': '34.89.109.27',
    'database': 'footballdb'
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Login')
def login():
    return render_template("login.html")

@app.route('/LoginNew')
def loginNew():
    return render_template("loginnew.html")

@app.route('/logout')
def logout():
    session.pop("userid", None)
    return render_template("loginnew.html")

@app.route('/Registration')
def Registration():
    return render_template("registration.html")

@app.route('/Settings')
def UserSettings():

    #, value=animal
    userid = session['userid'][0]
    teamid = session['teamid'][0]

    con = mysql.connector.connect(**config)
    cursor = con.cursor()

    cursor.execute("SELECT Name FROM Users WHERE userid = %s", ([userid]))
    name = cursor.fetchone()

    cursor.execute("SELECT password FROM Users WHERE userid = %s", ([userid]))
    password = cursor.fetchone()

    cursor.execute("SELECT email FROM Users WHERE userid = %s", ([userid]))
    email = cursor.fetchone()

    # password = session['password']
    # email = session['email']
    # name = session['name']
    return render_template("UserSettings.html", userid = userid, name = name[0], email = email[0], password = password[0])

@app.route('/standings')
def standings():
    return render_template('live.html')

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

    teamid = session['teamid'][0]
    return render_template('fixture.html', value = teamid)


@app.route('/updateUser', methods=['GET','POST'])
def updateUser():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']

    con = mysql.connector.connect(**config)
    cursor = con.cursor()

    cursor.execute("UPDATE Users SET Name=%s, password=%s, email=%s WHERE UserId=%s", (name, password, email, session['userid'][0]))
    con.commit()  # and commit changes

    return redirect(url_for('UserSettings'))

@app.route('/deleteUser', methods=['GET','POST'])
def deleteUser():
    userid = session['userid'][0]
    con = mysql.connector.connect(**config)
    cursor = con.cursor()

    cursor.execute("DELETE FROM Users WHERE UserId=%s", ([userid]))
    con.commit()  # and commit changes

    cursor.execute("DELETE FROM FavouriteTeam WHERE UserId=%s", ([userid]))
    con.commit()  # and commit changes


    return redirect(url_for('Registration'))


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    teamID = request.form['favouriteTeam']
    con = mysql.connector.connect(**config)
    cursor = con.cursor()
    
    cursor.execute("INSERT INTO Users (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
    con.commit()  # and commit changes

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
    return redirect(url_for('loginNew'))


@app.route('/userlogin', methods=['POST'])
def userlogin():
    email = request.form['email']
    password = request.form['password']

    con = mysql.connector.connect(**config)

    cursor = con.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (email, password))
    out = cursor.fetchall()

    if len(out) == 0:
        return render_template("loginnew.html", errorMessage = "Invalid Credentials")
    else:
        cursor.execute("SELECT UserId FROM Users WHERE email = %s", ([email]))
        out = cursor.fetchone()
        userid = out
        print(userid)

        session['userid'] = userid

        cursor.execute("SELECT TeamId FROM FavouriteTeam WHERE UserId = %s", (session['userid']))
        out2 = cursor.fetchone()
        teamid = out2

        cursor.execute("SELECT Name FROM Users WHERE UserId = %s", (session['userid']))
        out3 = cursor.fetchone()
        name = out3

        session['teamid'] = teamid
        # session['password'] = password
        # session['name'] = name
        return redirect(url_for('UserSettings'))

if __name__ == '__main__':
    app.run(debug = True)