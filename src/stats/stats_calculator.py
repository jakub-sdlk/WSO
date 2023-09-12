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
        self.next_position_id = self.calculate_next_position_id()
        self.next_position = self.get_next_position()
        self.next_workout_best_time = self.calculate_next_workout_best_time()
        self.current_workout_session_season = self.calculate_current_workout_session_season()

    def get_active_schedule_id(self):
        return int(session['active_schedule_id'])

    def get_all_workout_sessions(self):
        return WorkoutSession.query.filter_by(
            user_id=current_user.id, schedule_id=self.active_schedule_id
        ).all()

    def get_user_workout_sessions_count(self):
        return len(self.all_workout_sessions)

    def calculate_next_position_id(self):
        if self.user_workout_sessions_count == 0:
            next_position_id = (self.active_schedule_id * 100) + 1
        else:
            last_workout_session_position_id = int(self.all_workout_sessions[-1].position_id)
            next_position_id = (self.active_schedule_id * 100) + (last_workout_session_position_id % 100) + 1

        return next_position_id

    def get_next_position(self):
        return Position.query.filter_by(id=self.next_position_id).first()

    def calculate_next_workout_best_time(self):
        if self.next_position:
            next_workout_best_time = WorkoutSession.query.filter_by(
                workout_id=self.next_position.workout_id,
                user_id=current_user.id
            ).order_by(
                WorkoutSession.hours,
                WorkoutSession.minutes,
                WorkoutSession.seconds
            ).first()
        else:
            next_workout_best_time = None

        return next_workout_best_time

    def calculate_current_workout_session_season(self):
        if self.user_workout_sessions_count == 0:
            current_workout_session_season = 1
        else:
            current_workout_session_season = self.all_workout_sessions[-1].season

        return current_workout_session_season
