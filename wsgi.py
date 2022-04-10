import click
from flask import Flask
from flask.cli import with_appcontext

from App.database import create_db
from App.main import app, migrate
from App.controllers import (
    create_user,
    get_all_users_json,
    create_spotting,
    get_all_spottings_json,
    get_user_spottings
)


@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

@app.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@app.cli.command("get-users")
def get_users():
    print(get_all_users_json())

@app.cli.command("create-spotting")
@click.argument("user_id")
@click.argument("bird_name")
@click.argument("lat")
@click.argument("long")
@click.argument("details")
def create_spotting_command(user_id, bird_name, lat, long, details):
    create_spotting(user_id, bird_name, lat, long, details)
    print(f"{bird_name} at {lat},{long} spotted")

@app.cli.command("get-spottings")
def get_spottings():
    print(get_all_spottings_json())

@app.cli.command("get-user-spottings")
@click.argument("user_id")
def get_user_spottings_command(user_id):
    print(get_user_spottings(user_id))