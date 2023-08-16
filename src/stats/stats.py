from flask import Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from sqlalchemy.sql import func
from models import WorkoutSessions, Schedules, Workouts, Positions
from db import db
from datetime import time

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

    # Create basic schedules in case the database was deleted in development process
    all_schedules = Schedules.query.all()

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

    # Create basic workouts in case the database was deleted in development process

    all_workouts = Workouts.query.all()

    if not all_workouts:
        workout1 = Workouts(
            name="Core Strength", number_of_circles=5
        )
        workout2 = Workouts(
            name="Full Fledged Strength", number_of_circles=5
        )
        workout3 = Workouts(
            name="Leg Strength", number_of_circles=5
        )
        db.session.add(workout1)
        db.session.add(workout2)
        db.session.add(workout3)
        db.session.commit()

    # Create basic positions table in case the database was deleted in development process

    all_positions = Positions.query.all()

    if not all_positions:
        position101 = Positions(
            id=101, workout_id=1
        )
        position102 = Positions(
            id=102, workout_id=3
        )
        position103 = Positions(
            id=103, workout_id=1
        )
        position104 = Positions(
            id=104, workout_id=2
        )

        db.session.add(position101)
        db.session.add(position102)
        db.session.add(position103)
        db.session.add(position104)
        db.session.commit()

    all_workout_sessions = WorkoutSessions.query.filter_by(
        user_id=current_user.id, schedule_id=active_schedule_id
    ).all()

    user_workout_sessions_count = len(all_workout_sessions)

    # calculate position_id

    if user_workout_sessions_count == 0:
        position_id = (active_schedule_id * 100) + 1
    else:
        last_workout_session_position_id = int(all_workout_sessions[-1].position_id)
        position_id = (active_schedule_id * 100) + (last_workout_session_position_id % 100) + 1

    # calculate next_workout_id and best time that the workout was ever achieved

    next_workout = Positions.query.filter_by(id=position_id).first()

    if next_workout:
        next_workout_best_time_session = WorkoutSessions.query.filter_by(
            workout_id=next_workout.workout_id,
            user_id=current_user.id
        ).order_by(
            WorkoutSessions.hours,
            WorkoutSessions.minutes,
            WorkoutSessions.seconds
        ).first()
    else:
        next_workout_best_time_session = None

    # calculate current workout session season

    if user_workout_sessions_count == 0:
        current_workout_session_season = 1
    else:
        current_workout_session_season = all_workout_sessions[-1].season

    if request.method == "POST":
        date = request.form.get('calendar')
        hours = request.form.get('hours')
        minutes = request.form.get('minutes')
        seconds = request.form.get('seconds')
        new_season = request.form.get('season_setup')

        if int(new_season):  # new_season returns 0 | 1 as a string
            current_workout_session_season += 1
            position_id = (active_schedule_id * 100) + 1
            next_workout = Positions.query.filter_by(id=position_id).first()

        if not date or not hours or not minutes or not seconds:
            flash(f'Please fill in all inputs{date, hours, minutes, seconds}', category='error')
        elif not next_workout:
            flash(
                f'No more workouts in current schedule. Start a new season or choose another schedule',
                category='error'
            )
        else:
            workout_session = WorkoutSessions(
                date=date,
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                season=current_workout_session_season,

                user_id=current_user.id,
                workout_id=next_workout.workout_id,
                position_id=position_id,
                schedule_id=active_schedule_id
            )
            db.session.add(workout_session)
            db.session.commit()
            flash('Workout record added!', category='success')

    return render_template("overview.html",
                           user=current_user,
                           all_schedules=all_schedules,
                           active_schedule_id=active_schedule_id,
                           all_workout_sessions=all_workout_sessions,
                           user_workout_sessions_count=user_workout_sessions_count,
                           time=time,
                           next_workout=next_workout,
                           next_workout_best_time_session=next_workout_best_time_session,
                           current_workout_session_season=current_workout_session_season
                           )
