from flask import Flask, redirect, url_for

from auth.auth import auth
from stats.stats import stats


def create_app():
    app = Flask(__name__)
    app.secret_key = "WSO"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(stats, url_prefix="/stats")

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)