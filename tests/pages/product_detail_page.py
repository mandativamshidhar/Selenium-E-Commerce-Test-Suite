from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class ProductDetailPage(BasePage):
    PRODUCT_NAME    = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DESC    = (By.CLASS_NAME, "inventory_details_desc")
    PRODUCT_PRICE   = (By.CLASS_NAME, "inventory_details_price")
    PRODUCT_IMAGE   = (By.CLASS_NAME, "inventory_details_img")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    REMOVE_BTN      = (By.CSS_SELECTOR, "[data-test^='remove']")
    BACK_BUTTON     = (By.ID, "back-to-products")

    def is_on_product_page(self):
        return "inventory-item" in self.get_current_url()

    def get_product_name(self):
        return self.get_text(self.PRODUCT_NAME)

    def get_product_description(self):
        return self.get_text(self.PRODUCT_DESC)

    def get_product_price(self):
        text = self.get_text(self.PRODUCT_PRICE)
        return float(text.replace("$", ""))

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)

    def remove_from_cart(self):
        self.click(self.REMOVE_BTN)

    def go_back(self):
        self.click(self.BACK_BUTTON)

    def is_add_to_cart_visible(self):
        return self.is_element_present(self.ADD_TO_CART_BTN)

    def is_remove_visible(self):
        return self.is_element_present(self.REMOVE_BTN)
