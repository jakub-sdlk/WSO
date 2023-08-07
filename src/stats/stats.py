from flask import Blueprint, render_template
from flask_login import login_required, current_user

stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")

@stats.route("/")
@login_required
def overview():
    return render_template("overview.html")