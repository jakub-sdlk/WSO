from tests.general_base_test import GeneralBaseTest


class AuthTest(GeneralBaseTest):
    def test_login_page_get_method(self):
        with self.app() as client:
            with self.app_context():
                get_request = client.get("auth/login")

                self.assertEqual(200, get_request.status_code)

                self.assertIn(b"Log into your account", get_request.data)
                self.assertIn(b"login_email", get_request.data)
                self.assertIn(b"login_password", get_request.data)

    def test_signup_page_get_method(self):
        with self.app() as client:
            with self.app_context():
                get_request = client.get("auth/signup")

                self.assertEqual(200, get_request.status_code)

                self.assertIn(b"Join us today!", get_request.data)
                self.assertIn(b"signup_email", get_request.data)
                self.assertIn(b"signup_password", get_request.data)
