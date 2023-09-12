from tests.general_base_test import GeneralBaseTest
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
