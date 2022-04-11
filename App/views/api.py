from flask import Blueprint, redirect, render_template, request, send_from_directory
from App.forms import SignUp, LogIn

api_views = Blueprint('api_views', __name__, template_folder='../templates')

@api_views.route('/', methods=['GET'])
def login():
    form = LogIn()
    return render_template('login.html', form=form)

@api_views.route('/signup', methods=['GET'])
def signup():
    form = SignUp()
    return render_template('signup.html', form=form)

@api_views.route('/account')
def account():
    return render_template('account.html')

@api_views.route('/map', methods=['GET'])
def map():
    return render_template('map.html')