from behave import *
from selenium.webdriver.support.wait import WebDriverWait

use_step_matcher('re')


@given('I wait for bootstrap to load')
def step_impl(context):
    WebDriverWait(context.driver, 2)