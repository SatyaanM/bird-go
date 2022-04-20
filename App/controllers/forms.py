import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, EqualTo, DataRequired


class SignUp(FlaskForm):
    uname = StringField("username", validators=[InputRequired()])
    password = PasswordField(
        "New Password",
        validators=[
            InputRequired(),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password")
    submit = SubmitField(
        "Sign Up", render_kw={"class": "btn waves-effect waves-light white-text"}
    )


class LogIn(FlaskForm):
    uname = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("Login", render_kw={"class": "btn white-text"})


class PostSpotting(FlaskForm):
    f = open('bird_species.json', 'r')
    data = json.load(f)
    f.close()
    choices = [bird["English name"] for bird in data]
    bird_name = SelectField("Bird Name", choices=choices, validators=[DataRequired()])
    details = StringField("details", validators=[InputRequired()])
    submit = SubmitField("Post", render_kw={"class": "btn white-text"})


class SearchMap(FlaskForm):
    f = open('bird_species.json', 'r')
    data = json.load(f)
    f.close()
    choices = [bird["English name"] for bird in data]
    bird_name = SelectField("Bird Name", choices=choices, validators=[DataRequired()])
    submit = SubmitField("Search", render_kw={"class": "btn white-text"})