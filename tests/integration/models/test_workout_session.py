from src.models import WorkoutSessions, Users, Workouts, Positions, Schedules
from tests.general_base_test import GeneralBaseTest
from werkzeug.security import generate_password_hash


# noinspection PyArgumentList
class WorkoutSessionTest(GeneralBaseTest):
    def test_create_workout_session(self):
        with self.app_context():
            workout_session_1 = WorkoutSessions(
                date="1991/07/24",
                hours=1,
                minutes=30,
                seconds=20,
                season=1,
                user_id=1,
                workout_id=5,
                position_id=1,
                schedule_id=5
            )

            self.assertIsNone(WorkoutSessions.find_by_id(1))

            try:
                workout_session_1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(WorkoutSessions.find_by_id(1))
                self.assertEqual(1, WorkoutSessions.find_by_id(1).id)

    def test_class_methods(self):
        with self.app_context():
            workout_session_1 = WorkoutSessions(
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

            workout_session_2 = WorkoutSessions(
                date="1991/07/24",
                hours=1,
                minutes=30,
                seconds=20,
                season=1,
                user_id=1,
                workout_id=5,
                position_id=102,
                schedule_id=1
            )

            workout_session_3 = WorkoutSessions(
                date="1991/07/24",
                hours=1,
                minutes=30,
                seconds=20,
                season=2,
                user_id=1,
                workout_id=1,
                position_id=201,
                schedule_id=2
            )

            try:
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()
                workout_session_3.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                # class methods should return lists with these lengths
                self.assertEqual(2, len(WorkoutSessions.find_by_season(1)))
                self.assertEqual(2, len(WorkoutSessions.find_by_workout_id(1)))
                self.assertEqual(3, len(WorkoutSessions.find_by_user_id(1)))
                self.assertEqual(1, len(WorkoutSessions.find_by_position_id(201)))
                self.assertEqual(2, len(WorkoutSessions.find_by_schedule_id(1)))

                # if nothing is found, .first() returns None, whereas .all() returns an empty list
                self.assertIsNone(WorkoutSessions.find_by_id(5))
                self.assertListEqual(WorkoutSessions.find_by_user_id(2), [])

                # check that the data in lists can be queried and are correct
                self.assertEqual(101, WorkoutSessions.find_by_user_id(1)[0].position_id)
                self.assertEqual(30, WorkoutSessions.find_by_user_id(1)[1].minutes)

    def test_user_relationship(self):
        with self.app_context():
            workout_session_1 = WorkoutSessions(
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

            user1 = Users(
                first_name="John",
                last_name="Doe",
                email="John@Doe.com",
                password=generate_password_hash("1234", method='sha256')
            )

            try:
                workout_session_1.save_to_db()
                user1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertEqual(1, workout_session_1.users.id)
                self.assertEqual("John@Doe.com", workout_session_1.users.email)

    def test_workout_relationship(self):
        with self.app_context():
            workout_session_1 = WorkoutSessions(
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

            workout1 = Workouts(
                name="Core Strength",
                number_of_circles=5
            )

            try:
                workout_session_1.save_to_db()
                workout1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertEqual(1, workout_session_1.workouts.id)
                self.assertEqual("Core Strength", workout_session_1.workouts.name)

    def test_position_relationship(self):
        with self.app_context():
            workout_session_1 = WorkoutSessions(
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

            position101 = Positions(
                id=101, workout_id=1, week=1, day=1
            )

            try:
                workout_session_1.save_to_db()
                position101.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertEqual(101, workout_session_1.positions.id)
                self.assertEqual(1, workout_session_1.positions.week)

    def test_schedule_relationship(self):
        with self.app_context():
            workout_session_1 = WorkoutSessions(
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

            schedule1 = Schedules(
                name="Triatlon"
                )

            try:
                workout_session_1.save_to_db()
                schedule1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertEqual(1, workout_session_1.schedules.id)
                self.assertEqual("Triatlon", workout_session_1.schedules.name)