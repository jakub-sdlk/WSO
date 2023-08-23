from tests.general_base_test import GeneralBaseTest
from src.models import User
from werkzeug.security import generate_password_hash
from flask import get_flashed_messages


class AuthTest(GeneralBaseTest):
    def test_login_page_get_method(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("auth/login")

                self.assertEqual(200, response.status_code)

                self.assertIn(b"Log into your account", response.data)
                self.assertIn(b"login_email", response.data)
                self.assertIn(b"login_password", response.data)

    def test_login_user(self):
        with self.app() as client:
            with self.app_context():
                user1 = User(
                    first_name="John",
                    last_name="Doe",
                    email="John@Doe.com",
                    password=generate_password_hash("1234", method='sha256')
                )

                user1.save_to_db()

                response = client.post(
                    "auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(200, response.status_code)

                for category, message in messages:
                    self.assertEqual('success', category),
                    self.assertEqual("Logged in!", message)

                self.assertEqual(1, len(response.history))
                self.assertEqual("/stats/", response.request.path)
                self.assertIn(b"User:+1;+John@Doe.com", response.request.query_string)

    def test_login_user_incorrect_password(self):
        with self.app() as client:
            with self.app_context():
                user1 = User(
                    first_name="John",
                    last_name="Doe",
                    email="John@Doe.com",
                    password=generate_password_hash("1234", method='sha256')
                )

                user1.save_to_db()

                response = client.post(
                    "auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 12345678
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("Incorrect password", message)

                self.assertEqual("/auth/login", response.request.path)

    def test_login_non_existing_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("Email does not exist", message)

                self.assertEqual("/auth/login", response.request.path)

    def test_signup_page_get_method(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("auth/signup")

                self.assertEqual(200, response.status_code)

                self.assertIn(b"Join us today!", response.data)
                self.assertIn(b"signup_email", response.data)
                self.assertIn(b"signup_password", response.data)

    def test_signup_new_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "auth/signup",
                    follow_redirects=True,
                    data={
                        "signup_first_name": "John",
                        "signup_last_name": "Doe",
                        "signup_email": "John@Doe.com",
                        "signup_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(200, response.status_code)

                for category, message in messages:
                    self.assertEqual('success', category),
                    self.assertEqual("User created", message)

                self.assertEqual(1, User.find_by_email("John@Doe.com").id)

                self.assertEqual(1, len(response.history))
                self.assertEqual("/stats/", response.request.path)
                self.assertIn(b"User:+1;+John@Doe.com", response.request.query_string)

    def test_signup_existing_user(self):
        with self.app() as client:
            with self.app_context():
                user1 = User(
                    first_name="John",
                    last_name="Doe",
                    email="John@Doe.com",
                    password=generate_password_hash("1234", method='sha256')
                )
                user1.save_to_db()

                response = client.post(
                    "auth/signup",
                    follow_redirects=True,
                    data={
                        "signup_first_name": "John",
                        "signup_last_name": "Doe",
                        "signup_email": "John@Doe.com",
                        "signup_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("This email is already registered.", message)

                self.assertEqual("/auth/signup", response.request.path)
                self.assertNotIn(b"User:+1;+John@Doe.com", response.request.query_string)

    def test_signup_empty_first_name(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "auth/signup",
                    follow_redirects=True,
                    data={
                        "signup_first_name": "",
                        "signup_last_name": "Doe",
                        "signup_email": "John@Doe.com",
                        "signup_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("First name is required.", message)

                self.assertEqual(0, len(response.history))


    def test_signup_empty_last_name(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "auth/signup",
                    follow_redirects=True,
                    data={
                        "signup_first_name": "John",
                        "signup_last_name": "",
                        "signup_email": "John@Doe.com",
                        "signup_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("Last name is required.", message)

                self.assertEqual(0, len(response.history))

    def test_signup_empty_email(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "auth/signup",
                    follow_redirects=True,
                    data={
                        "signup_first_name": "John",
                        "signup_last_name": "Doe",
                        "signup_email": "",
                        "signup_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("Email is invalid.", message)

                self.assertEqual(0, len(response.history))

    def test_signup_invalid_email(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "auth/signup",
                    follow_redirects=True,
                    data={
                        "signup_first_name": "John",
                        "signup_last_name": "Doe",
                        "signup_email": "test",
                        "signup_password": 1234
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("Email is invalid.", message)

                self.assertEqual(0, len(response.history))

    def test_signup_empty_password(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "auth/signup",
                    follow_redirects=True,
                    data={
                        "signup_first_name": "John",
                        "signup_last_name": "Doe",
                        "signup_email": "John@Doe.com",
                        "signup_password": ""
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("Invalid password.", message)

                self.assertEqual(0, len(response.history))

    def test_signup_invalid_password(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "auth/signup",
                    follow_redirects=True,
                    data={
                        "signup_first_name": "John",
                        "signup_last_name": "Doe",
                        "signup_email": "John@Doe.com",
                        "signup_password": 12
                    })

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("Invalid password.", message)

                self.assertEqual(0, len(response.history))

