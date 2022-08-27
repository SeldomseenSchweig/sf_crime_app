from crypt import methods
import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import null
from sqlalchemy.exc import IntegrityError
import requests
import json
from forms import UserAddForm, LoginForm, UserEditForm, NewHoodWatchForm
from models import db, connect_db, User
from apikey import API_TOKEN

API_BASE_URL = f'https://data.sfgov.org/resource/wg3w-h783.json?$order=incident_date DESC&$$app_token={API_TOKEN}&'


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///sf_crime'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                location=form.location.data,
                email=form.email.data,
                image_url=form.image_url.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username or Email already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/home")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f'Hello, {user.username}!', "success")
            return redirect("/home")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    do_logout()
    flash(f"Successfully logged out!", "success")
    return redirect('/home')



@app.route('/home')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 10 most recent incidents of san francisco or location if shosen
    """
    

    if g.user:

        # if g.user.location == null:
        #     resp = requests.get(f'{API_BASE_URL}')
        # else:
        resp = requests.get(f'{API_BASE_URL}analysis_neighborhood={g.user.location}')
        
        
        data  = json.loads(resp.text)
       
        messages = data[:10]
            
        return render_template('home.html', messages=messages)

    else:
        return render_template('home-anon.html')


#############################################################################################################
""" Routes For the user, profile, edit, ect"""

@app.route('/users/<int:user_id>')
def user_detail(user_id):

    if not g.user or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/home")
    


    return render_template('users/detail.html')


@app.route('/users/edit', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    form = UserEditForm(obj=g.user)
    user = User.query.get_or_404(g.user.id)
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/home")
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.image_url = form.image_url.data
        g.user.header_image_url = form.header_image_url.data
        g.user.location = form.location.data

        
        user = User.authenticate(g.user.username,
                                 form.password.data)
        if user:
            db.session.commit()
            return redirect(f'/users/{g.user.id}')
        else:
            flash('Invalid Password')
            return redirect('users/edit')
    
    user = User.query.get_or_404(g.user.id)
    return render_template('users/edit.html', user=user, form=form )



    ###########################################
    """ Handles new watches """

@app.route('/watch/new', methods=["GET", "POST"])
def add_watches():
    form = NewHoodWatchForm()

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/home")
  
    if form.validate_on_submit():
        location = form.location.data
        crime_description = form.crime_description.data

        resp = requests.get(f'{API_BASE_URL}analysis_neighborhood={location}&incident_category={crime_description}')
        
        data  = json.loads(resp.text)
        messages = data[:10]
        print(data)
    
        return render_template('watches/watch.html', messages=messages)

    print(form.errors)

    return render_template('watches/new_watch.html',form=form)


