from src.models import Users
from tests.general_base_test import GeneralBaseTest
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class UserTest(GeneralBaseTest):
    def test_create_user(self):
        with self.app_context():
            test = Users("John", "Doe", "John@Doe.com", generate_password_hash("1234", method='sha256'))

            self.assertIsNone(Users.find_by_id(1))

            try:
                test.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(Users.find_by_id(1))
                self.assertEqual("John@Doe.com", Users.find_by_id(1).email)

                # check that date_created is added to the database automatically
                self.assertIsNotNone(Users.find_by_id(1).date_created)
                self.assertIsInstance(Users.find_by_id(1).date_created, datetime)

                # check that password is saved hashed
                self.assertIsNotNone(Users.find_by_id(1).password)
                self.assertIn("sha256$", Users.find_by_id(1).password)

    def test_create_multiple_users(self):
        with self.app_context():
            test1 = Users("John", "Doe", "John@Doe.com", generate_password_hash("1234", method='sha256'))
            test2 = Users("John", "Doe", "test@test.com", generate_password_hash("1234", method='sha256'))

            self.assertIsNone(Users.find_by_id(1))

            try:
                test1.save_to_db()
                test2.save_to_db()
            except Exception as e:
                self.assertIsNone(e)
            finally:
                self.assertIsNotNone(Users.find_by_id(1))
                self.assertEqual("John@Doe.com", Users.find_by_id(1).email)
                self.assertIsNotNone(Users.find_by_id(2))
                self.assertEqual("test@test.com", Users.find_by_id(2).email)
                self.assertEqual(2, Users.count_all())

    def test_user_email_is_unique(self):
        with self.app_context():
            test1 = Users("John", "Doe", "John@Doe.com", generate_password_hash("1234", method='sha256'))
            test2 = Users("John", "Doe", "John@Doe.com", generate_password_hash("1234", method='sha256'))

            try:
                test1.save_to_db()
                test2.save_to_db()
            except Exception as e:
                self.assertIn("(sqlite3.IntegrityError)", e.__str__())
            finally:
                with self.app_context():
                    self.assertIsNotNone(Users.find_by_id(1))
                    self.assertIsNone(Users.find_by_id(2))
                    self.assertEqual(1, Users.find_by_email("John@Doe.com").id)
                    self.assertEqual(1, Users.count_all())
