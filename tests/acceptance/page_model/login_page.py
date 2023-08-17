from tests.acceptance.locators.login_page import LoginPageLocators
from tests.acceptance.page_model.base_page import BasePage


class LoginPage(BasePage):
    @property
    def url(self):
        return super().url + '/auth/login'

    @property
    def link_to_register(self):
        return self.driver.find_element(*LoginPageLocators.LINK_TO_REGISTER)