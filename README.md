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

Before diving on our project we need to setup everythin we need after importing all necessarily classes and methods.
But Here I'm not going to explain each details for this project because our focuse will be on creating our Movies Database Model and how to use the Movie Database Api to fetch the movie data and save it to our database and display it as well.

## STEP 2 - CREATING OUR MOVIES MODEL

Our Movies Model will includes 9 Columns as mentioned below:
```python
# Database Movies Table
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True, default="I loved it!!!")
    image_url = db.Column(db.String(20), nullable=False, default='static/images/default.jpg')
```
And I build this Model after checking which Movie data I can get from Movie DataBase API, and it is many actually but what is important for us the below:
1. (id) and it will generate automaticly
2. (title) We will get it from Movie DataBase API
3. (type) or Genre,  We will get it from Movie DataBase API
4. (year)  We will get it from Movie DataBase API
5. (description)  We will get it from Movie DataBase API
6. (rating)  We will get it from Movie DataBase API
7. (ranking) This will be some tricky because we will order to movies from lower rating to higher so we will generate numbers from max movies list to the min
8. (review) will have default value but we can also edit it later.
9. (image_url) We will get it from Movie DataBase API

And I know all that because I tried first the Movie Database API and you can do so in your interactive python consol by importing everything and start experiments your instances and methodes like this:

```python
from main import *
>>> search = tmdb.Search()
>>> response = search.movie(query='The Bourne')
>>> for s in search.results:
...     print(s['title'], s['id'], s['release_date'], s['popularity'])
...
The Bourne Ultimatum 2503 2007-08-03 55.2447062124256
The Bourne Supremacy 2502 2004-07-23 43.4553609681985
The Bourne Identity 2501 2002-06-06 38.5531563780592
The Bourne Legacy 49040 2012-08-10 9.90635210153143
The Bourne Identity 8677 1988-05-08 1.53988446573129
Bette Bourne: It Goes with the Shoes 179304  0.23
```
For more details you can check tmdbsimple documentation [Here](https://github.com/celiao/tmdbsimple/)
## STEP 3 - CREATE OUR FORM AND DO SOME EXPIRAMENTS.

Now we need to create our form to get the data from the user and process the results, but what data we need exactly?? Yes, you gussed it again. We need the movie title to use it for searching to all related movies with Movie Database API.

We are going to use FlaskForm and WTForms as well so our form will look like this:

```python
class MoveTitle(FlaskForm):
    movie_title = StringField("Movie Title", validators=[DataRequired(), Length(min=2, max=250)])
    submit = SubmitField("Done")
```
So we are almost ready but first we need to activate our database and to do so we can do that from importing our `db` instance and create all Models and save it to our database, we can do so by this code on python interactive console
```python
from main import db
```
If you did not get any error so you are on the right path else you need to check your flask alchemy setup. Then we need to create our Books database table by using this line of code:
```python
db.create_all()
```
And you will see your database file will be created and place on the selected path. Now we can add data to our table by import the Model from our app script file and create an objects that referring to each row of data in our Movies table. I recommend you to do some experiment before implementing any code to your flask web app so you will be fully understanding of how you can deal with it later.

So first expirament is lets add a movie by using Movies Model as below:
```python
movie = Movies(title="Drive", type="Action", year=2011, 
                description="A mysterious Hollywood stuntman and mechanic moonligh
                ts as a getaway driver and finds himself in trouble when he helps 
                out his neighbor in this action drama.",rating=8.5, ranking=10,
                review="I Loved it!!!",
                image_url="https://www.cityonfire.com/wp-content/uploads/2012/02/drive-movie-poster-2011-"\                                      "1020745540.jpg")
```
then you need it to add it to that database and commit it as well like this:
```python
db.session.add(movie)
db.session.commit()
```
Great now we are ready to view our first movie in our home page but again we need to create our home function route and render our html home and pass it our movie instance. and this what we are going to do next step.

## STEP 4 - VIEW OUR FIRST MOVIE
Because we are using bootstrap-flask we need to fellow its documentation because it is different from flask-bootstrap. I encourage you to spend some time with it so you can setup your html pages with bootstrap, you can get the documentation [HERE](https://bootstrap-flask.readthedocs.io/en/stable/migrate/)

After sitting up your home page in our project it will be index.html our home route function will look like this:

```python
@app.route("/")
def home():
    movies_order_by_rating = db.session.query(Movies).order_by(Movies.rating)
    all_movies = []
    movies_length = len([m for m in movies_order_by_rating])
    rank = [num for num in range(movies_length, 0, -1)]
    for index, movie in enumerate(movies_order_by_rating):
        movie.ranking = rank[index]
        db.session.commit()
        all_movies.append(movie)
    return render_template("index.html", movies=all_movies)
```
Here we will stop for a while to explain what going on... First line in our home route function is 
```python
movies_order_by_rating = db.session.query(Movies).order_by(Movies.rating)
```
Well this line of code will order by Movies by their rating from lower rating to higher rating. if you want the opposite I mean from higher to lower you can add this line of code instead of this one:
```py
from sqlalchemy import desc
desc_movies_by_rating = db.session.query(Movies).order_by(desc(Movies.rating))
```
For more details you can check SQLALchemy documentation [HERE](https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.desc)
So What I'm aiming to achieve here is to show movies from lower rating to higher and the lower rating will hold the higher ranking I know it's not logic as the lower rating movie must have the lower ranking also but when I tried it I like how the movie displayed so I keep it like this and it is up to you how you want to change it as you like.

lets explain the rest of the block of code, Well I created `all_movies empty list` and because `movies_order_by_rating` is a custom generator belong to ALChemy we need to unpack the saved instances by using list comprehension and use `len` function to get the length of the Movies array `movies_length = len([m for m in movies_order_by_rating])`

Then I created a count down list to use it as ranks `rank = [num for num in range(movies_length, 0, -1)]` So if the length of Movies are 3 so I will get inside the rank list `[3,2,1]`.

And Finally we are going to loop throw the Movies Model and update our ranking Column and commit it to our database and appended to our `all_movies` empty list then when it ready we can send our list as argument by `movies` parameter from `render_template` method.

So Now we can move to our home page to arrange it for displaying the movies data so the part of html that we are going to use jinja2 Templating engin, will be like this:
```html
{% for movie in movies %}
  <div class="card" >
    <div class="front" style="background-image: url({{ movie.image_url }});">
        <p class="large">{{ movie.ranking }}</p>
    </div>
    <div class="back">
      <div>
    <div class="title"> {{ movie.title }} <span class="release_date">({{ movie.year }})</span></div>
        <div class="rating">
            <label>{{ movie.rating }}</label>
          <i class="fas fa-star star"></i>
        </div>
          <p class="review">"{{ movie.review }}"</p>
        <p class="overview">
            {{ movie.description }}
        </p>
          <p class="type">{{ movie.type }}</p>
{% endfor %}
```
For more details you can check Jinja2 Documentation [HERE](https://jinja.palletsprojects.com/en/3.1.x/).
![bandicam 2022-03-30 14-33-13-289](https://user-images.githubusercontent.com/57592040/160825323-9c137e80-f7e3-4572-bd0b-6f8564736fa9.jpg)

Great Job so far lets now add our add function with select to feed our database data from Movie Database API and this what will discuse next.

## STEP 4 - Search , SELECT, ADD

I can see it is the most important step because here you need to get your movie data and save it to your database then display it as well, to do so we need to activate the add button that will take us to our add page where we will use our MovieTitle form we created later.

The MovieTitle FlaskForm:
```py
class MoveTitle(FlaskForm):
    movie_title = StringField("Movie Title", validators=[DataRequired(), Length(min=2, max=250)])
    submit = SubmitField("Done")
```
Then we will create our add route method that will allowed for GET and POST Methods
```py
@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    form = MoveTitle()
    if request.method == "POST":
        if form.validate_on_submit():
            return redirect(url_for('select_movie', movie_title=form.data.get('movie_title')))
    return render_template("add.html", form=form)
```
As we can see When the user submit the form to our server we will check if the form data is validate and it will redirect us to the select route function where we will request the Movie data by seaching with the movie name throw THEMOVIE DATABASE SERVER by Thier end point API.
So our select route function will look like this:
```py
@app.route('/select_movie/<movie_title>)', methods=["GET", "POST"])
def select_movie(movie_title):
    search = tmdb.Search()
    search.movie(query=movie_title)
    return render_template('select.html', all_movies=search.results)
```
Here we created an instance from tmdb the tmdbsimple wrapper and we will use search class to search by the movie name that we got from the add route function.
Then we will render the `select.html` with a parameter that hold the all results founds.
Now we need to display all results in our select page and to do so we can check the code below:
```html
{% for movie in all_movies %}
  <p>
    <a href="{{ url_for('add_movie_to_db', movie_id=movie['id']) }}"> MOVIE TITLE: {{ movie['title'] }} - MOVIE RELEASE DATE: {{movie['release_date'][:4] }}</a>
  </p>
{% endfor %}
```
and it will look like this 
![bandicam 2022-03-30 17-58-10-682](https://user-images.githubusercontent.com/57592040/160865812-84ba1963-1515-4145-9fcd-e2600c54c08b.jpg)

As we see when the user click on any link that will add the movie data to our database and here we just pass the movie id as argument to `movie_id` parameter.
And our `add_movie_to_db` will look like this 
```py
@app.route('/add_to_db/<movie_id>', methods=["GET", "POST"])
def add_movie_to_db(movie_id):
    movie = tmdb.Movies(movie_id).info()
    movie_title = movie.get('title')
    movie_genre = movie.get('genres')[0].get('name')
    year = int(movie.get('release_date')[:4])
    description = movie.get('overview')
    rating = movie.get('vote_average')
    image_url = movie.get('poster_path')
    movie = Movies(title=movie_title,
                   type=movie_genre,
                   year=year,
                   description=description,
                   rating=rating,
                   image_url=IMAGE_MOVIEDB_URL + image_url)
    db.session.add(movie)
    db.session.commit()

    return redirect(url_for('home'))
```
After doing some experiments I did find all movie data I need to feed my database and I created a movie instance from the Movies Model class and I add it to the database and commit the changes as well.
And when All done it will redirect us to the home page where all Movies will load and display as well.
![bandicam 2022-03-30 18-18-00-192](https://user-images.githubusercontent.com/57592040/160870637-ad40b39d-3423-421d-be79-da83cbe40f23.jpg)

Greate job so far after that we need to update our review and delete Movie Options and that will do next Step.

## STEP 5 - Update Review and Delete Movie
What if I want to update my review as by default review Column have a ready review so if I want to update it I could do so by creating a form to allow user to type a new review then update it to our database.

So lets create our EditReview FlaskForm and it will be like this :
```py
class EditReview(FlaskForm):
    review = StringField("Review", validators=[DataRequired(), Length(min=10, max=250)])
    submit = SubmitField("Done")
```
After that we need to create our update review route function and it will look like this:
```py
@app.route("/update_review/<movie_id>", methods=["GET", "POST"])
def update_review(movie_id):
    form = EditReview()
    if request.method == "POST":
        if form.validate_on_submit():
            movie = db.session.query(Movies).filter_by(id=movie_id).first()
            movie.review = form.data.get("review")
            db.session.commit()
            return redirect(url_for('home'))

    movie_data = db.session.query(Movies).filter_by(id=movie_id).first()
    return render_template('edit.html', movie=movie_data, form=form)
```
Again we did the same steps with add route function but here we got the user review and update our review cell with the new data and commit it as well then again redirect the user to home page.

### Delete Movie
To delete movie we will create a Delete button the link to `del_movie` route function that will allow us to delete the selected movie as well the code will look like this:
```py
@app.route("/delete_movie/<movie_id>")
def del_movie(movie_id):
    movie = db.session.query(Movies).filter_by(id=movie_id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))
```

As we see here that we located the movie throw its `movie_id` and then deleted it and save changes by commited it, finally again will redirect us to the home page.

## OVERVIEW

The project didn't discuss handling error or how we could build flipcard with Css but it focused on dealing with How to connect our Flask Web Application with MovieDB API and use that data to feed our database.

I figured out that I really need to learn about web development more to solve some issues that can't solve it with bootstrap-flask only.
I wish this mini documentation help you to understand more this challenge and how to come over it an solve it as well.
Goodluck for everyone.

