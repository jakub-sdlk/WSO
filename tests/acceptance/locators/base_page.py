from selenium.webdriver.common.by import By


class BasePageLocators:
    TITLE = By.TAG_NAME, 'title'
    H1_TITLE = By.TAG_NAME, 'h1'
    H2_SUBTITLE = By.TAG_NAME, 'h2'

