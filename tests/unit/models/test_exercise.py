from src.models import Exercise
from tests.unit.unit_base_test import UnitBaseTest


class ExerciseTest(UnitBaseTest):
    def test_create_workout(self):
        test = Exercise(
            name="Burpee"
        )

        self.assertEqual(test.name, "Burpee")

    def test_repr_method(self):
        test = Exercise(
            id=10,
            name="Burpee",
        )
        expected = "<Class: Exercise; Id: 10; Name: Burpee>"
        self.assertEqual(expected, repr(test))


