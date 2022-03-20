import click
from flask import Flask
from flask.cli import with_appcontext

from App import create_db, db, User, app, migrate


@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

@app.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    print(f'{username} created!')

@app.cli.command("get-users")
def get_users():
    users = User.query.all()
    if not users:
        return []
    users = [user.toDict() for user in users]
    print(users)