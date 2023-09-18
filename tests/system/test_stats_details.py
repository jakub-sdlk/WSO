from tests.general_base_test import GeneralBaseTest
from src.database_generator import DatabaseGenerator
from src.models import WorkoutSession


# noinspection PyArgumentList
class StatsTest(GeneralBaseTest):
    def setUp(self):
        #  create new test user every time
        super(StatsTest, self).setUp()  # making sure the General base test setup works as well
        with self.app() as client:
            with self.app_context():
                #  Create test user that will be logged in
                DatabaseGenerator.create_verified_test_user()

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

                # Check that sets in next workout works
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

                # Check that best workout times work - New user should see only the table name
                expected6 = b"""Best workout times"""
                self.assertIn(expected6, response.data)

                expected7 = b"""id="best-workout-"""
                self.assertNotIn(expected7, response.data)

                # Check that next workout progress works. New user should see only the table name
                expected8 = b"""Next workout progress"""
                self.assertIn(expected8, response.data)

                expected9 = b"""id="progress-session-id-"""
                self.assertNotIn(expected9, response.data)

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

                # Check that sets in next workout works
                expected1 = b"""id="set 1">\n            <span>Burpee"""
                self.assertIn(expected1, response.data)

                expected2 = b"""id="set 4">\n            <span>Lunge"""
                self.assertIn(expected2, response.data)

                # Check that best workout times work - user now should see the table and data in it
                expected3 = b"""Best workout times"""
                self.assertIn(expected3, response.data)

                expected4 = b"""id="best-workout-Frontal Strength"""
                self.assertIn(expected4, response.data)

                expected4 = b"""id="best-time-of-Frontal Strength">\n              00:24:12"""
                self.assertIn(expected4, response.data)

                # Let's add one more workout session of Frontal Strength and skip to position 112, so that next
                # Workout should be Frontal Strength again.

                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=11,
                    minutes=11,
                    seconds=11,
                    season=2,
                    user_id=1,
                    workout_id=5,
                    position_id=108,
                    schedule_id=1
                )
                workout_session_3 = WorkoutSession(
                    date="1991/07/24",
                    hours=5,
                    minutes=52,
                    seconds=52,
                    season=2,
                    user_id=1,
                    workout_id=2,
                    position_id=112,
                    schedule_id=1
                )
                workout_session_2.save_to_db()
                workout_session_3.save_to_db()

                response = client.get(
                    "/stats/",
                    follow_redirects=True
                )

                # Check that Next workout progress works - user now should see the progress of two previous
                # Frontal Strength sessions

                expected5 = b"""id="progress-session-id-1"""
                self.assertIn(expected5, response.data)

                expected6 = b"""id="progress-session-time-1">\n              00:24:12"""
                self.assertIn(expected6, response.data)

                expected7 = b"""id="progress-session-id-2"""
                self.assertIn(expected7, response.data)

                expected8 = b"""id="progress-session-time-2">\n              11:11:11"""
                self.assertIn(expected8, response.data)



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
                # Check that sets in next workout works - User should see only the table name at the end of the season
                expected1 = b"""Sets in next workout"""
                self.assertIn(expected1, response.data)

                expected2 = b"""id="set"""
                self.assertNotIn(expected2, response.data)

                # Check that best workout times work - user now should see best times of two workouts
                expected3 = b"""id="best-workout-Frontal Strength"""
                self.assertIn(expected3, response.data)

                expected4 = b"""id="best-time-of-Frontal Strength">\n              00:07:07"""
                self.assertIn(expected4, response.data)

                expected5 = b"""id="best-workout-V-Taper">V-Taper"""
                self.assertIn(expected5, response.data)

                expected6 = b"""id="best-time-of-V-Taper">\n              01:30:20"""
                self.assertIn(expected6, response.data)

                # Check that next workout progress works. New user should see only the table name
                expected7 = b"""Next workout progress"""
                self.assertIn(expected7, response.data)

                expected8 = b"""id="progress-session-id-"""
                self.assertNotIn(expected8, response.data)



