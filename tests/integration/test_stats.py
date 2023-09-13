from werkzeug.security import generate_password_hash
from flask import get_flashed_messages
from flask_login import current_user

from tests.general_base_test import GeneralBaseTest

from src.models import User, WorkoutSession
from src.stats.stats_calculator import Calculator
from src.stats.database_generator import DatabaseGenerator


# noinspection PyArgumentList
class StatsTest(GeneralBaseTest):
    def setUp(self):
        #  create new test user every time
        super(StatsTest, self).setUp()  # making sure the General base test setup works as well
        with self.app() as client:
            with self.app_context():
                #  Create test user that will be logged in
                DatabaseGenerator.create_test_user()
                DatabaseGenerator.create_automatic_testing_database()

    def test_logged_user_can_refresh_page(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)
                for category, message in messages:
                    self.assertEqual('success', category),
                    self.assertEqual("Logged in!", message)

                response = client.get(
                    "/stats/",
                    follow_redirects=True
                )

                self.assertEqual(200, response.status_code)
                self.assertEqual(0, len(response.history))
                self.assertEqual("/stats/", response.request.path)
                self.assertIn(b"Overview", response.data)

    def test_log_out_logged_user(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })
                response = client.get(
                    "/auth/logout",
                    follow_redirects=True
                )

                self.assertEqual(200, response.status_code)
                self.assertEqual(1, len(response.history))
                self.assertEqual("/auth/login", response.request.path)
                self.assertIn(b"Log into your account", response.data)

    def test_log_in_is_required(self):
        with self.app() as client:
            with self.app_context():
                response = client.get(
                    "/stats/",
                    follow_redirects=True
                )

                self.assertEqual(200, response.status_code)
                self.assertEqual(1, len(response.history))
                self.assertEqual("/auth/login", response.request.path)
                self.assertIn(b"Log into your account", response.data)
                self.assertIn(b'next=%2Fstats%2F', response.request.query_string)

    def test_current_user_variable(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                self.assertEqual("John@Doe.com", current_user.email)
                self.assertEqual("John", current_user.first_name)

                client.get(
                    "/auth/logout",
                    follow_redirects=True
                )
                #  Know when the user logged out, accessing current user email should throw an error
                try:
                    self.assertFalse("John@Doe.com", current_user.email)
                except AttributeError as e:
                    self.assertIsNotNone(e)
                finally:
                    test2 = User(
                        first_name="Test",
                        last_name="Osteron",
                        email="test@test.com",
                        password=generate_password_hash("1234", method='sha256')
                    )
                    test2.save_to_db()

                    client.post(
                        "/auth/login",
                        follow_redirects=True,
                        data={
                            "login_email": "test@test.com",
                            "login_password": 1234
                        })

                    self.assertEqual("test@test.com", current_user.email)
                    self.assertEqual("Test", current_user.first_name)

    def test_active_schedule_id_variable(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                calculator = Calculator()

                self.assertEqual(b'schedule_selector=1', response.request.query_string)
                self.assertEqual(1, calculator.active_schedule_id)

                response = client.get(
                    "/stats/",
                    follow_redirects=True,
                    query_string={
                        "schedule_selector": 2
                    })

                calculator = Calculator()

                self.assertEqual(b'schedule_selector=2', response.request.query_string)
                self.assertEqual(2, calculator.active_schedule_id)

    def test_all_schedules_variable(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                calculator = Calculator()

                expected1 = "[<Class: Schedule; Id: 1; Name: Lane Goodwin Full>, <Class: Schedule; Id: 2; Name: " \
                            "Triatlon>]"
                self.assertEqual(expected1, repr(calculator.all_schedules))

                #  Make sure you can loop through the all_schedules and get correct results
                expected2 = ("Lane Goodwin Full", "Triatlon")
                for count, schedule in enumerate(calculator.all_schedules):
                    self.assertEqual(count + 1, schedule.id)
                    self.assertEqual(expected2[count], schedule.name)

    def test_all_workout_sessions_variable(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                calculator = Calculator()
                self.assertListEqual([], calculator.get_all_workout_sessions())

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

                # This is the session of another user, the calculator should ignore it
                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=2,
                    workout_id=1,
                    position_id=101,
                    schedule_id=1
                )
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()

                calculator = Calculator()
                self.assertListEqual([workout_session_1], calculator.get_all_workout_sessions())
                self.assertEqual(1, len(calculator.get_all_workout_sessions()))

    def test_user_workout_sessions_count_variable(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                calculator = Calculator()
                self.assertEqual(0, calculator.get_user_workout_sessions_count())

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

                # This is the session of another user, the calculator should ignore it
                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=2,
                    workout_id=1,
                    position_id=101,
                    schedule_id=1
                )
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()

                calculator = Calculator()
                self.assertEqual(1, calculator.get_user_workout_sessions_count())

    def test_position_id_variable(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                calculator = Calculator()
                self.assertEqual(101, calculator.next_position_id)

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

                # This is the session of another user, the calculator should ignore it
                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=2,
                    workout_id=21,
                    position_id=201,
                    schedule_id=2
                )
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()

                calculator = Calculator()
                self.assertEqual(102, calculator.next_position_id)

                workout_session_3 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=1,
                    workout_id=21,
                    position_id=201,
                    schedule_id=2
                )
                workout_session_3.save_to_db()

                # If the user wish to start a new season, calculator with new_season_flag=True
                # handles the calculation and sets next_position_id to first position of the given schedule

                client.get(
                    "/stats/",
                    follow_redirects=True,
                    query_string={
                        "schedule_selector": 2
                    })
                calculator = Calculator(new_season_flag=True)
                self.assertEqual(201, calculator.next_position_id)

    def test_next_position_variable(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                calculator = Calculator()
                self.assertEqual(
                    "<Class: Position; Id: 101; WorkoutId: 5>", str(calculator.next_position)
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
                workout_session_1.save_to_db()

                calculator = Calculator()
                self.assertEqual(
                    "<Class: Position; Id: 102; WorkoutId: 1>", str(calculator.next_position)
                )

    def test_next_workout_best_time_variable(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                calculator = Calculator()
                self.assertIsNone(calculator.next_workout_best_time_session)

                workout_session_1 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=1,
                    workout_id=1,
                    position_id=102,
                    schedule_id=1
                )

                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=1,
                    workout_id=8,
                    position_id=104,
                    schedule_id=1
                )

                # This is the session of another user, the calculator should ignore it
                workout_session_3 = WorkoutSession(
                    date="1991/07/24",
                    hours=0,
                    minutes=1,
                    seconds=1,
                    season=1,
                    user_id=2,
                    workout_id=1,
                    position_id=102,
                    schedule_id=1
                )
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()
                workout_session_3.save_to_db()

                calculator = Calculator()
                self.assertIsNotNone(calculator.next_workout_best_time_session)
                self.assertEqual(1, calculator.next_workout_best_time_session.hours)
                self.assertEqual(30, calculator.next_workout_best_time_session.minutes)
                self.assertEqual(20, calculator.next_workout_best_time_session.seconds)

                # New season, but worse time
                workout_session_5 = WorkoutSession(
                    date="1991/07/24",
                    hours=2,
                    minutes=1,
                    seconds=1,
                    season=2,
                    user_id=1,
                    workout_id=1,
                    position_id=102,
                    schedule_id=1
                )

                workout_session_6 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=2,
                    user_id=1,
                    workout_id=8,
                    position_id=104,
                    schedule_id=1
                )
                workout_session_5.save_to_db()
                workout_session_6.save_to_db()

                calculator = Calculator()
                self.assertEqual(1, calculator.next_workout_best_time_session.hours)
                self.assertEqual(30, calculator.next_workout_best_time_session.minutes)
                self.assertEqual(20, calculator.next_workout_best_time_session.seconds)

                # New season, better than ever before
                workout_session_7 = WorkoutSession(
                    date="1991/07/24",
                    hours=0,
                    minutes=59,
                    seconds=59,
                    season=3,
                    user_id=1,
                    workout_id=1,
                    position_id=102,
                    schedule_id=1
                )

                workout_session_8 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=3,
                    user_id=1,
                    workout_id=8,
                    position_id=104,
                    schedule_id=1
                )
                workout_session_7.save_to_db()
                workout_session_8.save_to_db()

                calculator = Calculator()
                self.assertEqual(0, calculator.next_workout_best_time_session.hours)
                self.assertEqual(59, calculator.next_workout_best_time_session.minutes)
                self.assertEqual(59, calculator.next_workout_best_time_session.seconds)

    def test_current_workout_session_season_variable(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                calculator = Calculator()
                self.assertEqual(1, calculator.current_workout_session_season)

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
                workout_session_1.save_to_db()

                calculator = Calculator()
                self.assertEqual(1, calculator.current_workout_session_season)

                # The data should be retrieved based on the last added workout session
                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=2,
                    user_id=1,
                    workout_id=1,
                    position_id=101,
                    schedule_id=1
                )
                workout_session_2.save_to_db()

                calculator = Calculator()
                self.assertEqual(2, calculator.current_workout_session_season)

                # If the user wish to start a new season, calculator with new_season_flag=True
                # handles the calculation and increases season by 1
                calculator = Calculator(new_season_flag=True)
                self.assertEqual(3, calculator.current_workout_session_season)
