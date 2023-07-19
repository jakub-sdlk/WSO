from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask, redirect, url_for
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.secret_key = "WSO"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from auth.auth import auth
    from stats.stats import stats

    from models import User

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(stats, url_prefix="/stats")

    create_database(app)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app


def create_database(app):
    if not path.exists(f"scr/{DB_NAME}"):
        db.create_all(app=app)
        print("Created database")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)