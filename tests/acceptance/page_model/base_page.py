from tests.acceptance.locators.base_page import BasePageLocators


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @property
    def url(self):
        return 'http://127.0.0.1:5000'

    @property
    def title(self):
        return self.driver.find_element(*BasePageLocators.TITLE)


    @property
    def h1_title(self):
        return self.driver.find_element(*BasePageLocators.H1_TITLE)

    @property
    def h2_subtitle(self):
        return self.driver.find_element(*BasePageLocators.H2_SUBTITLE)