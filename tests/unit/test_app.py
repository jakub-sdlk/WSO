from tests.unit.unit_base_test import UnitBaseTest, app


class AppTest(UnitBaseTest):
    def test_app_config(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(len(app.secret_key) > 10)

