import bcrypt

from model import User


from model import connect_to_db, db
from server import app

def sample_user():
    """ Add sample user to DB """
    password = "123"
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users = [
        User(first_name="Kim", last_name="Jones", email="kim@example.com", password=hashed_pw),
    ]

    for user in users:
        db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    sample_user()

