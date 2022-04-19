from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo


class SignUp(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
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
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("Login", render_kw={"class": "btn white-text"})


class PostSpotting(FlaskForm):
    bird_name = StringField("bird_name", validators=[InputRequired()])
    details = StringField("details", validators=[InputRequired()])
    submit = SubmitField("Post", render_kw={"class": "btn white-text"})
