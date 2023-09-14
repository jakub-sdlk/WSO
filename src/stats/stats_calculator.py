from flask import session
from flask_login import current_user

from src.models import WorkoutSession, Schedule, Workout, Position, set_workout


class Calculator:
    def __init__(self, new_season_flag=False):
        # When new_season_flag is True, calculator returns data for first workout of each schedule
        self.new_season_flag = new_season_flag

        self.all_schedules = self.get_all_schedules()
        self.active_schedule_id = self.get_active_schedule_id()
        self.all_workout_sessions = self.get_all_workout_sessions()
        self.user_workout_sessions_count = self.get_user_workout_sessions_count()
        self.next_position_id = self.calculate_next_position_id()
        self.next_position = self.get_next_position()
        self.next_workout_best_time_session = self.get_next_workout_best_time_session()
        self.current_workout_session_season = self.calculate_current_workout_session_season()
        self.sets_in_next_workout = self.get_sets_in_next_workout()

    def get_all_schedules(self):
        return Schedule.query.all()

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

        if self.new_season_flag:
            next_position_id = (self.active_schedule_id * 100) + 1

        return next_position_id

    def get_next_position(self):
        return Position.query.filter_by(id=self.next_position_id).first()

    def get_next_workout_best_time_session(self):
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

        if self.new_season_flag:
            current_workout_session_season += 1

        return current_workout_session_season

    def get_sets_in_next_workout(self):
        if self.next_position:
            next_workout = Workout.query.filter_by(
                id=self.next_position.workout_id
            ).first()

            # For some reason the next_workout.sets list is not sorted - objects inside change positions with every call
            # This is a working solution - objects are sorted based on their position_in_workout attribute
            ordered_sets = []
            for i, value in enumerate(next_workout.sets, start=1):
                for obj in next_workout.sets:
                    if obj.position_in_workout == i:
                        ordered_sets.append(obj)

        else:
            ordered_sets = None

        return ordered_sets


