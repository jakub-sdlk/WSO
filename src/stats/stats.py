from flask import Blueprint
from flask_login import login_required, current_user

stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")

@stats.route("/")
@login_required
def overview():
    return f"<h1> Welcome, {current_user.first_name}! </h1> <p> Your stats:</p>"