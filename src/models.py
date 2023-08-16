from db import db
from flask_login import UserMixin
from sqlalchemy.sql import func

user_schedule = db.Table('user_schedule',
                         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                         db.Column('schedule_id', db.Integer, db.ForeignKey('schedules.id'))
                         )


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    workout_sessions = db.relationship('WorkoutSessions', backref='users', passive_deletes=True)
    registered_schedules = db.relationship('Schedules', secondary=user_schedule, backref='registered_users')

    def __repr__(self):
        return f'<User: {self.first_name} {self.last_name}>'


class WorkoutSessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    hours = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    season = db.Column(db.Integer)  # add foreign key relationship later on

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
    positions = db.relationship('Positions', backref='workout_session', lazy=True)

    def __repr__(self):
        return f'<WorkoutSession: {self.id}>'


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    number_of_circles = db.Column(db.Integer)
    positions = db.relationship('Positions', backref='workout', lazy=True)

    def __repr__(self):
        return f'<Workout: {self.name}>'


class Schedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    workout_sessions = db.relationship('WorkoutSessions', backref='schedule', lazy=True)

    def __repr__(self):
        return f'<Schedule: {self.name}>'


class Positions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    week = db.Column(db.Integer)
    day = db.Column(db.Integer)
