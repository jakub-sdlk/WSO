from tests.general_base_test import GeneralBaseTest
from src.models import User, Schedule, Workout, Position, WorkoutSession
from werkzeug.security import generate_password_hash
from flask import get_flashed_messages, session, request
from flask_login import current_user

from src.stats.stats_calculator import Calculator


# noinspection PyArgumentList
class StatsTest(GeneralBaseTest):
    def setUp(self):
        #  create new test user every time
        super(StatsTest, self).setUp()  # making sure the General base test setup works as well
        with self.app() as client:
            with self.app_context():
                #  Create test user that will be logged in
                user1 = User(
                    first_name="John",
                    last_name="Doe",
                    email="John@Doe.com",
                    password=generate_password_hash("1234", method='sha256')
                )
                user1.save_to_db()

                # Create 2 test schedules

                schedule1 = Schedule(
                    name="Lane Goodwin Full"
                )
                schedule2 = Schedule(
                    name="Triatlon"
                )
                schedule1.save_to_db()
                schedule2.save_to_db()

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

                workout1.save_to_db()
                workout2.save_to_db()
                workout3.save_to_db()
                workout4.save_to_db()
                workout5.save_to_db()

                workout21.save_to_db()
                workout22.save_to_db()
                workout23.save_to_db()

                #  Create first 4 days of Lane Goodwin Full Schedule and 2 weeks of Triatlon schedule

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

                position101.save_to_db()
                position102.save_to_db()
                position103.save_to_db()
                position104.save_to_db()

                position201.save_to_db()
                position202.save_to_db()
                position203.save_to_db()
                position204.save_to_db()
                position205.save_to_db()
                position206.save_to_db()

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

    def test_all_schedules_variable(self):
        with self.app() as client:
            with self.app_context():
                all_schedules = Schedule.query.all()

                expected1 = "[<Schedule: 1; Lane Goodwin Full>, <Schedule: 2; Triatlon>]"
                self.assertEqual(expected1, str(all_schedules))

                #  Make sure you can loop through the all_schedules and get correct results
                expected2 = ("Lane Goodwin Full", "Triatlon")
                for count, schedule in enumerate(all_schedules):
                    self.assertEqual(count + 1, schedule.id)
                    self.assertEqual(expected2[count], schedule.name)

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

                active_schedule_id = int(session['active_schedule_id'])

                self.assertEqual(b'schedule_selector=1', response.request.query_string)
                self.assertEqual(1, active_schedule_id)

                response = client.get(
                    "/stats/",
                    follow_redirects=True,
                    query_string={
                        "schedule_selector": 2
                    })

                active_schedule_id = int(session['active_schedule_id'])

                self.assertEqual(b'schedule_selector=2', response.request.query_string)
                self.assertEqual(2, active_schedule_id)

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

    def test_time_variable(self):
        with self.app() as client:
            with self.app_context():
                pass

    def test_next_workout_variable(self):
        with self.app() as client:
            with self.app_context():
                pass

    def test_next_workout_best_time_session_variable(self):
        with self.app() as client:
            with self.app_context():
                pass

    def test_current_workout_session_season_variable(self):
        with self.app() as client:
            with self.app_context():
                pass

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

    def test_user_can_add_workout_session(self):
        pass

    def test_stats_are_correct_after_adding_workout_session(self):
        pass

    def test_switching_between_schedules(self):
        pass

    def test_end_of_schedule_displays_correctly(self):
        pass
