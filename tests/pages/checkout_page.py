from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    PAGE_TITLE    = (By.CLASS_NAME, "title")
    FIRST_NAME    = (By.ID, "first-name")
    LAST_NAME     = (By.ID, "last-name")
    POSTAL_CODE   = (By.ID, "postal-code")
    # Use data-test attribute — more reliable than ID on SauceDemo
    CONTINUE_BTN  = (By.CSS_SELECTOR, "[data-test='continue']")
    CANCEL_BTN    = (By.CSS_SELECTOR, "[data-test='cancel']")
    ERROR_MSG     = (By.CSS_SELECTOR, "[data-test='error']")

    def is_on_checkout_info_page(self):
        return "checkout-step-one" in self.get_current_url()

    def fill_info(self, first, last, postal):
        """Fill checkout fields — handles empty strings correctly."""
        first_el = self.wait_for_visible(self.FIRST_NAME)
        first_el.clear()
        if first:
            first_el.send_keys(first)

        last_el = self.wait_for_visible(self.LAST_NAME)
        last_el.clear()
        if last:
            last_el.send_keys(last)

        postal_el = self.wait_for_visible(self.POSTAL_CODE)
        postal_el.clear()
        if postal:
            postal_el.send_keys(postal)

    def continue_checkout(self):
        self.click(self.CONTINUE_BTN)

    def cancel(self):
        self.click(self.CANCEL_BTN)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)

    def is_error_displayed(self):
        return self.is_element_present(self.ERROR_MSG)


class CheckoutOverviewPage(BasePage):
    PAGE_TITLE      = (By.CLASS_NAME, "title")
    CART_ITEMS      = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES      = (By.CLASS_NAME, "inventory_item_name")
    SUBTOTAL_LABEL  = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL       = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL     = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN      = (By.CSS_SELECTOR, "[data-test='finish']")
    CANCEL_BTN      = (By.CSS_SELECTOR, "[data-test='cancel']")

    def is_on_overview_page(self):
        return "checkout-step-two" in self.get_current_url()

    def get_subtotal(self):
        text = self.get_text(self.SUBTOTAL_LABEL)
        return float(text.split("$")[1])

    def get_tax(self):
        text = self.get_text(self.TAX_LABEL)
        return float(text.split("$")[1])

    def get_total(self):
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.split("$")[1])

    def get_item_names(self):
        return [el.text for el in self.get_elements(self.ITEM_NAMES)]

    def finish_order(self):
        self.click(self.FINISH_BTN)

    def cancel(self):
        self.click(self.CANCEL_BTN)


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER   = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT     = (By.CLASS_NAME, "complete-text")
    PONY_IMAGE        = (By.CLASS_NAME, "pony_express")
    BACK_HOME_BTN     = (By.CSS_SELECTOR, "[data-test='back-to-products']")

    def is_on_complete_page(self):
        return "checkout-complete" in self.get_current_url()

    def get_complete_header(self):
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self):
        return self.get_text(self.COMPLETE_TEXT)

    def back_to_products(self):
        self.click(self.BACK_HOME_BTN)

    def is_pony_image_displayed(self):
        return self.is_element_present(self.PONY_IMAGE)
