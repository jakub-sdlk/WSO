from src.models import WorkoutSessions
from tests.unit.unit_base_test import UnitBaseTest


# noinspection PyArgumentList
class WorkoutSessionsTest(UnitBaseTest):
    def test_create_workout_session(self):
        test = WorkoutSessions(
            date="1991/07/24",
            hours=1,
            minutes=30,
            seconds=20,
            season=1,
            user_id=1,
            workout_id=5,
            position_id=1,
            schedule_id=4
        )

        self.assertEqual(test.date, "1991/07/24")
        self.assertEqual(test.hours, 1)
        self.assertEqual(test.minutes, 30)
        self.assertEqual(test.seconds, 20)
        self.assertEqual(test.season, 1)
        self.assertEqual(test.user_id, 1)
        self.assertEqual(test.workout_id, 5)
        self.assertEqual(test.position_id, 1)
        self.assertEqual(test.schedule_id, 4)

    def test_repr_method(self):
        test = WorkoutSessions(
            id=10,
            date="1991/07/24",
            hours=1,
            minutes=30,
            seconds=20,
            season=1,
            user_id=1,
            workout_id=5,
            position_id=1,
            schedule_id=4
        )
        expected = '<WorkoutSession: 10; 5>'
        self.assertEqual(expected, repr(test))