from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user
from datetime import time

from src.models import WorkoutSession, Schedule, Workout, Position
from src.db import db


class Calculator:
    def __init__(self):
        self.all_schedules = Schedule.query.all()
        self.active_schedule_id = self.get_active_schedule_id()
        self.all_workouts = Workout.query.all()
        self.all_positions = Position.query.all()
        self.all_workout_sessions = self.get_all_workout_sessions()
        self.user_workout_sessions_count = self.get_user_workout_sessions_count()
        # self.time = self.get_time()
        # self.next_workout = self.get_next_workout()
        # self.next_workout_best_time_session = self.get_next_workout_best_time_session()
        # self.current_workout_session_season = self.get_current_workout_session_season()

    def get_active_schedule_id(self):
        return int(session['active_schedule_id'])

    def get_all_workout_sessions(self):
        return WorkoutSession.query.filter_by(
            user_id=current_user.id, schedule_id=self.active_schedule_id
        ).all()

    def get_user_workout_sessions_count(self):
        return len(self.all_workout_sessions)
