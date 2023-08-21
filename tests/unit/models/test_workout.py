from src.models import Workouts
from tests.unit.unit_base_test import UnitBaseTest


class WorkoutsTest(UnitBaseTest):
    def test_create_workout(self):
        test = Workouts(
            name="Sample Workout",
            number_of_circles=3
        )

        self.assertEqual(test.name, "Sample Workout")
        self.assertEqual(test.number_of_circles, 3)

    def test_repr_method(self):
        test = Workouts(
            id=10,
            name="Sample Workout",
            number_of_circles=3
        )
        expected = '<Workout: 10; Sample Workout>'
        self.assertEqual(expected, repr(test))