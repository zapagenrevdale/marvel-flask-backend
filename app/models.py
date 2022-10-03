from app import db, ma

class StreamSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    link = db.Column(db.String(255))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))

class StreamSiteSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "link")

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255))
    value = db.Column(db.String(255))
    imdb_id = db.Column(db.Integer, db.ForeignKey("imdb.id"))


class RatingSchema(ma.Schema):
    class Meta:
        fields = ("id", "source", "value", "imdb_id")


class Imdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    rated = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    director = db.Column(db.String(255))
    actors = db.Column(db.String(255))
    plot = db.Column(db.Text)
    language = db.Column(db.String(255))
    awards = db.Column(db.String(255))
    metascore = db.Column(db.Integer)
    rating = db.Column(db.Float(1))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    ratings = db.relationship("Rating", backref="imdb", lazy="dynamic")



class ImdbSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
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
            "ratings",
        )

    ratings = ma.Nested(RatingSchema(), many=True)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    overview = db.Column(db.Text)
    cover_url = db.Column(db.String(255), nullable=False)
    background_url = db.Column(db.String(255))
    trailer_url = db.Column(db.String(255))
    saga = db.Column(db.String(255))
    chronology = db.Column(db.Integer)
    post_credit_scenes = db.Column(db.Integer)
    phase = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    box_office = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    stream_sites = db.relationship("StreamSite", backref="movie", lazy="subquery")
    imdb = db.relationship("Imdb", backref="movie", lazy="subquery", uselist=False)



class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        
    imdb = ma.Nested(ImdbSchema())
    stream_sites = ma.Nested(StreamSiteSchema(), many=True)

