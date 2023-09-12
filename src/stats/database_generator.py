from werkzeug.security import generate_password_hash

from src.models import User, WorkoutSession, Schedule, Workout, Position
from src.db import db


# noinspection PyArgumentList
class DatabaseGenerator:
    @staticmethod
    def recreate_development_database():

        # SCHEDULES

        schedule1 = Schedule(
            name="Lane Goodwin Full"
        )
        schedule2 = Schedule(
            name="Lane Goodwin Best Of"
        )
        schedule3 = Schedule(
            name="Triatlon"
        )
        schedule4 = Schedule(
            name="Frontal Strength Only"
        )

        # WORKOUTS

        workout1 = Workout(
            name="Core Strength", number_of_circles=5
        )
        workout2 = Workout(
            name="Full Fledged Strength", number_of_circles=5
        )
        workout3 = Workout(
            name="Leg Strength", number_of_circles=5
        )
        workout4 = Workout(
            name="V-Taper", number_of_circles=5
        )
        workout5 = Workout(
            name="Frontal Strength", number_of_circles=5
        )

        workout21 = Workout(
            id=21, name="Běh 3km", number_of_circles=1
        )
        workout22 = Workout(
            id=22, name="Jízda na kole 20km", number_of_circles=1
        )
        workout23 = Workout(
            id=23, name="Plavání 1,5km", number_of_circles=1
        )

        # POSITIONS

        position101 = Position(
            id=101, workout_id=1, week=1, day=1
        )
        position102 = Position(
            id=102, workout_id=3, week=1, day=2
        )
        position103 = Position(
            id=103, workout_id=1, week=1, day=3
        )
        position104 = Position(
            id=104, workout_id=2, week=1, day=4
        )

        position401 = Position(
            id=401, workout_id=5, week=1, day=1
        )
        position402 = Position(
            id=402, workout_id=5, week=1, day=2
        )
        position403 = Position(
            id=403, workout_id=5, week=1, day=3
        )
        position404 = Position(
            id=404, workout_id=5, week=2, day=1
        )

        position301 = Position(
            id=301, workout_id=21, week=1, day=1
        )
        position302 = Position(
            id=302, workout_id=22, week=1, day=2
        )
        position303 = Position(
            id=303, workout_id=23, week=1, day=3
        )

        position304 = Position(
            id=304, workout_id=21, week=2, day=1
        )
        position305 = Position(
            id=305, workout_id=22, week=2, day=2
        )
        position306 = Position(
            id=306, workout_id=23, week=2, day=3
        )

        objects_to_add_to_session = [
            schedule1, schedule2, schedule3, schedule4,
            workout1, workout2, workout3, workout4, workout5,
            workout21, workout22, workout23,
            position101, position102, position103, position104,
            position401, position402, position403, position404,
            position301, position302, position303, position304, position305, position306
        ]

        for obj in objects_to_add_to_session:
            db.session.add(obj)

        db.session.commit()

    @staticmethod
    def create_test_user():
        #  Create test user that will be logged in
        user1 = User(
            first_name="John",
            last_name="Doe",
            email="John@Doe.com",
            password=generate_password_hash("1234", method='sha256')
        )
        user1.save_to_db()

    @staticmethod
    def create_automatic_testing_database():
        # Create 2 test schedules
        schedule1 = Schedule(
            name="Lane Goodwin Full"
        )
        schedule2 = Schedule(
            name="Triatlon"
        )

        #  Create test workouts for Lane Goodwin full and Triatlon schedules
        workout1 = Workout(
            name="Core Strength", number_of_circles=5
        )
        workout2 = Workout(
            name="Full Fledged Strength", number_of_circles=5
        )
        workout3 = Workout(
            name="Leg Strength", number_of_circles=5
        )
        workout4 = Workout(
            name="V-Taper", number_of_circles=5
        )
        workout5 = Workout(
            name="Frontal Strength", number_of_circles=5
        )

        workout21 = Workout(
            id=21, name="Běh 3km", number_of_circles=1
        )
        workout22 = Workout(
            id=22, name="Jízda na kole 20km", number_of_circles=1
        )
        workout23 = Workout(
            id=23, name="Plavání 1,5km", number_of_circles=1
        )

        # Create first 4 days of Lane Goodwin Full Schedule and 2 weeks of Triatlon schedule
        position101 = Position(
            id=101, workout_id=1, week=1, day=1
        )
        position102 = Position(
            id=102, workout_id=3, week=1, day=2
        )
        position103 = Position(
            id=103, workout_id=1, week=1, day=3
        )
        position104 = Position(
            id=104, workout_id=2, week=1, day=4
        )

        position201 = Position(
            id=201, workout_id=21, week=1, day=1
        )
        position202 = Position(
            id=202, workout_id=22, week=1, day=2
        )
        position203 = Position(
            id=203, workout_id=23, week=1, day=3
        )

        position204 = Position(
            id=204, workout_id=21, week=2, day=1
        )
        position205 = Position(
            id=205, workout_id=22, week=2, day=2
        )
        position206 = Position(
            id=206, workout_id=23, week=2, day=3
        )

        objects_to_add_to_session = [
            schedule1, schedule2,
            workout1, workout2, workout3, workout4, workout5,
            workout21, workout22, workout23,
            position101, position102, position103, position104,
            position201, position202, position203, position204, position205, position206
        ]

        for obj in objects_to_add_to_session:
            db.session.add(obj)

        db.session.commit()
