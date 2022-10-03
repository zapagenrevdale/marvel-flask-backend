from re import L
from app.models import Imdb, Movie, MovieSchema, Rating, StreamSite
import requests
from datetime import datetime
from app import app, db
import os
from util.extra_data import background_url_data, stream_sites_data

movies_url = os.environ.get("MOVIES_URL")
imdb_url = os.environ.get("IMDB_URL")
rapid_api_key = os.environ.get("RAPID_API_KEY")
rapid_api_host = os.environ.get("RAPID_API_HOST")
payload = {"X-RapidAPI-Key": rapid_api_key, "X-RapidAPI-Host": rapid_api_host}


def fetch_movies():
    response = requests.get(movies_url)
    response.raise_for_status()
    movies = response.json()
    fields = (
        "imdb_id",
        "title",
        "overview",
        "cover_url",
        "background_url",
        "trailer_url",
        "saga",
        "chronology",
        "post_credit_scenes",
        "phase",
        "release_date",
        "box_office",
        "duration",
    )
    for m in movies["data"]:

        m["release_date"] = datetime.strptime(m["release_date"], "%Y-%m-%d").date()
        m["background_url"] = background_url_data[m["imdb_id"]]
        movie = Movie(**{field: m[field] for field in fields})
        try:
            db.session.add(movie)
            db.session.commit()
            save_streaming_sites(movie, stream_sites_data[m["imdb_id"]])
        except:
            db.session.rollback()

def save_streaming_sites(movie, streaming_sites):
    for site_name, link in streaming_sites.items():
        db.session.add(StreamSite(name=site_name, link=link, movie_id=movie.id))
    db.session.commit()


def delete_movies():

    for movie in Movie.query.all():
        db.session.delete(movie)
    db.session.commit()


def delete_imdb_movies():
    for movie in Imdb.query.all():
        db.session.delete(movie)
    db.session.commit()


def delete_ratings():
    for rating in Rating.query.all():
        db.session.delete(rating)
    db.session.commit()

def delete_sites():
    for site in StreamSite.query.all():
        db.session.delete(site)
    db.session.commit()


def delete_all_movies():
    delete_movies()
    delete_imdb_movies()
    delete_ratings()
    delete_sites()



def fetch_imdb_movies():

    fields = (
        "year",
        "rated",
        "genre",
        "director",
        "actors",
        "plot",
        "language",
        "awards",
        "metascore",
        "rating",
        "movie_id",
    )
    try:
        for movie in Movie.query.all():
            imdb_id = movie.imdb_id
            response = requests.get(imdb_url + imdb_id, headers=payload)
            response.raise_for_status()
            data = response.json()
            data["Movie_Id"] = movie.id
            data["Rating"] = data["imdbRating"] if data["imdbRating"] != "N/A" else None
            data["Metascore"] = (
                data["Metascore"] if data["Metascore"] != "N/A" else None
            )

            imdb_movie = Imdb(**{field: data[field.title()] for field in fields})
            db.session.add(imdb_movie)
            db.session.commit()
            data["Imdb_Id"] = imdb_movie.id
            save_ratings(data)

    except Exception as e:
        print(e)
        db.session.rollback()


def save_ratings(data):
    fields = ("source", "value", "imdb_id")
    for rating in data["Ratings"]:
        rating["Imdb_Id"] = data["Imdb_Id"]
        rating = Rating(**{field: rating[field.title()] for field in fields})
        db.session.add(rating)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "fetch_movies": fetch_movies,
        "fetch_imdb_movies": fetch_imdb_movies,
        "delete_all_movies": delete_all_movies,
        "Movie": Movie,
        "MovieSchema": MovieSchema,
        "Imdb": Imdb,
        "Rating": Rating,
    }
