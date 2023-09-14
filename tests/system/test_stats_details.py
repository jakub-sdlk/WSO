from tests.general_base_test import GeneralBaseTest
from src.stats.database_generator import DatabaseGenerator
from src.models import WorkoutSession


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

    def test_new_user_stats_details_are_correct(self):
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

                expected1 = b"""id="set 16">\n            <span>Push Up"""
                self.assertIn(expected1, response.data)
                expected2 = b"""id="reps set 16">20</span>"""
                self.assertIn(expected2, response.data)

                expected3 = b"""id="set 17">\n            <span>Squat"""
                self.assertIn(expected3, response.data)
                expected4 = b"""id="reps set 17">40</span>"""
                self.assertIn(expected4, response.data)

                expected5 = b"""id="number-of-circles">5</span>"""
                self.assertIn(expected5, response.data)

    def test_stats_details_are_correct_after_adding_workout_session(self):
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

                expected1 = b"""id="set 1">\n            <span>Burpee"""
                self.assertIn(expected1, response.data)
                expected2 = b"""id="set 4">\n            <span>Lunge"""
                self.assertIn(expected2, response.data)

    def test_end_of_schedule_displays_stats_details_correctly(self):
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

                # Skip to the very end of the season - Position 147
                workout_session_1 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=1,
                    workout_id=4,
                    position_id=147,
                    schedule_id=1
                )
                workout_session_1.save_to_db()

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

                expected1 = b"""Sets in next workout"""
                self.assertNotIn(expected1, response.data)

                expected2 = b"""id="set"""
                self.assertNotIn(expected2, response.data)

