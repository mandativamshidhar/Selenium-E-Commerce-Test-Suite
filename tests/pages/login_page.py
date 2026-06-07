from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    # ── Locators ─────────────────────────────────
    USERNAME_INPUT   = (By.ID, "user-name")
    PASSWORD_INPUT   = (By.ID, "password")
    LOGIN_BUTTON     = (By.ID, "login-button")
    ERROR_MESSAGE    = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BTN  = (By.CSS_SELECTOR, ".error-button")
    LOGIN_LOGO       = (By.CLASS_NAME, "login_logo")

    # Credentials
    VALID_PASSWORD   = "secret_sauce"
    USERS = {
        "standard":  "standard_user",
        "locked":    "locked_out_user",
        "problem":   "problem_user",
        "perf_glitch": "performance_glitch_user",
        "error":     "error_user",
        "visual":    "visual_user",
    }

    def open_login_page(self):
        self.open("/")

    def enter_username(self, username):
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password=None):
        password = password or self.VALID_PASSWORD
        self.open_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def login_as(self, user_type):
        username = self.USERS.get(user_type, user_type)
        self.login(username)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_element_present(self.ERROR_MESSAGE)

    def close_error(self):
        self.click(self.ERROR_CLOSE_BTN)

    def is_on_login_page(self):
        return self.is_element_present(self.LOGIN_BUTTON)

    def is_logo_displayed(self):
        return self.is_element_present(self.LOGIN_LOGO)
