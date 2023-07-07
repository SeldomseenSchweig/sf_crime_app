from crypt import methods
from inspect import getargvalues
import os
from flask import Flask, render_template, flash, redirect, session, g, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests
import json
from forms import UserAddForm, LoginForm, UserEditForm, NewHoodWatchForm
from models import db, connect_db, User, UserIncidents
import datetime
import time
from dateutil import parser
try:
    from apikey import API_TOKEN
except:
    API_TOKEN = os.environ.get('API_TOKEN')


# API_BASE_URL = f'https://data.sfgov.org/resource/wg3w-h783.json?$order=incident_date DESC&$$app_token={API_TOKEN}&'
API_BASE_URL = f'https://data.sfgov.org/resource/wg3w-h783.json?$order=incident_date DESC'


CURR_USER_KEY = "curr_user"
app = Flask(__name__)
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///sf_crime')

if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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

@app.route('/')
def home():
    return redirect('/home')

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
        if g.user.location != "All":
            resp = requests.get(f'{API_BASE_URL}analysis_neighborhood={g.user.location}')
        else:
            resp = requests.get(f'{API_BASE_URL}')

        if resp.status_code == 200:
            data = json.loads(resp.text)
            messages = data[:10]
            converted_messages = convert(messages)
            processed_messages = intersection(converted_messages)
            return render_template('home.html', messages=processed_messages)
        else:
            
            return render_template('home-anon.html')
    else:
        return render_template('home-anon.html')

def convert(messages):
    for m in messages:
        m['incident_datetime'] = format_incident_datetime(m['incident_datetime'])
    return messages

def format_incident_datetime(datetime_str):
    DT = parser.parse(datetime_str)
    return DT.strftime("%d-%b-%Y %I.%M %p")

def intersection(messages):
    for m in messages:
        if 'intersection' in m:
            m['intersection'] = m['intersection'].lower().title().replace("\\", "and")
    return messages


#############################################################################################################
""" Routes For the user, profile, edit, ect"""

@app.route('/users/<int:user_id>')
def user_detail(user_id):

    if not g.user or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/home")
    watches = g.user.watches
    


    return render_template('users/detail.html', watches = watches)


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

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")



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
        d = form.date.data
        d.strftime
        date = d.strftime("%Y-%m-%d")
        if crime_description == 'All' and location == 'All' :
            resp = requests.get(f'{API_BASE_URL}incident_date={date}')
            print(f'{API_BASE_URL}incident_date={date}')
        elif location == 'All':
            resp = requests.get(f'{API_BASE_URL}incident_date={date}&incident_category={crime_description}')
        elif crime_description == 'All':
            resp = requests.get(f'{API_BASE_URL}incident_date={date}T00:00:00.000&analysis_neighborhood={location}')
        else:
            resp = requests.get(f'{API_BASE_URL}incident_date={date}T00:00:00.000&analysis_neighborhood={location}&incident_category={crime_description}')

        data  = json.loads(resp.text)
        if len(data) == 0:
            flash("Your search was empty", "error")
            return render_template('watches/new_watch.html',form=form)
        messages = data[:10]
        messages = convert(messages)
        messages = intersection(messages)
        
        return render_template('watches/watch.html', messages=messages)

    return render_template('watches/new_watch.html',form=form)

def intersection(messages):
    for m in messages:
        try:
            m['intersection']

        except:
            continue
        m['intersection'] = m['intersection'].lower()
        m['intersection'] = m['intersection'].title()
        m['intersection'] = m['intersection'].split("\\")
        m['intersection'] = 'and'.join(m['intersection'])
          
    return messages




@app.route('/users/save_search', methods=["POST"])
def save_search():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/home")
    d = request.form['messages']
    name = request.form['name']
    list = UserIncidents(user_id = g.user.id, incidents=d, name=name)
    db.session.add(list)
    db.session.commit()

    return redirect('/home')


@app.route('/saved_watch/<int:id>')
def saved_search(id):
    u = UserIncidents.query.get(id)
    if not g.user or g.user.id != u.user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/home")

    u = eval(u.incidents)
    return render_template('watches/saved_watch.html', watches=u, id=id )


@app.route('/watch/delete/<int:id>', methods=["POST"])
def delete_watch(id):
    """Delete user."""
    i = UserIncidents.query.get(id)
    if not g.user or i.user_id != g.user.id :
        flash("Access unauthorized.", "danger")
        return redirect("/")


    db.session.delete(i)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")