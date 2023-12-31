from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user
from datetime import time, date as date_obj
import re

from package.models import WorkoutSession, Schedule
from package.stats.stats_calculator import Calculator
from package.database_generator import DatabaseGenerator
from package.db import db

stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")


@stats.route("/", methods=['GET', 'POST'])
@login_required
def overview():
    # save active_schedule_id to session variable
    session['active_schedule_id'] = request.args.get('schedule_selector')



    # create basic schedules in case the database was deleted in development process
    if not Schedule.query.all():
        DatabaseGenerator.create_automatic_testing_database()

    # Register user to the schedule - For now All users should see all schedules,
    # But later they should see only one and register more with special button
    if not current_user.registered_schedules:
        for schedule in Schedule.query.all():
            current_user.registered_schedules.append(schedule)
        db.session.commit()

       # create calculator
    calculator = Calculator()

    # check post requests
    if request.method == "POST":
        date = request.form.get('calendar')
        hours = request.form.get('hours')
        minutes = request.form.get('minutes')
        seconds = request.form.get('seconds')
        new_season = request.form.get('season_setup')

        if int(new_season):  # new_season returns 0 | 1 as a string
            calculator = Calculator(new_season_flag=True)

           # Make sure all inputs are filled in
        if not date or not hours or not minutes or not seconds:
            flash(f'Please fill in all inputs{date, hours, minutes, seconds}', category='error')
        # Make sure hours, minutes and seconds consists of digits only
        elif not re.search("\d+", hours) or not re.search("\d+", seconds) or not re.search("\d+", minutes):
            flash('Incorrect datatype of hours or minutes or seconds ', category='error')
        # Make sure hours, minutes and seconds consists do not exceed limit values
        elif int(hours) < 0 or int(hours) > 23 or int(minutes) < 0 or int(minutes) > 59 or int(seconds) < 0 or int(
                seconds) > 59:
            flash('Incorrect number of hours or minutes or seconds ', category='error')
        elif not calculator.next_position:
            flash(
                'No more workouts in current schedule. Start a new season or choose another schedule',
                category='error'
            )
        else:
            workout_session = WorkoutSession(
                date=date,
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                season=calculator.current_workout_session_season,

                user_id=current_user.id,
                workout_id=calculator.next_position.workout_id,
                position_id=calculator.next_position_id,
                schedule_id=calculator.active_schedule_id
            )
            WorkoutSession.save_to_db(workout_session)
            flash('Workout record added!', category='success')
            return redirect(url_for("stats.sent"))

    return render_template("overview.html",
                           user=current_user,
                           all_schedules=calculator.all_schedules,
                           active_schedule_id=calculator.active_schedule_id,
                           all_workout_sessions=calculator.all_workout_sessions,
                           user_workout_sessions_count=calculator.user_workout_sessions_count,
                           time=time,
                           date_obj=date_obj,
                           next_position=calculator.next_position,
                           next_workout_best_time_session=calculator.next_workout_best_time_session,
                           current_workout_session_season=calculator.current_workout_session_season,
                           sets_in_next_workout=calculator.sets_in_next_workout,
                           best_workout_times=calculator.best_workout_times,
                           next_workout_all_workout_sessions=calculator.next_workout_all_workout_sessions
                           )


@stats.route("/sent", methods=['GET', 'POST'])
def sent():
    return redirect(url_for("stats.overview", schedule_selector=session['active_schedule_id']))
