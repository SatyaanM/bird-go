from App.models import User
from App.database import db
import json


# returns a list of all users
def get_all_users():
    return User.query.all()


# creates a new User object and stores it in the database
def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()


def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toDict() for user in users]
    return json.dumps(users)
