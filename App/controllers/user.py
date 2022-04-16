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


def set_user_location(uid, lat, long):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        return
    user.set_location(lat, long)
    db.session.add(user)
    db.session.commit()


def get_user_location(uid):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        return
    return [user.latitude, user.longitude]
