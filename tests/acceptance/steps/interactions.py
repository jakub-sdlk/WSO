from behave import *

from tests.acceptance.page_model.login_page import LoginPage
from tests.acceptance.page_model.signup_page import SignupPage

use_step_matcher('parse')


@when('I click on the "Register here" link')
def step_impl(context):
    page = LoginPage(context.driver)
    link = page.link_to_register
    link.click()


@when('I click on the "Log in here" link')
def step_impl(context):
    page = SignupPage(context.driver)
    link = page.link_to_login
    link.click()


