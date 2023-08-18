from src.models import Users
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = Users("John", "Doe", "John@Doe.com", 1234)

        self.assertEqual("John", user.first_name)
        self.assertEqual("Doe", user.last_name)
        self.assertEqual("John@Doe.com", user.email)
        self.assertEqual(1234, user.password)