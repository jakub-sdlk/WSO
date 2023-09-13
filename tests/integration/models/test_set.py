from src.models import Set, Exercise
from tests.general_base_test import GeneralBaseTest


# noinspection PyArgumentList
class SetTest(GeneralBaseTest):
    def test_create_set(self):
        with self.app_context():
            set1 = Set(
                exercise_id=1,
                position_in_workout=1,
                number_of_reps=15
            )

            self.assertIsNone(Set.find_by_id(1))

            try:
                set1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(Set.find_by_id(1))
                self.assertEqual(1, Set.find_by_id(1).id)
                self.assertEqual(1, Set.find_by_id(1).exercise_id)
                self.assertEqual(1, Set.find_by_id(1).position_in_workout)
                self.assertEqual(15, Set.find_by_id(1).number_of_reps)

    def test_exercise_backref(self):
        with self.app_context():
            set1 = Set(
                exercise_id=1,
                position_in_workout=1,
                number_of_reps=15
            )

            exercise1 = Exercise(
                name="Burpee"
            )
            try:
                set1.save_to_db()
                exercise1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsInstance(set1.exercise, Exercise)
                self.assertEqual(1, set1.exercise.id)
                self.assertEqual("Burpee", set1.exercise.name)

