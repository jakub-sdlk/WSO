from src.models import Position, Workout, WorkoutSession
from tests.general_base_test import GeneralBaseTest


# noinspection PyArgumentList
class PositionTest(GeneralBaseTest):
    def test_create_position(self):
        with self.app_context():
            position101 = Position(
                id=101, workout_id=1, week=1, day=1
            )

            self.assertIsNone(Position.find_by_id(1))

            try:
                position101.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(Position.find_by_id(101))
                self.assertEqual(101, Position.find_by_id(101).id)
                self.assertEqual(1, Position.find_by_id(101).workout_id)
                self.assertEqual(1, Position.find_by_id(101).week)
                self.assertEqual(1, Position.find_by_id(101).day)

    def test_workout_session_relationship(self):
        with self.app_context():
            position101 = Position(
                id=101, workout_id=1, week=1, day=1
            )

            position102 = Position(
                id=102, workout_id=3, week=1, day=2
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
                season=2,
                user_id=1,
                workout_id=1,
                position_id=101,
                schedule_id=1
            )

            try:
                position101.save_to_db()
                position102.save_to_db()
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()
                workout_session_3.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsInstance(position101.workout_sessions[0], WorkoutSession)
                self.assertEqual(2, len(position101.workout_sessions))
                self.assertEqual(1, len(position102.workout_sessions))

                self.assertEqual(1, position101.workout_sessions[0].id)
                self.assertEqual(3, position101.workout_sessions[1].id)

                self.assertEqual("1991/07/24", position101.workout_sessions[0].date)
                self.assertEqual("2022/02/02", position102.workout_sessions[0].date)

    def test_workout_relationship(self):
        with self.app_context():
            position101 = Position(
                id=101, workout_id=1, week=1, day=1
            )

            workout1 = Workout(
                name="Core Strength",
                number_of_circles=5
            )

            try:
                position101.save_to_db()
                workout1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertEqual(1, position101.workout.id)
                self.assertEqual("Core Strength", position101.workout.name)
                self.assertEqual(5, position101.workout.number_of_circles)