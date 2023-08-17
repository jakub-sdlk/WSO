from tests.acceptance.locators.signup_page import SignupPageLocators
from tests.acceptance.page_model.base_page import BasePage


class SignupPage(BasePage):
    @property
    def url(self):
        return super().url + '/auth/signup'

    @property
    def link_to_login(self):
        return self.driver.find_element(*SignupPageLocators.LINK_TO_LOGIN)