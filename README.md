# FOOTBALL LIVE SCORES⚽
This website displays live fixtures of users favourite football teams in the premier league.

## Table of contents

* [About](#About "Goto About")

* [Working](#Working )

* [Guide to run WebApp](#Guide)

* [References](#References)


 

      
  

## About 
  
 We designed a web application for this project that takes the user's favourite soccer teams and links them to an external API to get the appropriate fixtures. This web app was created to look and work like soccer apps like the Barclays Premier League app. The football API from the rapid API website was used in this case.


## Working
 
The web app operates as follows: the user is first led to a home page with three pages shown in the navigation bar. A user will register on the Signup page. Multiple forms on the signup page collect information such as a user's name, email address, and password.

This information is transmitted to a MYSQL database stored on Google Cloud once it is submitted. The data base will return a single int that reflects the user's id. On the same page, there is a dropdown menu from which a user can choose their favourite team.
This information is also saved in the MYSQL cloud. The user is directed to the login page after completing the registration process. The login page operates as follows: the user's email address and password are entered.

This email and password are then compared to the user and password in the Google Cloud database. The user will be successfully logged in if the user and password in a specific row of the database match the ones entered. A session is started when a user logs in, and it is active for as long as the user is logged in.

After logging into their account, users are directed to the user settings page. A user can edit their information on the user settings page by filling out the form, which allows them to alter their name, email, and password. New pages appear in the navigation bar on this page, including a logout option that deletes the current session and leads the user to a login page, as well as live fixture and team fixture sites.


The team fixture page pulls current data from the user's favourite football team drop down. For example, if a user selects Manchester United as their favourite team, the team fixtures page will display all the team's current fixtures. The live fixtures page, on the other hand, does not accept any input arguments and merely outputs the fixtures of any team that is playing on that day.  

##### Guide
## Guide to run WebApp
> Running the Web Application Locally on Windows and Ubuntu.

##### Download the source code and extract the contents to run this repository locally, or clone the repository.

#### Windows
> Visual Studio Code

1. In your VS code terminal, open CMD.

2. To activate the environment.
```
.\env\Scripts\activate

```
3. Setting the FLASK_ENV environment variable to 'development' will
  enable debug mode.
  
```
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

##### Ubuntu
> Terminal

1. To begin, open the cloud shell and clone the repository as follows:
```
git clone https://github.com/CameronRobsonLeigh/Football.git

```
2. Enter the repository by typing
```
cd Football/
```
3. Creating a new Virtual Environment.
```
python3 -m venv venv
```
4. Activate the enviroment.
```
source venv/bin/activate
```
5. Installing the dependencies.
```
pip install -r requirements.txt
````
6. Flask run
```
flask run
```



### References 

*Reference [Football API](https://www.api-football.com/)*

*To create a [Docker container](https://docs.github.com/en/github-ae@latest/actions/creating-actions/creating-a-docker-container-action#creating-a-dockerfile)*

*Google Kubernetes Engine[GKE](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app)*


