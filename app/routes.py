from app import app, db
from flask import request, jsonify
from app.models import Movie, Imdb
from app.models import MovieSchema, ImdbSchema
from datetime import date


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/marvel")
def get_marvel_movies():
    movies = Movie.query.all()

    return jsonify(MovieSchema().dump(movies, many=True))


@app.route("/marvel/<int:id>")
def get_marvel_movie(id):
    movie = Movie.query.get(id)
    return jsonify(Movie().dump(movie))


@app.route("/marvel/featured")
def get_featured_movie():
    movies = Movie.query.all()
    day = int(str(date.today()).split("-")[1]) % len(movies)
    return jsonify(MovieSchema().dump(movies[day]))


@app.route("/imdb/<int:id>")
def get_imdb_movie(id):
    imdb = Imdb.query.get(id)

    return jsonify(ImdbSchema().dump(imdb))
