from tests.general_base_test import GeneralBaseTest
from src.models import User
from werkzeug.security import generate_password_hash
from flask import get_flashed_messages
from flask_login import current_user


class StatsTest(GeneralBaseTest):
    def setUp(self):
        #  create new test user every time
        super(StatsTest, self).setUp()  # making sure the General base test setup works as well
        with self.app() as client:
            with self.app_context():
                user1 = User(
                    first_name="John",
                    last_name="Doe",
                    email="John@Doe.com",
                    password=generate_password_hash("1234", method='sha256')
                )
                user1.save_to_db()

    def test_logged_user_can_refresh_page(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })

                response = client.get(
                    "/stats/",
                    follow_redirects=True,
                )

                self.assertEqual(200, response.status_code)
                self.assertEqual(0, len(response.history))
                self.assertEqual("/stats/", response.request.path)
                self.assertIn(b"Overview", response.data)
                self.assertEqual("John@Doe.com", current_user.email)

    def test_log_out_logged_user(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/login",
                    follow_redirects=True,
                    data={
                        "login_email": "John@Doe.com",
                        "login_password": 1234
                    })
                response = client.get(
                    "/auth/logout",
                    follow_redirects=True
                )

                self.assertEqual(200, response.status_code)
                self.assertEqual(1, len(response.history))
                self.assertEqual("/auth/login", response.request.path)
                self.assertIn(b"Log into your account", response.data)

    def test_log_in_is_required(self):
        with self.app() as client:
            with self.app_context():
                response = client.get(
                    "/stats/",
                    follow_redirects=True
                )

                self.assertEqual(200, response.status_code)
                self.assertEqual(1, len(response.history))
                self.assertEqual("/auth/login", response.request.path)
                self.assertIn(b"Log into your account", response.data)
                self.assertIn(b'next=%2Fstats%2F', response.request.query_string)
