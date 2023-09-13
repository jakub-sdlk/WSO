from src.models import Set
from tests.unit.unit_base_test import UnitBaseTest


class WorkoutTest(UnitBaseTest):
    def test_create_workout(self):
        test = Set(
            exercise_id=1,
            position_in_workout=1,
            number_of_reps=15
        )

        self.assertEqual(test.exercise_id, 1)
        self.assertEqual(test.position_in_workout, 1)
        self.assertEqual(test.number_of_reps, 15)

    def test_repr_method(self):
        test = Set(
            id=10,
            exercise_id=1,
            position_in_workout=1,
            number_of_reps=15
        )
        expected = "<Class: Set; Id: 10; ExerciseId: 1>"
        self.assertEqual(expected, repr(test))


