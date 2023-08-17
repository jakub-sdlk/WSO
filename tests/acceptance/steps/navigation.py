from behave import *
from selenium import webdriver

from tests.acceptance.page_model.login_page import LoginPage
from tests.acceptance.page_model.signup_page import SignupPage

use_step_matcher('re')


@given('I am on the login page')
def step_impl(context):
    context.driver = webdriver.Chrome()
    page = LoginPage(context.driver)
    context.driver.get(page.url)


@given('I am on the signup page')
def step_impl(context):
    context.driver = webdriver.Chrome()
    page = SignupPage(context.driver)
    context.driver.get(page.url)


@then('I am on the signup page')
def step_impl(context):
    page = SignupPage(context.driver)
    expected_url = page.url
    assert context.driver.current_url == expected_url


@then('I am on the login page')
def step_impl(context):
    page = LoginPage(context.driver)
    expected_url = page.url
    assert context.driver.current_url == expected_url
