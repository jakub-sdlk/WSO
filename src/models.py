from src.db import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from src.general_model import GeneralModel

user_schedule = db.Table('user_schedule',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id'))
                         )


class User(db.Model, UserMixin, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    workout_sessions = db.relationship('WorkoutSession', backref='user', passive_deletes=True)
    registered_schedules = db.relationship('Schedule', secondary=user_schedule, backref='registered_users')

    def __repr__(self):
        return f"<Class: User; Id: {self.id}; Email: {self.email}>"

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class WorkoutSession(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    hours = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    season = db.Column(db.Integer)  # add foreign key relationship later on

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)

    # positions = db.relationship('Position', backref='workout_session', lazy=True)

    def __repr__(self):
        return f"<Class: WorkoutSession; Id: {self.id}; WorkoutId: {self.workout_id}>"

    @classmethod
    def find_by_season(cls, season):
        return cls.query.filter_by(season=season).all()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_workout_id(cls, workout_id):
        return cls.query.filter_by(workout_id=workout_id).all()

    @classmethod
    def find_by_position_id(cls, position_id):
        return cls.query.filter_by(position_id=position_id).all()

    @classmethod
    def find_by_schedule_id(cls, schedule_id):
        return cls.query.filter_by(schedule_id=schedule_id).all()


class Workout(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    number_of_circles = db.Column(db.Integer)

    positions = db.relationship('Position', backref='workout', lazy=True)
    workout_sessions = db.relationship('WorkoutSession', backref='workout', lazy=True)

    def __repr__(self):
        return f"<Class: Workout; Id: {self.id}; Name: {self.name}>"


class Schedule(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    workout_sessions = db.relationship('WorkoutSession', backref='schedule', lazy=True)

    def __repr__(self):
        return f"<Class: Schedule; Id: {self.id}; Name: {self.name}>"


class Position(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    week = db.Column(db.Integer)
    day = db.Column(db.Integer)

    workout_sessions = db.relationship('WorkoutSession', backref='position', lazy=True)

    def __repr__(self):
        return f"<Class: Position; Id: {self.id}; WorkoutId: {self.workout_id}>"


class Exercise(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

    sets = db.relationship('Set', backref='exercise', lazy=True)

    def __repr__(self):
        return f"<Class: Exercise; Id: {self.id}; Name: {self.name}>"


class Set(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    position_in_workout = db.Column(db.Integer)
    number_of_reps = db.Column(db.Integer)

    def __repr__(self):
        return f"<Class: Set; Id: {self.id}; ExerciseId: {self.exercise_id}>"

