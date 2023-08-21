from src.models import Schedules
from tests.unit.unit_base_test import UnitBaseTest


class SchedulesTest(UnitBaseTest):
    def test_create_schedule(self):
        test = Schedules(
            name="Sample Schedule"
        )

        self.assertEqual(test.name, "Sample Schedule")

    def test_repr_method(self):
        test = Schedules(
            id=10,
            name="Sample Schedule"
        )
        expected = '<Schedule: 10; Sample Schedule>'
        self.assertEqual(expected, repr(test))