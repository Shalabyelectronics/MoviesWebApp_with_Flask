# MoviesWebApp_with_Flask
This another practice project where we are going to build My top 10 Movies Web Application, we are going to practice working with getting Movies Data from TheMovieDB API and save that movies data in our database to display it in our web application.

![Move-web-app-with-flask](https://user-images.githubusercontent.com/57592040/160721231-b14d3f2c-42b9-4777-8ee4-ae1e15629745.gif)


## STEP 1
We need first to install all requirements frameworks and libraries, there is already a requirements text file that you can use it to do that by this command:
```python
pip install -r requirements.txt
```
Then we need to import all nessary classes and methods as showing below:
```python
# Flask class to create our web application and some others methods that will be used to render our html pages
# And redirect to other html pages finally request to check which method GET or POST was implemented.
from flask import Flask, render_template, redirect, url_for, request
# You can read the documentation of bootstrap-flask that allow us to use Bootstrap4 and 5 version as well
# https://bootstrap-flask.readthedocs.io/en/stable/migrate/
from flask_bootstrap import Bootstrap5
# SQlAlchemy will help us to connect and manage our sqlite3 database for this project.
from flask_sqlalchemy import SQLAlchemy
# FlaskForm class will help us to create Forms and generate them in our webpage as well.
from flask_wtf import FlaskForm
# wtforms will help us to get all Fields we need to our form
from wtforms import StringField, SubmitField
# validators is important to get the data under our condetions.
from wtforms.validators import DataRequired, Length
# tmdbsimple is a wrapper, written in Python, for The Movie Database (TMDb) API v3.
# You can find the github repo here https://github.com/celiao/tmdbsimple/
import tmdbsimple as tmdb
# We will need the os module to hide our The Movie Database API key
import os
# We need it for configration with tmdbsimple wrapper 
import requests
```

### Creating instances and setting up Configrations:

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# you need to create your own account on https://www.themoviedb.org/
tmdb.API_KEY = os.getenv("MOVIEDBAPI")# To get Api key you need to create an account on https://www.themoviedb.org/
# This two options with tmdb are optional as mentioned on thier Documentation.
tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.REQUESTS_SESSION = requests.Session()
# We will use a relative path to save our database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my-top-movies.db"
# this will hide SQLALchemy Warning 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Here we will create db instance and add our Flask app to SQlAlchemy class
db = SQLAlchemy(app)
# Here we will add Bootstrap5 to our Flask app.
Bootstrap5(app)
# We will use the link to joining poster_path to provide the movie cover later
IMAGE_MOVIEDB_URL = "https://image.tmdb.org/t/p/w500"
```

Before diving on our project we need to setup everythin we need after importing all nessarly classes and methods.
But Here I'm not going to explain each details for this project because our focuse will be on creating our Movies Database Model and how to use the Movie Database Api to fetch the movie data and save it to our database and display it as well.

## STEP 2 - CREATING OUR MOVIES MODEL


