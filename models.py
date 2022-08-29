from datetime import datetime
from tkinter import CASCADE

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import ARRAY

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        # unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png"
    )

    header_image_url = db.Column(
        db.Text,
        default="static/images/warbler-hero.jpg"
    )

    location = db.Column(
        db.Text,
        nullable=True
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )


    @classmethod
    def signup(cls, username, email, password, image_url, location):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
            location=location
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)



class choices(db.Model):

    __tablename__ = 'user_crime'


    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )
    incident_id = db.Column(
        ARRAY(db.Text), nullable=False) 
    # neigborhood_name = db.Column(
    #     db.Text,
    #     nullable=True,
    # )
    # from_time = db.Column(
    #     db.DateTime,
    #     nullable=True,
    # )
    # to_time = db.Column(
    #     db.DateTime,
    #     nullable=True,
    # )
    # from_date = db.Column(
    #     db.Date,
    #     nullable=True,
    # )
    # to_date = db.Column(
    #     db.Date,
    #     nullable=True,
    # )
    # supervisor_district = db.Column(
    # db.Text,
    # nullable=True,
    # )

    # police_district = db.Column(
    # db.Text,
    # nullable=True,
    # )






    