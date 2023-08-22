from src.models import User
from tests.unit.unit_base_test import UnitBaseTest


# noinspection PyArgumentList
class UserTest(UnitBaseTest):
    def test_create_user(self):
        test = User(
            first_name="John",
            last_name="Doe",
            email="John@Doe.com",
            password=1234)

        self.assertEqual(test.first_name, "John")
        self.assertEqual(test.last_name, "Doe")
        self.assertEqual(test.email, "John@Doe.com")
        self.assertEqual(test.password, 1234)

    def test_repr_method(self):
        test = User(
            id=10,
            first_name="John",
            last_name="Doe",
            email="John@Doe.com",
            password=1234)

        expected = '<User: 10; John@Doe.com>'
        self.assertEqual(expected, repr(test))