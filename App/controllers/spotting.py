from App.database import db
from App.models import Spotting


# creates a new Spotting object and stores it in database
def create_spotting(user_id, bird_name, lat, long, details):
    new_spotting = Spotting(
        user_id=user_id, bird_name=bird_name, lat=lat, long=long, details=details
    )
    new_spotting.set_time()
    db.session.add(new_spotting)
    db.session.commit()


# returns a list of all spottings
def get_all_spottings():
    return Spotting.query.all()


def get_all_spottings_json():
    spottings = Spotting.query.all()
    if not spottings:
        return []
    spottings = [spotting.toDict() for spotting in spottings]
    return spottings


def get_spottings_by_user(user_id):
    spottings = Spotting.query.filter_by(user_id=user_id).all()
    spottings = [spotting.toDict() for spotting in spottings]
    return spottings


def get_spottings_by_bird(bird_name):
    spottings = Spotting.query.filter_by(bird_name=bird_name).all()
    spottings = [spotting.toDict() for spotting in spottings]
    return spottings
