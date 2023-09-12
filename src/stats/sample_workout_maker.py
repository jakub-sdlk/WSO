from src.models import WorkoutSession, Schedule, Workout, Position
from src.db import db


class WorkoutMaker:
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

        db.session.add(schedule1)
        db.session.add(schedule2)
        db.session.add(schedule3)
        db.session.add(schedule4)

        db.session.add(workout1)
        db.session.add(workout2)
        db.session.add(workout3)
        db.session.add(workout4)
        db.session.add(workout5)

        db.session.add(workout21)
        db.session.add(workout22)
        db.session.add(workout23)

        db.session.add(position101)
        db.session.add(position102)
        db.session.add(position103)
        db.session.add(position104)

        db.session.add(position401)
        db.session.add(position402)
        db.session.add(position403)
        db.session.add(position404)

        db.session.add(position301)
        db.session.add(position302)
        db.session.add(position303)
        db.session.add(position304)
        db.session.add(position305)
        db.session.add(position306)

        db.session.commit()