from src.models import Workout, WorkoutSession, Position, Set
from tests.general_base_test import GeneralBaseTest


# noinspection PyArgumentList
class WorkoutTest(GeneralBaseTest):
    def test_create_workout(self):
        with self.app_context():
            workout1 = Workout(
                name="Core Strength",
                number_of_circles=5
            )

            self.assertIsNone(Workout.find_by_id(1))

            try:
                workout1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(Workout.find_by_id(1))
                self.assertEqual(1, Workout.find_by_id(1).id)
                self.assertEqual("Core Strength", Workout.find_by_id(1).name)
                self.assertEqual(5, Workout.find_by_id(1).number_of_circles)

    def test_workout_session_relationship(self):
        with self.app_context():
            workout1 = Workout(
                name="Core Strength",
                number_of_circles=5
            )

            workout_session_1 = WorkoutSession(
                date="1991/07/24",
                hours=1,
                minutes=30,
                seconds=20,
                season=1,
                user_id=1,
                workout_id=1,
                position_id=101,
                schedule_id=1
            )

            workout_session_2 = WorkoutSession(
                date="2022/02/02",
                hours=1,
                minutes=30,
                seconds=20,
                season=1,
                user_id=1,
                workout_id=5,
                position_id=102,
                schedule_id=1
            )

            workout_session_3 = WorkoutSession(
                date="2000/12/24",
                hours=1,
                minutes=30,
                seconds=20,
                season=1,
                user_id=1,
                workout_id=1,
                position_id=103,
                schedule_id=1
            )
            try:
                workout1.save_to_db()
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()
                workout_session_3.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsInstance(workout1.workout_sessions[0], WorkoutSession)
                self.assertEqual(2, len(workout1.workout_sessions))

                self.assertEqual(1, workout1.workout_sessions[0].id)
                self.assertEqual(3, workout1.workout_sessions[1].id)

                self.assertEqual("1991/07/24", workout1.workout_sessions[0].date)

    def test_position_relationship(self):
        with self.app_context():
            workout1 = Workout(
                name="Core Strength",
                number_of_circles=5
            )

            position101 = Position(
                id=101, workout_id=1, week=1, day=1
            )

            position206 = Position(
                id=206, workout_id=1, week=2, day=2
            )

            try:
                workout1.save_to_db()
                position101.save_to_db()
                position206.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsInstance(workout1.positions[0], Position)
                self.assertEqual(2, len(workout1.positions))

                self.assertEqual(101, workout1.positions[0].id)
                self.assertEqual(1, workout1.positions[0].week)

                self.assertEqual(206, workout1.positions[1].id)
                self.assertEqual(2, workout1.positions[1].week)

    def test_set_relationship(self):
        with self.app_context():
            workout1 = Workout(
                name="Core Strength",
                number_of_circles=5
            )
            set1 = Set(
                exercise_id=1,
                position_in_workout=1,
                number_of_reps=15
            )
            set2 = Set(
                exercise_id=2,
                position_in_workout=2,
                number_of_reps=10
            )
            try:
                workout1.save_to_db()
                set1.save_to_db()
                set2.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertListEqual([], workout1.sets)

                workout1.sets.extend([set1, set2])

                self.assertIsInstance(workout1.sets[0], Set)

                self.assertEqual(1, workout1.sets[0].exercise_id)
                self.assertEqual(2, workout1.sets[1].exercise_id)
                self.assertEqual(2, workout1.sets[1].position_in_workout)
                self.assertEqual(10, workout1.sets[1].number_of_reps)




