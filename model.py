"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# Replace this with your code!


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    
    ratings = db.relationship("Rating", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    

class Movie(db.Model):
    """A Movie."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates='movie')
    
    def __repr__(self):
        return f'<Movie movie_id={self.movie_id} title={self.title}>'


class Rating(db.Model):
    """A Rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    movie = db.relationship("Movie", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")

    def __repr__(self):
        return f'<Movie rating_id={self.rating_id} score={self.score}>'
    

if __name__ == "__main__":
    from server import app
    import os

    os.system("dropdb ratings --if-exists")
    os.system("createdb ratings")

    connect_to_db(app)
    
    # Make our tables)
    db.create_all()    

    user1 = User(email='test@test.com', password='test')
    user2 = User(email='test2@test2.com', password='test2')
    
    movie1 = Movie(title='title1', overview='a basic overview', release_date=datetime.now(), poster_path='/basicbath.html')
    movie2 = Movie(title='Movie2', overview='overview2', release_date=datetime.now(), poster_path='path.html')

    # movies = Movie.query.all()

    rating1 = Rating(score=1, movie=movie1, user=user1)

    db.session.add_all([user1, user2, movie1, movie2, rating1])
    db.session.commit()