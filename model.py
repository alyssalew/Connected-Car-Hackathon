"""Models and database functions for Foraging Foodie project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions


class User(db.Model):
    """ Users of SafeGuard website. """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(75), nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} first_name={} last_name={} email={}>".format(
                                                                        self.user_id,
                                                                        self.first_name,
                                                                        self.last_name,
                                                                        self.email
                                                                        )

class SmartCarAuth(db.Model):
    """ Tokens for SmartCar Auth """

    __tablename__ = "smartcarauth"

    token_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    access_token = db.Column(db.String(40), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<SmartCarAuth token_id={} access_token={}>".format(self.token_id,
                                                                self.access_token,
                                                                )




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///safeguard'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
