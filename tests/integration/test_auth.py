from flask import get_flashed_messages
from flask_login import current_user
import jwt

from tests.general_base_test import GeneralBaseTest
from package.models import User
from package.database_generator import DatabaseGenerator
from package.config import SECRET_KEY


class AuthTest(GeneralBaseTest):
    def test_login_page_get_method(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("auth/login")

                self.assertEqual(200, response.status_code)

                self.assertIn(b"Log into your account", response.data)
                self.assertIn(b"login_email", response.data)
                self.assertIn(b"login_password", response.data)

    def test_login_verified_user(self):
        with self.app() as client:
            with self.app_context():
                DatabaseGenerator.create_verified_test_user()

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
                self.assertEqual("John@Doe.com", current_user.email)
                self.assertEqual(b'schedule_selector=1', response.request.query_string)

    def test_login_unverified_user(self):
        with self.app() as client:
            with self.app_context():
                DatabaseGenerator.create_unverified_test_user()

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
                    self.assertEqual("User is not verified", message)

                self.assertEqual(0, len(response.history))
                self.assertEqual("/auth/login", response.request.path)

    def test_login_verified_user_incorrect_password(self):
        with self.app() as client:
            with self.app_context():
                DatabaseGenerator.create_verified_test_user()

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

    def test_signup_page_login_required(self):
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

                self.assertEqual(0, len(response.history))
                self.assertEqual("/auth/signup", response.request.path)
                self.assertIn(b"""Verification email was sent to John@Doe.com.""", response.data)

    def test_signup_existing_user(self):
        with self.app() as client:
            with self.app_context():
                DatabaseGenerator.create_verified_test_user()

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

    def test_verify_email_valid_key(self):
        with self.app() as client:
            with self.app_context():
                user1 = DatabaseGenerator.create_unverified_test_user()

                token = jwt.encode(
                    {
                        "email_address": user1.email ,
                        "password": user1.password,
                    }, SECRET_KEY
                )

                response = client.get(f"auth/verify-email/{token}",
                                      follow_redirects=True)

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(200, response.status_code)
                self.assertEqual(1, len(response.history))

                for category, message in messages:
                    self.assertEqual('success', category),
                    self.assertEqual("Logged in!", message)

                self.assertEqual("/stats/", response.request.path)
                self.assertIn(b"Overview", response.data)

    def test_verify_email_invalid_key(self):
        with self.app() as client:
            with self.app_context():
                user1 = DatabaseGenerator.create_unverified_test_user()

                token = jwt.encode(
                    {
                        "email_address": user1.email,
                        "password": 1234,
                    }, SECRET_KEY
                )

                response = client.get(f"auth/verify-email/{token}",
                                      follow_redirects=True)

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)
                self.assertEqual(1, len(response.history))

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("Invalid verification token", message)

                self.assertEqual("/auth/login", response.request.path)

    def test_verify_email_already_verified_user(self):
        with self.app() as client:
            with self.app_context():
                user1 = DatabaseGenerator.create_verified_test_user()

                token = jwt.encode(
                    {
                        "email_address": user1.email,
                        "password": user1.password,
                    }, SECRET_KEY
                )

                response = client.get(f"auth/verify-email/{token}",
                                      follow_redirects=True)

                messages = get_flashed_messages(with_categories=True)

                self.assertEqual(401, response.status_code)
                self.assertEqual(1, len(response.history))

                for category, message in messages:
                    self.assertEqual('error', category),
                    self.assertEqual("User is already verified", message)

                self.assertEqual("/auth/login", response.request.path)