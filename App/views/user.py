from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session
)

from App.controllers import (
    SignUp,
    LogIn,
    create_user,
    authenticate,
    login_user,
    logout_user,
    get_spottings_by_user,
    get_all_spottings_json,
)

from flask_login import login_required

# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map

user_views = Blueprint("user_views", __name__, template_folder="../templates")


# if request to /signup is GET, renders signup.html
@user_views.route("/signup", methods=["GET"])
def signup():
    form = SignUp()  # create form object
    return render_template("signup.html", form=form)  # pass form object to template


# if request to /signup is POST, gets form data, creates user and redirects to user_views.index
# url_for() finds the url associated with a function.
# In this case, index() function returns the login page and is the '/' route
@user_views.route("/signup", methods=["POST"])
def signup_action():
    form = SignUp()
    if form.validate_on_submit():
        data = request.form
        create_user(username=data["username"], password=data["password"])
        flash("Account Created!")
        return redirect(url_for("user_views.index"))


# if request to /login is a GET, return login.html
@user_views.route("/", methods=["GET"])
def index():
    form = LogIn()
    return render_template("login.html", form=form)


# if request to /login is a POST, then get form info, validate, login and redirects to user_views.account
@user_views.route("/login", methods=["POST"])
def login_action():
    form = LogIn()
    if form.validate_on_submit():
        data = request.form
        user = authenticate(username=data["username"], password=data["password"])
        if user is not None:
            flash("Logged in successfully")
            login_user(user, False)
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for("user_views.account"))
        flash("Invalid Credentials")
        return redirect(url_for("user_views.index"))


@user_views.route("/logout")
def logout_action():
    logout_user()
    return redirect(url_for("user_views.index"))


# user must be logged in to view account
@user_views.route("/account", methods=["GET"])
@login_required
def account():
    spottings = get_spottings_by_user(session['user_id'])
    return render_template("account.html", spottings=spottings)


@user_views.route('/map', methods=['GET'])
def map_page():
    spottings = get_all_spottings_json()
    coords = [[spotting['lat'], spotting['long']] for spotting in spottings]
    # my_map = Map(
    #     identifier="view-side",
    #     lat=37.4419,
    #     lng=-122.1419,
    #     markers=[(37.4419, -122.1419)]
    # )
    return render_template('map.html', coords=coords)


