from src.models import Schedule
from tests.unit.unit_base_test import UnitBaseTest


class ScheduleTest(UnitBaseTest):
    def test_create_schedule(self):
        test = Schedule(
            name="Sample Schedule"
        )

        self.assertEqual(test.name, "Sample Schedule")

    def test_repr_method(self):
        test = Schedule(
            id=10,
            name="Sample Schedule"
        )
        expected = '<Schedule: 10; Sample Schedule>'
        self.assertEqual(expected, repr(test))