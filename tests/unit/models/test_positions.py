from src.models import Position
from tests.unit.unit_base_test import UnitBaseTest


class PositionTest(UnitBaseTest):
    def test_create_position(self):
        test = Position(
            workout_id=5,
            week=1,
            day=1
        )

        self.assertEqual(test.workout_id, 5)
        self.assertEqual(test.week, 1)
        self.assertEqual(test.day, 1)

    def test_repr_method(self):
        test = Position(
            id=101,
            workout_id=5,
            week=1,
            day=1
        )
        expected = '<Position: 101; 5>'
        self.assertEqual(expected, repr(test))