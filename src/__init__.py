from flask_login import LoginManager
from flask import Flask, redirect, url_for
from os import path
from redmail import gmail

from auth.auth import auth
from stats.stats import stats
from db import db, DB_NAME
from config import SECRET_KEY, MAIL_USERNAME, MAIL_PASSWORD, SQLALCHEMY_DATABASE_URI
from socket import gethostname

from models import User


def create_database(app):
    if not path.exists("instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database")


# Change this on production

app = Flask(__name__)

app.secret_key = SECRET_KEY
app.config['DEBUG'] = True
app.config['TESTING'] = False

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

gmail.username = MAIL_USERNAME
gmail.password = MAIL_PASSWORD

db.init_app(app)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(stats, url_prefix="/stats")

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

create_database(app=app)


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, id)


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


if __name__ == '__main__':
    db.create_all()
    if 'liveconsole' not in gethostname():
        app.run()
