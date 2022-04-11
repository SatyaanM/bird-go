from flask import Blueprint, redirect, render_template, request, send_from_directory
from App.controllers.forms import SignUp, LogIn

api_views = Blueprint('api_views', __name__, template_folder='../templates')

@api_views.route('/', methods=['GET'])
def login():
    form = LogIn()
    return render_template('login.html', form=form)

@api_views.route('/', methods=['POST'])
def loginAction():
    form = LogIn()
    if form.validate_on_submit(): # respond to form submission
        data = request.form
        user = User.query.filter_by(username = data['username']).first()
        if user and user.check_password(data['password']): # check credentials
            flash('Logged in successfully.') # send message to next page
            login_user(user) # login the user
            return redirect(url_for('todos')) # redirect to main page if login successful
    flash('Invalid credentials')
    return redirect(url_for('account'))

@api_views.route('/signup', methods=['GET'])
def signup():
    form = SignUp()
    return render_template('signup.html', form=form)

@api_views.route('/signup', methods=['POST'])
def signupAction():
    form = SignUp() # create form object
    if form.validate_on_submit():
        data = request.form # get data from form submission
        newuser = User(username=data['username']) # create user object
        newuser.set_password(data['password']) # set password
        db.session.add(newuser) # save new user
        db.session.commit()
        flash('Account Created!')# send message
        return redirect(url_for('login'))# redirect to login page
    flash('Error invalid input!')
    return redirect(url_for('signup')) 

@api_views.route('/account')
def account():
    return render_template('account.html')

@api_views.route('/map', methods=['GET'])
def map():
    return render_template('map.html')