"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from src import app
from src.db import db

from src.models import Users
from werkzeug.security import generate_password_hash


class GeneralBaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

    @classmethod
    def setUpClass(cls):
        # This code happens only once at the initialization of the test class
        app.config['SQLALCHEMY_DATABASE_URI'] = GeneralBaseTest.SQLALCHEMY_DATABASE_URI
        app.config['DEBUG'] = True
        app.config['TESTING'] = True

    def setUp(self):
        # Make sure database exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        #  Clear database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()
