from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    spottings = db.relationship(
        "Spotting", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.active = True

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "num_spottings": self.get_num_spottings(),
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_num_spottings(self):
        return len(self.spottings)

    def set_location(self, lat, long):
        self.latitude = lat
        self.longitude = long
