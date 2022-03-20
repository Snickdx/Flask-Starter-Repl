import os
from flask import Flask, redirect, render_template, jsonify, request, send_from_directory, flash
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from flask_jwt import JWT
from sqlalchemy.exc import OperationalError
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta

from App.models import db, init_db, get_migrate, create_db, User, Upload

def create_app():
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'MySecretKey'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    app.config['UPLOAD_FOLDER'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    create_db(app)
    configure_uploads(app, photos)
    app.app_context().push()
    return app

app = create_app()

migrate = get_migrate(app)

'''
JWT Setup

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user

# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload['identity'])

JWT(app, authenticate, identity)
'''

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<path:name>', methods=["GET"])
def download_file(name):
  return send_from_directory('uploads', name)

@app.route('/', methods=['GET'])
def get_api_docs():
  return render_template('index.html')

@app.route('/uploader', methods=['GET'])
def uploader():
  uploads = Upload.query.all()
  return render_template('uploads.html', uploads=uploads)



@app.route('/upload', methods=['POST'])
def upload_action():
  if 'file' not in request.files:
    flash('No file in request')
    return redirect('/uploader')
  file = request.files['file']
  if allowed_file(file.filename):
    flash('Invlid file format uploaded')
    return redirect('/uploader')
  newupload = Upload(file)
  db.session.add(newupload)
  db.session.commit()
  flash('file uploaded!')
  return redirect('/uploader')

@app.route('/users', methods=['GET'])
def get_user_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')


@app.route('/deleteUpload/<int:id>', methods=['GET'])
def delete_file(id):
  upload = Upload.query.get(id)
  if upload:
    upload.remove_file()
    db.session.delete(upload)
    db.session.commit()
    flash('Upload Deleted')
  return redirect('/uploader')
    

'''
API route that returns all stored users as json
'''
@app.route('/api/users', methods=['GET'])
def client_app():
    users = User.query.all()
    if not users:
        return []
    users = [user.toDict() for user in users]
    return jsonify(users)

"""
Creates a user by providing credentails in the url
"""
@app.route('/adduser/<string:username>/<string:password>', methods=['GET'])
def create_user(username, password):
    existing_user = User.query.filter_by(username=username).first()
    if(existing_user):
        flash(f'Error: cannot create {username}, user already exists')
        return redirect('/users')
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    flash(f'{username} created!');
    return redirect('/users')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)