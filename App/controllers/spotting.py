from App.models import Spotting
from App.database import db
import json

# returns a list of all spottings
def get_all_spottings():
    return Spotting.query.all()


# creates a new Spotting object and stores it in databse
def create_spotting(user_id, bird_name, lat, long, details):
    newSpotting = Spotting(
        user_id=user_id, bird_name=bird_name, lat=lat, long=long, details=details
    )
    newSpotting.set_time()
    db.session.add(newSpotting)
    db.session.commit()


def get_all_spottings_json():
    spottings = Spotting.query.all()
    if not spottings:
        return []
    spottings = [spotting.toDict() for spotting in spottings]
    return spottings


def get_user_spottings(user_id):
    spottings = Spotting.query.filter_by(user_id=user_id).all()
    spottings = [spotting.toDict() for spotting in spottings]
    return json.dumps(spottings)
