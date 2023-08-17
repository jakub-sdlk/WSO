from behave import *

from tests.acceptance.page_model.base_page import BasePage


use_step_matcher('parse')


@then('The h1 title has content "{p}"')
def step_impl(context, p):
    page = BasePage(context.driver)
    print(page.h1_title.text)
    print(p)
    assert page.h1_title.text == p


@then('The h2 subtitle has content "{p}"')
def step_impl(context, p):
    page = BasePage(context.driver)
    print(page.h2_subtitle.text)
    assert page.h2_subtitle.text == p