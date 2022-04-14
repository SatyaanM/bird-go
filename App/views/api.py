from flask import Blueprint
import json

from App.controllers import get_all_spottings_json, get_spottings_by_user, get_spottings_by_bird

api_views = Blueprint("api_views", __name__, template_folder="../templates")


@api_views.route('/spottings', methods=['GET'])
def get_all_spottings():
    return json.dumps(get_all_spottings_json())


@api_views.route('/spottings/u/<user_id>', methods=['GET'])
def get_user_spottings(user_id):
    return json.dumps(get_spottings_by_user(user_id=user_id))


@api_views.route('/spottings/b/<bird_name>', methods=['GET'])
def get_bird_spottings(bird_name):
    return json.dumps(get_spottings_by_bird(bird_name=bird_name))

