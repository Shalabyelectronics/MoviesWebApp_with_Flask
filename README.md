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

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import tmdbsimple as tmdb
import os
import requests
```

### Creating instances and setting up Configrations:

Before diving in our project we need to setup everythin we need after importing all nessarly classes and methods.
