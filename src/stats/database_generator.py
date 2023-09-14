from werkzeug.security import generate_password_hash

from src.models import User, Schedule, Workout, Position, Set, Exercise
from src.db import db


# noinspection PyArgumentList
class DatabaseGenerator:
    @staticmethod
    def recreate_development_database():
        pass

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

        workout6 = Workout(
            name="Upper Body Strength", number_of_circles=5
        )
        workout7 = Workout(
            name="Leg Skills", number_of_circles=5
        )
        workout8 = Workout(
            name="Explosive Strength", number_of_circles=5
        )
        workout9 = Workout(
            name="Upper Body Skills", number_of_circles=5
        )
        workout10 = Workout(
            name="Core Skills", number_of_circles=5
        )

        workout21 = Workout(
            id=21, name="Běh 3km", number_of_circles=1
        )
        workout22 = Workout(
            id=22, name="Jízda na kole 20km", number_of_circles=1
        )
        workout23 = Workout(
            id=23, name="Plavání 2km", number_of_circles=1
        )

        # EXERCISES

        exercise1 = Exercise(
            name="Burpee"
        )
        exercise2 = Exercise(
            name="Pull Up"
        )
        exercise3 = Exercise(
            name="Push Up"
        )
        exercise4 = Exercise(
            name="Sit Up"
        )
        exercise5 = Exercise(
            name="Squat"
        )
        exercise6 = Exercise(
            name="Leg Raise"
        )
        exercise7 = Exercise(
            name="Lunge"
        )
        exercise8 = Exercise(
            name="Jump"
        )

        # Here starts exercises for triatlon
        exercise9 = Exercise(
            name="Běh"
        )
        exercise10 = Exercise(
            name="Jízda na kole"
        )
        exercise11 = Exercise(
            name="Plavání"
        )

        # SETS

        set1 = Set(
            exercise_id=1,
            position_in_workout=1,
            number_of_reps=15
        )
        set2 = Set(
            exercise_id=4,
            position_in_workout=2,
            number_of_reps=30
        )
        set3 = Set(
            exercise_id=1,
            position_in_workout=3,
            number_of_reps=15
        )
        set4 = Set(
            exercise_id=7,
            position_in_workout=4,
            number_of_reps=20
        )
        set5 = Set(
            exercise_id=2,
            position_in_workout=1,
            number_of_reps=15
        )
        set6 = Set(
            exercise_id=3,
            position_in_workout=2,
            number_of_reps=30
        )
        set7 = Set(
            exercise_id=4,
            position_in_workout=3,
            number_of_reps=30
        )
        set8 = Set(
            exercise_id=5,
            position_in_workout=4,
            number_of_reps=30
        )
        set9 = Set(
            exercise_id=7,
            position_in_workout=1,
            number_of_reps=50
        )
        set10 = Set(
            exercise_id=8,
            position_in_workout=2,
            number_of_reps=10
        )
        set11 = Set(
            exercise_id=5,
            position_in_workout=3,
            number_of_reps=50
        )
        set12 = Set(
            exercise_id=8,
            position_in_workout=4,
            number_of_reps=10
        )
        set13 = Set(
            exercise_id=1,
            position_in_workout=1,
            number_of_reps=20
        )
        set14 = Set(
            exercise_id=2,
            position_in_workout=2,
            number_of_reps=10
        )
        set15 = Set(
            exercise_id=3,
            position_in_workout=3,
            number_of_reps=20
        )
        set16 = Set(
            exercise_id=3,
            position_in_workout=1,
            number_of_reps=20
        )
        set17 = Set(
            exercise_id=5,
            position_in_workout=2,
            number_of_reps=40
        )
        set18 = Set(
            exercise_id=4,
            position_in_workout=4,
            number_of_reps=20
        )
        set19 = Set(
            exercise_id=5,
            position_in_workout=1,
            number_of_reps=20
        )
        set20 = Set(
            exercise_id=7,
            position_in_workout=2,
            number_of_reps=20
        )
        set21 = Set(
            exercise_id=6,
            position_in_workout=3,
            number_of_reps=20
        )
        set22 = Set(
            exercise_id=1,
            position_in_workout=1,
            number_of_reps=30
        )
        set23 = Set(
            exercise_id=2,
            position_in_workout=2,
            number_of_reps=7
        )
        set24 = Set(
            exercise_id=3,
            position_in_workout=3,
            number_of_reps=15
        )
        set25 = Set(
            exercise_id=2,
            position_in_workout=1,
            number_of_reps=7
        )
        set26 = Set(
            exercise_id=3,
            position_in_workout=2,
            number_of_reps=14
        )
        set27 = Set(
            exercise_id=4,
            position_in_workout=3,
            number_of_reps=21
        )

        # Here starts sets for triatlon
        set28 = Set(
            exercise_id=9,
            position_in_workout=1,
            number_of_reps=3
        )
        set29 = Set(
            exercise_id=10,
            position_in_workout=1,
            number_of_reps=20
        )
        set30 = Set(
            exercise_id=11,
            position_in_workout=1,
            number_of_reps=2
        )

        # Create first 4 days of Lane Goodwin Full Schedule and 2 weeks of Triatlon schedule
        position101 = Position(
            id=101,
            workout_id=5,
            week=1,
            day=1
        )
        position102 = Position(
            id=102,
            workout_id=1,
            week=1,
            day=2
        )
        position103 = Position(
            id=103,
            workout_id=9,
            week=1,
            day=3
        )
        position104 = Position(
            id=104,
            workout_id=8,
            week=1,
            day=4
        )
        position105 = Position(
            id=105,
            workout_id=1,
            week=2,
            day=1
        )
        position106 = Position(
            id=106,
            workout_id=4,
            week=2,
            day=2
        )
        position107 = Position(
            id=107,
            workout_id=7,
            week=2,
            day=3
        )
        position108 = Position(
            id=108,
            workout_id=5,
            week=2,
            day=4
        )
        position109 = Position(
            id=109,
            workout_id=9,
            week=3,
            day=1
        )
        position110 = Position(
            id=110,
            workout_id=8,
            week=3,
            day=2
        )
        position111 = Position(
            id=111,
            workout_id=10,
            week=3,
            day=3
        )
        position112 = Position(
            id=112,
            workout_id=2,
            week=3,
            day=4
        )
        position113 = Position(
            id=113,
            workout_id=5,
            week=4,
            day=1
        )
        position114 = Position(
            id=114,
            workout_id=9,
            week=4,
            day=2
        )
        position115 = Position(
            id=115,
            workout_id=8,
            week=4,
            day=3
        )
        position116 = Position(
            id=116,
            workout_id=7,
            week=4,
            day=4
        )
        position117 = Position(
            id=117,
            workout_id=6,
            week=5,
            day=1
        )
        position118 = Position(
            id=118,
            workout_id=3,
            week=5,
            day=2
        )
        position119 = Position(
            id=119,
            workout_id=9,
            week=5,
            day=3
        )
        position120 = Position(
            id=120,
            workout_id=2,
            week=5,
            day=4
        )
        position121 = Position(
            id=121,
            workout_id=4,
            week=6,
            day=1
        )
        position122 = Position(
            id=122,
            workout_id=7,
            week=6,
            day=2
        )
        position123 = Position(
            id=123,
            workout_id=5,
            week=6,
            day=3
        )
        position124 = Position(
            id=124,
            workout_id=6,
            week=6,
            day=4
        )
        position125 = Position(
            id=125,
            workout_id=10,
            week=7,
            day=1
        )
        position126 = Position(
            id=126,
            workout_id=5,
            week=7,
            day=2
        )
        position127 = Position(
            id=127,
            workout_id=3,
            week=7,
            day=3
        )
        position128 = Position(
            id=128,
            workout_id=9,
            week=7,
            day=4
        )
        position129 = Position(
            id=129,
            workout_id=8,
            week=8,
            day=1
        )
        position130 = Position(
            id=130,
            workout_id=5,
            week=8,
            day=2
        )
        position131 = Position(
            id=131,
            workout_id=1,
            week=8,
            day=3
        )
        position132 = Position(
            id=132,
            workout_id=5,
            week=8,
            day=4
        )
        position133 = Position(
            id=133,
            workout_id=3,
            week=9,
            day=1
        )
        position134 = Position(
            id=134,
            workout_id=4,
            week=9,
            day=2
        )
        position135 = Position(
            id=135,
            workout_id=10,
            week=9,
            day=3
        )
        position136 = Position(
            id=136,
            workout_id=2,
            week=9,
            day=4
        )
        position137 = Position(
            id=137,
            workout_id=1,
            week=10,
            day=1
        )
        position138 = Position(
            id=138,
            workout_id=9,
            week=10,
            day=2
        )
        position139 = Position(
            id=139,
            workout_id=1,
            week=10,
            day=3
        )
        position140 = Position(
            id=140,
            workout_id=2,
            week=10,
            day=4
        )
        position141 = Position(
            id=141,
            workout_id=3,
            week=11,
            day=1
        )
        position142 = Position(
            id=142,
            workout_id=4,
            week=11,
            day=2
        )
        position143 = Position(
            id=143,
            workout_id=10,
            week=11,
            day=3
        )
        position144 = Position(
            id=144,
            workout_id=6,
            week=11,
            day=4
        )
        position145 = Position(
            id=145,
            workout_id=8,
            week=12,
            day=1
        )
        position146 = Position(
            id=146,
            workout_id=1,
            week=12,
            day=2
        )
        position147 = Position(
            id=147,
            workout_id=4,
            week=12,
            day=3
        )
        position148 = Position(
            id=148,
            workout_id=5,
            week=12,
            day=4
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
            workout6, workout7, workout8, workout9, workout10,
            workout21, workout22, workout23,
            exercise1, exercise2, exercise3, exercise4, exercise5, exercise6, exercise7, exercise8,
            exercise9, exercise10, exercise11,
            set1, set2, set3, set4, set5, set6, set7, set8, set9, set10,
            set11, set12, set13, set14, set15, set16, set17, set18, set19, set20,
            set21, set22, set23, set24, set25, set26, set27, set28, set29, set30
        ]
        # Lane Goodwin Full Workout positions
        objects_to_add_to_session.extend([
            position101, position102, position103, position104,
            position105, position106, position107, position108,
            position109, position110, position111, position112,
            position113, position114, position115, position116,
            position117, position118, position119, position120,
            position121, position122, position123, position124,
            position125, position126, position127, position128,
            position129, position130, position131, position132,
            position133, position134, position135, position136,
            position137, position138, position139, position140,
            position141, position142, position143, position144,
            position145, position146, position147, position148,
        ])
        # Triathlon positions
        objects_to_add_to_session.extend([
            position201, position202, position203,
            position204, position205, position206
        ])

        for obj in objects_to_add_to_session:
            db.session.add(obj)

        db.session.commit()

        # LINK SETS WITH WORKOUTS

        workout1.sets.extend([set1, set2, set3, set4])
        workout2.sets.extend([set5, set6, set7, set8])
        workout3.sets.extend([set9, set10, set11, set12])
        workout4.sets.extend([set13, set14, set15, set8])
        workout5.sets.extend([set16, set17, set15, set18])
        workout6.sets.extend([set5, set6, set7])
        workout7.sets.extend([set19, set20, set21])
        workout8.sets.extend([set22, set23, set24])
        workout9.sets.extend([set25, set26, set27])
        workout10.sets.extend([set13, set10])

        workout21.sets.extend([set28])
        workout22.sets.extend([set29])
        workout23.sets.extend([set30])

        db.session.commit()