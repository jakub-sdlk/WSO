from src.models import Workout
from tests.unit.unit_base_test import UnitBaseTest


class WorkoutTest(UnitBaseTest):
    def test_create_workout(self):
        test = Workout(
            name="Sample Workout",
            number_of_circles=3
        )

        self.assertEqual(test.name, "Sample Workout")
        self.assertEqual(test.number_of_circles, 3)

    def test_repr_method(self):
        test = Workout(
            id=10,
            name="Sample Workout",
            number_of_circles=3
        )
        expected = "<Class: Workout; Id: 10; Name: Sample Workout>"
        self.assertEqual(expected, repr(test))


