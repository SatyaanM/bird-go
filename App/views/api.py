import json

from flask import Blueprint, request, session

from App.controllers import set_user_location

api_views = Blueprint("api_views", __name__, template_folder="../templates")


@api_views.route('/user-location', methods=['POST'])
def set_user_location_route():
    data = request.get_json()
    set_user_location(session['user_id'], data['lat'], data['long'])
    return json.dumps({"location": f"({data['lat']}, {data['long']})"}), 200


@api_views.route('/birds', methods=['GET'])
def get_birds():
    f = open('bird_species.json', 'r')
    data = json.load(f)
    f.close()
    return data
