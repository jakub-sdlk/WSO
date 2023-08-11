from db import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    workout_sessions = db.relationship('WorkoutSessions', backref='users', passive_deletes=True)


class WorkoutSessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    hours = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    season = db.Column(db.Integer)  # add foreign key relationship later on
    schedule_id = db.Column(db.Integer)  # add foreign key relationship later on
    pos_in_schedule = db.Column(db.Integer)

