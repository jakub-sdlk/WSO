from tests.general_base_test import GeneralBaseTest
from src.models import User, Schedule, Workout, Position
from werkzeug.security import generate_password_hash
from flask import get_flashed_messages
from flask_login import current_user


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
                self.assertEqual("John@Doe.com", current_user.email)

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
