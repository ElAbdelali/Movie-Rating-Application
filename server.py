"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View Homepage"""
    return render_template('homepage.html') 

@app.route('/movies')
def movies():
    """ View all movies """

    movie_list = crud.retrieve_movies()
    return render_template('all_movies.html', movies=movie_list)

@app.route('/movies/<movie_id>')
def movie_detail(movie_id):
    """ View movie details """

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)


@app.route('/users')
def users():
    """ View all users """

    user_list = crud.retrieve_users()
    return render_template('all_users.html', users=user_list)

@app.route('/users/<user_id>')
def user_detail(user_id):
    """View user details"""
    
    user = crud.get_user_by_id(user_id)
    
    return render_template('user_details.html', user=user)

                 
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
