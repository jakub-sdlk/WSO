from flask import Blueprint

stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")

@stats.route("/")
def overview():
    return "Your stats overview"