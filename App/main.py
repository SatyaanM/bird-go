import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads

from App.controllers import setup_jwt, load_user_from_id
from App.database import init_db, get_migrate
from App.views import user_views, api_views

views = [user_views, api_views]


def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config["ENV"] = os.environ.get("ENV", "DEVELOPMENT")
    if app.config["ENV"] == "DEVELOPMENT":
        app.config.from_object("App.config")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["JWT_EXPIRATION_DELTA"] = timedelta(
            days=int(os.environ.get("JWT_EXPIRATION_DELTA"))
        )
        app.config["DEBUG"] = os.environ.get("ENV").upper() != "PRODUCTION"
        app.config["ENV"] = os.environ.get("ENV")
        app.config["GOOGLEMAPS_KEY"] = os.environ.get("GOOGLEMAPS_KEY")
        app.config['SESSION_COOKIE_SECURE'] = True
    for key, value in config.items():
        app.config[key] = config[key]


def create_app(config={}):
    app = Flask(__name__, static_url_path="/static")
    CORS(app)
    loadConfig(app, config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["UPLOADED_PHOTOS_DEST"] = "App/uploads"
    photos = UploadSet("photos", TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    init_db(app)
    setup_jwt(app)
    app.app_context().push()
    return app


app = create_app()
login_manager = LoginManager(app)
GoogleMaps(app)


@login_manager.user_loader
def load_user(user_id):
    return load_user_from_id(user_id)


migrate = get_migrate(app)

