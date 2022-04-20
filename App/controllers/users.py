import json

from App.database import db
from App.models import Users


# returns a list of all users
def get_all_users():
    return Users.query.all()


# creates a new User object and stores it in the database
def create_user(uname, password):
    newuser = Users(uname=uname, password=password)
    db.session.add(newuser)
    db.session.commit()


def get_all_users_json():
    users = Users.query.all()
    if not users:
        return []
    users = [user.toDict() for user in users]
    return json.dumps(users)


def set_user_location(uid, lat, long):
    user = Users.query.filter_by(id=uid).first()
    if user is None:
        return
    user.set_location(lat, long)
    db.session.add(user)
    db.session.commit()


def get_user_location(uid):
    user = Users.query.filter_by(id=uid).first()
    if user is None:
        return
    return [user.latitude, user.longitude]
