from src.models import Schedule, WorkoutSession
from tests.general_base_test import GeneralBaseTest


# noinspection PyArgumentList
class ScheduleTest(GeneralBaseTest):
    def test_create_schedule(self):
        with self.app_context():
            schedule1 = Schedule(
                name="Lane Goodwin Full"
            )

            self.assertIsNone(Schedule.find_by_id(1))

            try:
                schedule1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(Schedule.find_by_id(1))
                self.assertEqual(1, Schedule.find_by_id(1).id)
                self.assertEqual("Lane Goodwin Full", Schedule.find_by_id(1).name)

    def test_workout_session_relationship(self):
        with self.app_context():
            schedule1 = Schedule(
                name="Lane Goodwin Full"
            )

            schedule2 = Schedule(
                name="Triatlon"
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

            workout_session_2 = WorkoutSession(
                date="2022/02/02",
                hours=1,
                minutes=30,
                seconds=20,
                season=1,
                user_id=1,
                workout_id=5,
                position_id=102,
                schedule_id=1
            )

            workout_session_3 = WorkoutSession(
                date="2000/12/24",
                hours=1,
                minutes=30,
                seconds=20,
                season=1,
                user_id=1,
                workout_id=3,
                position_id=201,
                schedule_id=2
            )
            try:
                schedule1.save_to_db()
                schedule2.save_to_db()
                workout_session_1.save_to_db()
                workout_session_2.save_to_db()
                workout_session_3.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsInstance(schedule1.workout_sessions[0], WorkoutSession)
                self.assertEqual(2, len(schedule1.workout_sessions))

                self.assertEqual(1, schedule1.workout_sessions[0].id)
                self.assertEqual(3, schedule2.workout_sessions[0].id)

                self.assertEqual("1991/07/24", schedule1.workout_sessions[0].date)
                self.assertEqual(201, schedule2.workout_sessions[0].position_id)

