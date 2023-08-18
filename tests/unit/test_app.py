from tests.unit.unit_base_test import UnitBaseTest, app


class AppTest(UnitBaseTest):
    def test_app_config(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
