from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from models import Sessions
from db import db

stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")

@stats.route("/", methods=['GET', 'POST'])
@login_required
def overview():
    sessions = Sessions.query.all()
    num_of_sessions = Sessions.query.count()
    if request.method == "POST":
        date = request.form.get('calendar')
        hours = request.form.get('hours')
        minutes = request.form.get('minutes')
        seconds = request.form.get('seconds')

        if not date or not hours or not minutes or not seconds:
            flash(f'Please fill in all inputs{date, hours, minutes, seconds}', category='error')
        else:
            session = Sessions(
                date=date, hours=hours, minutes=minutes, seconds=seconds, user_id=current_user.id)
            db.session.add(session)
            db.session.commit()
            flash('Workout record added!', category='success')

    return render_template("overview.html", user=current_user, sessions=sessions, num_of_sessions=num_of_sessions)
