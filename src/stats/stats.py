from flask import Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from models import WorkoutSessions, Schedules
from db import db

stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")


@stats.route("/", methods=['GET', 'POST'])
@login_required
def overview():
    #  For now this code deals with switching the schedules
    if 'active_schedule_id' in session:
        session['active_schedule_id'] = request.args.get('scheduleSelector')
    else:
        session['active_schedule_id'] = 1
    #  This must be here, because the page refreshes twice - it sets id to 1 and then to None - scheduleSelector is none
    if session['active_schedule_id'] is None:
        session['active_schedule_id'] = 1

    active_schedule_id = int(session['active_schedule_id'])

    all_workout_sessions = WorkoutSessions.query.filter_by(user_id=current_user.id).all()
    num_of_workout_sessions = WorkoutSessions.query.filter_by(
        user_id=current_user.id,
        schedule_id=active_schedule_id
    ).count()

    all_schedules = Schedules.query.all()
    # Create basic schedules in case the database was deleted in development process
    if not all_schedules:
        schedule1 = Schedules(
            name="Lane Goodwin Full"
        )
        schedule2 = Schedules(
            name="Lane Goodwin Best Of"
        )
        schedule3 = Schedules(
            name="Bla Bla"
        )
        db.session.add(schedule1)
        db.session.add(schedule2)
        db.session.add(schedule3)
        db.session.commit()

    if request.method == "POST":
        date = request.form.get('calendar')
        hours = request.form.get('hours')
        minutes = request.form.get('minutes')
        seconds = request.form.get('seconds')

        if not date or not hours or not minutes or not seconds:
            flash(f'Please fill in all inputs{date, hours, minutes, seconds}', category='error')
        else:
            workout_session = WorkoutSessions(
                date=date,
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                user_id=current_user.id,
                season=1,
                schedule_id=active_schedule_id,
                position_in_schedule=1
            )
            db.session.add(workout_session)
            db.session.commit()
            flash('Workout record added!', category='success')

    return render_template("overview.html",
                           user=current_user,
                           all_workout_sessions=all_workout_sessions,
                           num_of_workout_sessions=num_of_workout_sessions,
                           all_schedules=all_schedules,
                           active_schedule_id=active_schedule_id
                           )
