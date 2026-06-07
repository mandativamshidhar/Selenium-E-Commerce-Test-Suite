from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os


class BasePage:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    # ── Navigation ──────────────────────────────
    def open(self, path=""):
        self.driver.get(f"{self.BASE_URL}{path}")

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    # ── Waits ────────────────────────────────────
    def wait_for_element(self, locator, timeout=None):
        t = timeout or self.DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=None):
        t = timeout or self.DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_visible(self, locator, timeout=None):
        t = timeout or self.DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_url_contains(self, text, timeout=None):
        t = timeout or self.DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, t).until(
            EC.url_contains(text)
        )

    def is_element_present(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ── Interactions ─────────────────────────────
    def click(self, locator):
        self.wait_for_clickable(locator).click()

    def type_text(self, locator, text):
        el = self.wait_for_visible(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        return self.wait_for_visible(locator).text

    def get_attribute(self, locator, attr):
        return self.wait_for_element(locator).get_attribute(attr)

    def scroll_to_element(self, locator):
        el = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        return el

    def get_elements(self, locator):
        self.wait_for_element(locator)
        return self.driver.find_elements(*locator)
