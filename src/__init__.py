from flask_login import LoginManager
from flask import Flask, redirect, url_for
from os import path
from src.auth.auth import auth
from src.stats.stats import stats

from src.models import User, WorkoutSession

from src.db import db, DB_NAME


def create_database(app):
    if not path.exists("instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database")


app = Flask(__name__)
app.secret_key = "WSO"
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False

db.init_app(app)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(stats, url_prefix="/stats")


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, id)


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    create_database(app=app)
    app.run(debug=True)
