from src.models import Users, WorkoutSessions, Schedules, user_schedule
from tests.general_base_test import GeneralBaseTest
from datetime import datetime
from werkzeug.security import generate_password_hash


# noinspection PyArgumentList
class UserTest(GeneralBaseTest):
    def test_create_user(self):
        with self.app_context():
            test = Users(
                first_name="John",
                last_name="Doe",
                email="John@Doe.com",
                password=generate_password_hash("1234", method='sha256')
            )

            self.assertIsNone(Users.find_by_id(1))

            try:
                test.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                # test that id is created automatically
                self.assertIsNotNone(Users.find_by_id(1))
                self.assertEqual("John@Doe.com", Users.find_by_id(1).email)

                # check that date_created is added to the database automatically
                self.assertIsNotNone(Users.find_by_id(1).date_created)
                self.assertIsInstance(Users.find_by_id(1).date_created, datetime)

                # check that password is saved hashed
                self.assertIsNotNone(Users.find_by_id(1).password)
                self.assertIn("sha256$", Users.find_by_id(1).password)

    def test_create_multiple_users(self):
        with self.app_context():
            test1 = Users(
                first_name="John",
                last_name="Doe",
                email="John@Doe.com",
                password=generate_password_hash("1234", method='sha256')
            )

            test2 = Users(
                first_name="Test",
                last_name="Osteron",
                email="test@test.com",
                password=generate_password_hash("1234", method='sha256')
            )

            self.assertIsNone(Users.find_by_id(1))

            try:
                test1.save_to_db()
                test2.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(Users.find_by_id(1))
                self.assertEqual("John@Doe.com", Users.find_by_id(1).email)
                self.assertIsNotNone(Users.find_by_id(2))
                self.assertEqual("test@test.com", Users.find_by_id(2).email)
                self.assertEqual(2, Users.count_all())

    def test_user_email_is_unique(self):
        with self.app_context():
            test1 = Users(
                first_name="John",
                last_name="Doe",
                email="John@Doe.com",
                password=generate_password_hash("1234", method='sha256')
            )

            test2 = Users(
                first_name="John",
                last_name="Doe",
                email="John@Doe.com",
                password=generate_password_hash("1234", method='sha256')
            )

            try:
                test1.save_to_db()
                test2.save_to_db()
            except Exception as e:
                self.assertIn("(sqlite3.IntegrityError)", e.__str__())
            finally:
                with self.app_context():
                    self.assertIsNotNone(Users.find_by_id(1))
                    self.assertIsNone(Users.find_by_id(2))
                    self.assertEqual(1, Users.find_by_email("John@Doe.com").id)
                    self.assertEqual(1, Users.count_all())

    def test_workout_sessions_relationship(self):
        with self.app_context():
            user1 = Users(
                first_name="John",
                last_name="Doe",
                email="John@Doe.com",
                password=generate_password_hash("1234", method='sha256')
            )

            user2 = Users(
                first_name="Test",
                last_name="Osteron",
                email="test@test.com",
                password=generate_password_hash("1234", method='sha256')
            )

            workout_session_user_1 = WorkoutSessions(
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

            workout_session_user_2 = WorkoutSessions(
                date="1991/07/24",
                hours=1,
                minutes=30,
                seconds=20,
                season=1,
                user_id=2,
                workout_id=3,
                position_id=1,
                schedule_id=3
            )

            try:
                user1.save_to_db()
                user2.save_to_db()

                # workout_sessions should be an empty list before adding them to the database

                self.assertListEqual(user1.workout_sessions, [])
                self.assertListEqual(user2.workout_sessions, [])

                workout_session_user_1.save_to_db()
                workout_session_user_2.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertEqual(workout_session_user_1, user1.workout_sessions[0])
                self.assertEqual(workout_session_user_2, user2.workout_sessions[0])

                self.assertEqual(user1.workout_sessions[0].id, 1)
                self.assertEqual(user2.workout_sessions[0].id, 2)

                self.assertEqual(user1.workout_sessions[0].workout_id, 5)
                self.assertEqual(user2.workout_sessions[0].schedule_id, 3)

                self.assertEqual(len(user1.workout_sessions), 1)
                self.assertEqual(len(user2.workout_sessions), 1)

    def test_registered_schedules_relationship(self):
        with self.app_context():
            user1 = Users(
                first_name="John",
                last_name="Doe",
                email="John@Doe.com",
                password=generate_password_hash("1234", method='sha256')
            )

            user2 = Users(
                first_name="Test",
                last_name="Osteron",
                email="test@test.com",
                password=generate_password_hash("1234", method='sha256')
            )

            schedule1 = Schedules(
                name="Lane Goodwin Full"
            )
            schedule2 = Schedules(
                name="Lane Goodwin Best Of"
            )
            schedule3 = Schedules(
                name="Triatlon"
            )
            schedule4 = Schedules(
                name="Frontal Strength Only"
            )

            try:
                user1.save_to_db()
                user2.save_to_db()

                schedule1.save_to_db()
                schedule2.save_to_db()
                schedule3.save_to_db()
                schedule4.save_to_db()

                self.assertListEqual(user1.registered_schedules, [])
                self.assertListEqual(user2.registered_schedules, [])

                user1.registered_schedules.append(schedule1)

                user2.registered_schedules.append(schedule2)
                user2.registered_schedules.append(schedule3)
                user2.registered_schedules.append(schedule4)

            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertEqual(schedule1, user1.registered_schedules[0])

                self.assertEqual(schedule2, user2.registered_schedules[0])
                self.assertEqual(schedule3, user2.registered_schedules[1])
                self.assertEqual(schedule4, user2.registered_schedules[2])

                self.assertEqual(user1.registered_schedules[0].id, 1)
                self.assertEqual(user2.registered_schedules[2].id, 4)
                self.assertEqual(user2.registered_schedules[1].name, "Triatlon")
