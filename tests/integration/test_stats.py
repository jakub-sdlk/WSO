from werkzeug.security import generate_password_hash
from flask import get_flashed_messages
from flask_login import current_user

from tests.general_base_test import GeneralBaseTest

from src.models import User, WorkoutSession
from src.stats.stats_calculator import Calculator
from src.database_generator import DatabaseGenerator


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
                    DatabaseGenerator.create_second_verified_test_user()

                    client.post(
                        "/auth/login",
                        follow_redirects=True,
                        data={
                            "login_email": "test@test.com",
                            "login_password": 1234
                        })

                    self.assertEqual("test@test.com", current_user.email)
                    self.assertEqual("Test", current_user.first_name)

    def test_active_schedule_id_attribute(self):
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

    def test_all_schedules_attribute(self):
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

                expected1 = "[<Class: Schedule; Id: 1; Name: LG Workout>, <Class: Schedule; Id: 2; Name: " \
                            "Triatlon>]"
                self.assertEqual(expected1, repr(calculator.all_schedules))

                #  Make sure you can loop through the all_schedules and get correct results
                expected2 = ("LG Workout", "Triatlon")
                for count, schedule in enumerate(calculator.all_schedules):
                    self.assertEqual(count + 1, schedule.id)
                    self.assertEqual(expected2[count], schedule.name)

    def test_all_workouts_in_active_schedule_attribute(self):
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

                self.assertEqual(10, len(calculator.all_workouts_in_active_schedule))
                expected1 = "<Class: Workout; Id: 1; Name: Core Strength>"
                self.assertEqual(expected1, str(calculator.all_workouts_in_active_schedule[0]))
                expected2 = "<Class: Workout; Id: 10; Name: Core Skills>"
                self.assertEqual(expected2, str(calculator.all_workouts_in_active_schedule[-1]))

                # When switching to another schedule, this list should change

                client.get(
                    "/stats/",
                    follow_redirects=True,
                    query_string={
                        "schedule_selector": 2
                    })

                calculator = Calculator()

                self.assertEqual(3, len(calculator.all_workouts_in_active_schedule))
                expected1 = "<Class: Workout; Id: 21; Name: Běh 3km>"
                self.assertEqual(expected1, str(calculator.all_workouts_in_active_schedule[0]))
                expected2 = "<Class: Workout; Id: 23; Name: Plavání 2km>"
                self.assertEqual(expected2, str(calculator.all_workouts_in_active_schedule[-1]))

    def test_all_workout_sessions_attribute(self):
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

    def test_user_workout_sessions_count_attribute(self):
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

    def test_position_id_attribute(self):
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

    def test_next_position_attribute(self):
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

    def test_next_workout_best_time_attribute(self):
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

    def test_current_workout_session_season_attribute(self):
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

    def test_sets_in_next_workout_attribute(self):
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

                # When first loaded, the sets for Frontal Strength should be available
                self.assertIsNotNone(calculator.sets_in_next_workout)
                self.assertEqual(4, len(calculator.sets_in_next_workout))

                self.assertEqual("<Class: Set; Id: 16; ExerciseId: 3>", str(calculator.sets_in_next_workout[0]))
                self.assertEqual(2, calculator.sets_in_next_workout[1].position_in_workout)
                self.assertEqual(3, calculator.sets_in_next_workout[2].exercise_id)
                self.assertEqual(18, calculator.sets_in_next_workout[-1].id)

                # Workout can consist of different number of sets. Next workout should be Leg Skills with 3 sets only
                workout_session_1 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=1,
                    workout_id=4,
                    position_id=106,
                    schedule_id=1
                )

                workout_session_1.save_to_db()

                calculator = Calculator()
                self.assertEqual(3, len(calculator.sets_in_next_workout))

                # At the very end of the season, no sets_in_next_workout should return None
                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=30,
                    seconds=20,
                    season=1,
                    user_id=1,
                    workout_id=5,
                    position_id=148,
                    schedule_id=1
                )

                workout_session_2.save_to_db()

                calculator = Calculator()
                self.assertIsNone(calculator.sets_in_next_workout)

    def test_best_workout_times_attribute(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                # New user should not see the list, the best_workout_times is set to None
                calculator = Calculator()
                self.assertIsNone(calculator.best_workout_times)

                # After adding two workout session, their times should be displayed
                workout_session_1 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=1,
                    seconds=1,
                    season=1,
                    user_id=1,
                    workout_id=5,
                    position_id=101,
                    schedule_id=1
                )

                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=15,
                    seconds=15,
                    season=1,
                    user_id=1,
                    workout_id=1,
                    position_id=102,
                    schedule_id=1
                )
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()

                calculator = Calculator()
                self.assertIsNotNone(calculator.best_workout_times)
                self.assertIsInstance(calculator.best_workout_times[0], WorkoutSession)
                self.assertEqual(2, len(calculator.best_workout_times))

                self.assertEqual(2, calculator.best_workout_times[0].id)
                self.assertEqual(1, calculator.best_workout_times[0].hours)
                self.assertEqual(15, calculator.best_workout_times[0].minutes)
                self.assertEqual(15, calculator.best_workout_times[0].seconds)

                self.assertEqual(1, calculator.best_workout_times[1].id)

                # After adding same workouts in different season with worse time,
                # The best times should stay the same

                workout_session_3 = WorkoutSession(
                    date="1991/07/24",
                    hours=2,
                    minutes=59,
                    seconds=59,
                    season=2,
                    user_id=1,
                    workout_id=5,
                    position_id=101,
                    schedule_id=1
                )

                workout_session_4 = WorkoutSession(
                    date="1991/07/24",
                    hours=2,
                    minutes=59,
                    seconds=59,
                    season=2,
                    user_id=1,
                    workout_id=1,
                    position_id=102,
                    schedule_id=1
                )
                workout_session_3.save_to_db()
                workout_session_4.save_to_db()

                calculator = Calculator()
                self.assertEqual(2, len(calculator.best_workout_times))

                self.assertEqual(2, calculator.best_workout_times[0].id)
                self.assertEqual(1, calculator.best_workout_times[0].hours)
                self.assertEqual(1, calculator.best_workout_times[1].id)

    def test_next_workout_all_workout_sessions_attribute(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234,
                    })

                # New user should not see the list - There are no sessions to show
                calculator = Calculator()
                self.assertIsNone(calculator.next_workout_all_workout_sessions)

                # After adding workout sessions to positions 101 and 107, next workout should be Frontal Strength
                # The correct data for the last session of Frontal Strength should be shown
                workout_session_1 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=24,
                    seconds=48,
                    season=1,
                    user_id=1,
                    workout_id=5,
                    position_id=101,
                    schedule_id=1
                )

                workout_session_2 = WorkoutSession(
                    date="1991/07/24",
                    hours=1,
                    minutes=15,
                    seconds=15,
                    season=1,
                    user_id=1,
                    workout_id=7,
                    position_id=107,
                    schedule_id=1
                )
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()

                calculator = Calculator()
                self.assertIsNotNone(calculator.next_workout_all_workout_sessions)
                self.assertIsInstance(calculator.next_workout_all_workout_sessions[0], WorkoutSession)
                self.assertEqual(1, len(calculator.next_workout_all_workout_sessions))

                self.assertEqual(1, calculator.next_workout_all_workout_sessions[0].id)
                self.assertEqual(1, calculator.next_workout_all_workout_sessions[0].season)
                self.assertEqual(1, calculator.next_workout_all_workout_sessions[0].hours)
                self.assertEqual(24, calculator.next_workout_all_workout_sessions[0].minutes)
                self.assertEqual(48, calculator.next_workout_all_workout_sessions[0].seconds)

                # The progress should span different seasons - The oldest season is on top

                workout_session_3 = WorkoutSession(
                    date="1991/07/24",
                    hours=2,
                    minutes=59,
                    seconds=59,
                    season=2,
                    user_id=1,
                    workout_id=5,
                    position_id=101,
                    schedule_id=1
                )

                workout_session_4 = WorkoutSession(
                    date="1991/07/24",
                    hours=2,
                    minutes=22,
                    seconds=44,
                    season=2,
                    user_id=1,
                    workout_id=7,
                    position_id=107,
                    schedule_id=1
                )
                workout_session_3.save_to_db()
                workout_session_4.save_to_db()

                calculator = Calculator()
                self.assertEqual(2, len(calculator.next_workout_all_workout_sessions))

                self.assertEqual(3, calculator.next_workout_all_workout_sessions[1].id)
                self.assertEqual(2, calculator.next_workout_all_workout_sessions[1].season)
                self.assertEqual(2, calculator.next_workout_all_workout_sessions[1].hours)
                self.assertEqual(59, calculator.next_workout_all_workout_sessions[1].minutes)
                self.assertEqual(59, calculator.next_workout_all_workout_sessions[1].seconds)

                # Workouts of other users should not be seen

                workout_session_5 = WorkoutSession(
                    date="1991/07/24",
                    hours=0,
                    minutes=32,
                    seconds=32,
                    season=1,
                    user_id=2,
                    workout_id=5,
                    position_id=101,
                    schedule_id=1
                )
                workout_session_6 = WorkoutSession(
                    date="1991/07/24",
                    hours=2,
                    minutes=22,
                    seconds=44,
                    season=2,
                    user_id=1,
                    workout_id=7,
                    position_id=107,
                    schedule_id=1
                )

                workout_session_5.save_to_db()
                workout_session_6.save_to_db()

                calculator = Calculator()
                self.assertEqual(2, len(calculator.next_workout_all_workout_sessions))

                # Let's add one more workout session of Frontal Strength and skip to position 112, so that next
                # Workout should be Frontal Strength again.
                # We should see id of workout sessions in next_workout_all_workouts in following order:
                # id 1, id 3, id 7 - Not id 5, that one belongs to different user

                workout_session_7 = WorkoutSession(
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
                workout_session_8 = WorkoutSession(
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

                workout_session_7.save_to_db()
                workout_session_8.save_to_db()

                calculator = Calculator()
                self.assertEqual(3, len(calculator.next_workout_all_workout_sessions))
                self.assertEqual(1, calculator.next_workout_all_workout_sessions[0].id)
                self.assertEqual(3, calculator.next_workout_all_workout_sessions[1].id)
                self.assertEqual(7, calculator.next_workout_all_workout_sessions[2].id)
