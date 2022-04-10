from App.database import db
from datetime import datetime

class Spotting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bird_name = db.Column(db.String, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    time = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=True)

    def __init(self, user_id, bird_name, lat, long, details):
        self.bird_name = bird_name
        self.lat = lat
        self.long = long
        self.details = details
        self.user_id = user_id

    def toDict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bird_name': self.bird_name,
            'latitude': self.lat,
            'longitude': self.long,
            'spotting_time': self.time,
            'spotting_details': self.details,
        }

    def set_time(self):
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")