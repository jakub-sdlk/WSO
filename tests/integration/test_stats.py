from tests.general_base_test import GeneralBaseTest
from src.models import User
from werkzeug.security import generate_password_hash
from flask import get_flashed_messages, session, request
from flask_login import current_user

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

                expected1 = "[<Schedule: 1; Lane Goodwin Full>, <Schedule: 2; Triatlon>]"
                self.assertEqual(expected1, str(calculator.all_schedules))

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
                    "<Position: 101; 1>", str(calculator.next_position)
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
                self.assertIsNone(calculator.next_workout_best_time)

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

    def test_new_user_stats_are_correct(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })
                #  Check that schedule 1 is selected
                expected1 = b"""<option selected value="1" >Lane Goodwin Full </option>"""
                self.assertIn(expected1, response.data)

                expected2 = b"""id="user_workout_sessions_count">\n              0"""
                self.assertIn(expected2, response.data)

                expected3 = b"""No workouts done"""
                self.assertIn(expected3, response.data)

                # Next session with the title Core Strength should be seen
                expected4 = b'id="next-session">\n              \n                Core Strength'
                self.assertIn(expected4, response.data)

                # Season should be set to 1 at the very beginning
                expected5 = b"""id="season">\n              Season 1"""
                self.assertIn(expected5, response.data)

                # Week and they should be empty at the very beginning
                expected6 = b"""Week\n              \n            </h2>"""
                self.assertIn(expected6, response.data)

                expected7 = b"""Day\n              \n            </h2>"""
                self.assertIn(expected7, response.data)

    def test_user_can_add_workout_session(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                response = client.post(
                    "/stats/",
                    follow_redirects=True,
                    data={
                        "calendar": "1991/07/24",
                        "hours": 0,
                        "minutes": 24,
                        "seconds": 12,
                        "season_setup": "0"
                    })

                self.assertEqual(200, response.status_code)
                self.assertEqual(2, len(response.history))
                self.assertEqual("/stats/", response.request.path)

                expected2 = b"""id="user_workout_sessions_count">\n              1"""
                self.assertIn(expected2, response.data)

    def test_stats_are_correct_after_adding_workout_session(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                response = client.post(
                    "/stats/",
                    follow_redirects=True,
                    data={
                        "calendar": "1991/07/24",
                        "hours": 0,
                        "minutes": 24,
                        "seconds": 12,
                        "season_setup": "0"
                    })

                expected2 = b"""id="user_workout_sessions_count">\n              1"""
                self.assertIn(expected2, response.data)

                expected3 = b"""id="last-session-name">\n              \n                Core Strength"""
                self.assertIn(expected3, response.data)

                # Next session with the title Core Strength should be seen
                expected4 = b'id="next-session">\n              \n                Leg Strength'
                self.assertIn(expected4, response.data)

                # Season should be set to 1 at the very beginning
                expected5 = b"""id="season">\n              Season 1"""
                self.assertIn(expected5, response.data)

                # Week and they should be empty at the very beginning
                expected6 = b"""id="week">\n              \n                Week 1"""
                self.assertIn(expected6, response.data)

                expected7 = b"""id="day">\n              \n                Day 1"""
                self.assertIn(expected7, response.data)

                # Last session time should be now displayed as well
                expected8 = b"""id="last-session-time">\n                00:24:12"""
                self.assertIn(expected8, response.data)

    def test_switching_between_schedules(self):
        # Log the user, add one workout, then switch the schedule.
        # Check that the data are shown correctly
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                client.post(
                    "/stats/",
                    follow_redirects=True,
                    data={
                        "calendar": "1991/07/24",
                        "hours": 0,
                        "minutes": 24,
                        "seconds": 12,
                        "season_setup": "0"
                    })

                response = client.get(
                    "/stats/",
                    follow_redirects=True,
                    query_string={
                        "schedule_selector": 2
                    })

                expected1 = b"""<option selected value="2" >Triatlon </option>"""
                self.assertIn(expected1, response.data)

                expected2 = b"""id="user_workout_sessions_count">\n              0"""
                self.assertIn(expected2, response.data)

                expected3 = b"""No workouts done"""
                self.assertIn(expected3, response.data)

    def test_end_of_schedule_displays_correctly(self):
        # Add workout sessions until you reach the end of season
        # Check everything looks good at that stage
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                client.post(
                    "/stats/",
                    follow_redirects=True,
                    data={
                        "calendar": "1991/07/24",
                        "hours": 0,
                        "minutes": 24,
                        "seconds": 12,
                        "season_setup": "0"
                    })

                client.post(
                    "/stats/",
                    follow_redirects=True,
                    data={
                        "calendar": "1991/07/25",
                        "hours": 0,
                        "minutes": 20,
                        "seconds": 10,
                        "season_setup": "0"
                    })

                client.post(
                    "/stats/",
                    follow_redirects=True,
                    data={
                        "calendar": "1991/07/26",
                        "hours": 0,
                        "minutes": 15,
                        "seconds": 15,
                        "season_setup": "0"
                    })

                response = client.post(
                    "/stats/",
                    follow_redirects=True,
                    data={
                        "calendar": "1991/07/27",
                        "hours": 0,
                        "minutes": 7,
                        "seconds": 7,
                        "season_setup": "0"
                    })

                expected2 = b"""id="user_workout_sessions_count">\n              4"""
                self.assertIn(expected2, response.data)

                expected4 = b"""No more workouts. Start a new season"""
                self.assertIn(expected4, response.data)

                expected6 = b"""id="week">\n              \n                Week 1"""
                self.assertIn(expected6, response.data)

                expected7 = b"""id="day">\n              \n                Day 4"""
                self.assertIn(expected7, response.data)
