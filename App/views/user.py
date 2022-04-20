from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session
)
from flask_login import login_required

from App.controllers import (
    SignUp,
    LogIn,
    PostSpotting,
    SearchMap,
    create_user,
    authenticate,
    login_user,
    logout_user,
    get_spottings_by_user,
    get_spottings_by_bird,
    get_all_spottings_json,
    create_spotting,
    get_user_location,
)

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
    data = request.form
    flash(data)
    return redirect(url_for("user_views.signup_action"))


# if request to /login is a GET, return login.html
@user_views.route("/", methods=["GET"])
def index():
    form = LogIn()
    return render_template("login.html", form=form)


# if request to /login is a POST, then get form info, validate, login and redirects to user_views.spottings_page
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
            return redirect(url_for("user_views.spottings_page"))
        flash("Invalid Credentials")
        return redirect(url_for("user_views.index"))
    flash("Invalid Credentials")
    return redirect(url_for("user_views.index"))


@user_views.route("/logout")
def logout_action():
    logout_user()
    return redirect(url_for("user_views.index"))


# user must be logged in to view account spottings
@user_views.route("/spottings", methods=["GET"])
@login_required
def spottings_page():
    user_coords = get_user_location(session['user_id'])
    spottings = get_spottings_by_user(session['user_id'])
    markers = [{
        'lat': spotting['lat'],
        'lng': spotting['long'],
        'infobox': f"{spotting['bird_name']} spotted at {spotting['time']}. Details: {spotting['details']}"
    } for spotting in spottings]
    
    return render_template("spottings.html", spottings=spottings, markers=markers, user_coords=user_coords)


@user_views.route('/map', methods=['GET'])
@login_required
def map_page():
    form = SearchMap()
    spottings = get_all_spottings_json()
    user_coords = get_user_location(session['user_id'])
    markers = [{
        'lat': spotting['lat'],
        'lng': spotting['long'],
        'infobox': f"{spotting['bird_name']} spotted at {spotting['time']}. Details: {spotting['details']}"
    } for spotting in spottings]
    return render_template('map.html', markers=markers, user_coords=user_coords, form=form)


@user_views.route('/map', methods=['POST'])
@login_required
def search_map_page():
    form = SearchMap()
    if form.validate_on_submit():
        data = request.form
        bird_name = data['bird_name']
        spottings = get_spottings_by_bird(bird_name)
        user_coords = get_user_location(session['user_id'])
        markers = [{
            'lat': spotting['lat'],
            'lng': spotting['long'],
            'infobox': f"{spotting['bird_name']} spotted at {spotting['time']}. Details: {spotting['details']}"
        } for spotting in spottings if spotting['bird_name'] == bird_name]
        return render_template('map.html', markers=markers, user_coords=user_coords, form=form)


@user_views.route('/post-spotting', methods=['GET'])
@login_required
def post_spotting_page():
    form = PostSpotting()
    user_coords = get_user_location(session['user_id'])
    return render_template('post-spotting.html', user_coords=user_coords, form=form)


@user_views.route('/post-spotting', methods=['POST'])
@login_required
def post_spotting_action():
    form = PostSpotting()
    location = get_user_location(session['user_id'])
    if form.validate_on_submit():
        data = request.form
        create_spotting(
            session['user_id'],
            data['bird_name'],
            location[0],
            location[1],
            data['details']
        )
        return redirect(url_for('user_views.spottings_page'))
