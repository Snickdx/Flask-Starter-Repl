[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flask-starter)

# Flask Starter Template
A template for simple flask projects. For production projects with testing and deployment it is recommended to use [flaskmvc](https://gitpod.io/#https://github.com/uwidcit/flaskmvc).


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```
$ pip install -r requirements.txt
```

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```
# inside wsgi.py

@app.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    print(f'{username} created!')
```

Then execute the command invoking with flask cli with command name and the relevant parameters

```
$ flask create-user bob bobpass
```


# Running the Project

_For development run the serve command (what you execute):_
```
$ flask run
```

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must aslo be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```