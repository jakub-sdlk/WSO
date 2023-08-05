from flask import Blueprint
from flask_login import login_required

stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")

@stats.route("/")
@login_required
def overview():
    return "Your stats overview"