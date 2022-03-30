from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import tmdbsimple as tmdb
import os
import requests

# Some notes if you want to use Select field to add Movie genres
'''
# All Movies Genre 
movies_genre = 
Action Genre
Animation Genre
Comedy Genre
Crime Genre
Drama Genre
Experimental Genre
Fantasy Genre
Historical Genre
Horror Genre
Romance Genre
Science Fiction Genre
Thriller Genre
Western Genre
Other Genres

all_movies_genre = movies_genre.split("\n")[1:-1]
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# you need to create your own account on https://www.themoviedb.org/
tmdb.API_KEY = os.getenv("MOVIEDBAPI")
tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.REQUESTS_SESSION = requests.Session()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my-top-movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap5(app)
# We will use the link to join poster_path to provide the movie cover later
IMAGE_MOVIEDB_URL = "https://image.tmdb.org/t/p/w500"


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

    def __repr__(self):
        return f"Movie(ID : {self.id}, Title: {self.title}," \
               f"Year: {self.year}, Rating:{self.rating}," \
               f"Ranking: {self.ranking}, Movie Genre: {self.type})"


# You Can use this form if you want to add movies data manually.
'''
# Add Movie Form
class AddMovie(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(), Length(min=2, max=100)])
    year = IntegerField("Year Of Release", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    rating = FloatField("Rating", validators=[DataRequired()])
    ranking = IntegerField("Ranking")
    review = StringField("Review", validators=[Length(min=10, max=250)])
    image_url = URLField("Image link")
    submit = SubmitField("Submit Movie")
'''


class EditReview(FlaskForm):
    review = StringField("Review", validators=[DataRequired(), Length(min=10, max=250)])
    submit = SubmitField("Done")


class MoveTitle(FlaskForm):
    movie_title = StringField("Movie Title", validators=[DataRequired(), Length(min=2, max=250)])
    submit = SubmitField("Done")


# Example of Movie Data
'''
movie = Movies(title="Drive", type="Action Genre", year=2011, 
description="A mysterious Hollywood stuntman and mechanic moonligh
ts as a getaway driver and finds himself in trouble when he helps 
out his neighbor in this action drama.",rating=8.5, ranking=10,rev
iew="I Loved it!!!",image_url="https://www.cityonfire.com/wp-conte
nt/uploads/2012/02/drive-movie-poster-2011-1020745540.jpg")
'''


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


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    form = MoveTitle()
    if request.method == "POST":
        if form.validate_on_submit():
            return redirect(url_for('select_movie', movie_title=form.data.get('movie_title')))
    return render_template("add.html", form=form)


@app.route("/delete_movie/<movie_id>")
def del_movie(movie_id):
    movie = db.session.query(Movies).filter_by(id=movie_id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def update_movie(movie_id):
    form = EditReview()
    if request.method == "POST":
        if form.validate_on_submit():
            movie = db.session.query(Movies).filter_by(id=movie_id).first()
            movie.review = form.data.get("review")
            db.session.commit()
            return redirect(url_for('home'))

    movie_data = db.session.query(Movies).filter_by(id=movie_id).first()
    return render_template('edit.html', movie=movie_data, form=form)


@app.route('/select_movie/<movie_title>)', methods=["GET", "POST"])
def select_movie(movie_title):
    search = tmdb.Search()
    search.movie(query=movie_title)
    return render_template('select.html', all_movies=search.results)


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


# The keys that I'm going to use these keys.
'''
keys = [(title_key, 'title'),(type_key, 'genres'[0].get('name'),(year,int('release_date')[:4]),
(description,'overview'), (rating, 'vote_average'), (image_url, IMAGE_MOVIEDB_URL+'poster_path'))
get movie data
first we need to search about the movie by it is name
search = tmdb.Search()
response = search.movie(query='The Bourne')
movie_id = response['results'][0]['id']
r = tmdb.Movies(movie_id).info()
movie_title = r.get('title')
movie_genre = r.get('genres')[0].get('name')
year = int(r.get('release_date')[:4])
description = r.get('overview')
rating = r.get('vote_average')
image_url = r.get('poster_path')
'''

if __name__ == '__main__':
    app.run(debug=True)
