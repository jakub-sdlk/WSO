from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")

@stats.route("/", methods=['GET', 'POST'])
@login_required
def overview():
    return render_template("overview.html", user=current_user)

def add_workout_record():
    if request.method == "POST":
        date = request.form.get('calendar')
        hours = request.form.get('hours')
        minutes = request.form.get('minutes')
        seconds = request.form.get('seconds')

        if not date or hours or minutes or seconds:
            flash('Please fill in all inputs', category='error')
        else:
            flash('Workout record added!', category='success')