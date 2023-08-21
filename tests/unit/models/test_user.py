from src.models import Users
from tests.unit.unit_base_test import UnitBaseTest


# noinspection PyArgumentList
class UserTest(UnitBaseTest):
    def test_create_user(self):
        test = Users(
            first_name="John",
            last_name="Doe",
            email="John@Doe.com",
            password=1234)

        self.assertEqual(test.first_name, "John")
        self.assertEqual(test.last_name, "Doe")
        self.assertEqual(test.email, "John@Doe.com")
        self.assertEqual(test.password, 1234)

