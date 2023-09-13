from src.models import Exercise, Set
from tests.general_base_test import GeneralBaseTest


# noinspection PyArgumentList
class ExerciseTest(GeneralBaseTest):
    def test_create_exercise(self):
        with self.app_context():
            exercise1 = Exercise(
                name="Burpee"
            )

            self.assertIsNone(Exercise.find_by_id(1))

            try:
                exercise1.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(Exercise.find_by_id(1))
                self.assertEqual(1, Exercise.find_by_id(1).id)
                self.assertEqual("Burpee", Exercise.find_by_id(1).name)

    def test_set_relationship(self):
        with self.app_context():
            exercise1 = Exercise(
                name="Burpee"
            )
            exercise2 = Exercise(
                name="Push up"
            )

            set1 = Set(
            exercise_id=1,
            position_in_workout=1,
            number_of_reps=15
            )

            set2 = Set(
                exercise_id=2,
                position_in_workout=2,
                number_of_reps=10
            )

            set3 = Set(
                exercise_id=1,
                position_in_workout=3,
                number_of_reps=5
            )

            try:
                exercise1.save_to_db()
                exercise2.save_to_db()
                set1.save_to_db()
                set2.save_to_db()
                set3.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsInstance(exercise1.sets[0], Set)
                self.assertEqual(2, len(exercise1.sets))

                self.assertEqual(1, exercise1.sets[0].id)
                self.assertEqual(2, exercise2.sets[0].id)

                self.assertEqual(3, exercise1.sets[1].position_in_workout)
                self.assertEqual(10, exercise2.sets[0].number_of_reps)

