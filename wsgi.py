import click
from flask import Flask
from App import create_db, db, app


@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')
