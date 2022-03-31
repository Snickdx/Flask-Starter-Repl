import os
from flask import Flask, redirect, render_template, jsonify, request, send_from_directory, flash
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from App.models import db, get_migrate, create_db

def create_app():
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'MySecretKey'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    create_db(app)
    app.app_context().push()
    return app

app = create_app()

migrate = get_migrate(app)


@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


@app.route('/static/home', methods=['GET'])
def home2():
  return send_from_directory('static', 'index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)