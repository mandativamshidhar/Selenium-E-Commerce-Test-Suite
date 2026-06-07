from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class CartPage(BasePage):
    PAGE_TITLE        = (By.CLASS_NAME, "title")
    CART_ITEMS        = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES        = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES       = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITIES   = (By.CLASS_NAME, "cart_quantity")
    REMOVE_BTNS       = (By.CSS_SELECTOR, "[data-test^='remove']")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    CHECKOUT_BTN      = (By.ID, "checkout")

    def is_on_cart_page(self):
        return "cart" in self.get_current_url()

    def get_cart_item_names(self):
        return [el.text for el in self.get_elements(self.ITEM_NAMES)]

    def get_cart_item_count(self):
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)

    def get_cart_item_prices(self):
        prices = [el.text for el in self.get_elements(self.ITEM_PRICES)]
        return [float(p.replace("$", "")) for p in prices]

    def remove_item_by_name(self, name):
        locator = (By.XPATH, f"//div[@class='inventory_item_name'][text()='{name}']/ancestor::div[@class='cart_item']//button")
        self.click(locator)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING)

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BTN)

    def is_item_in_cart(self, name):
        return name in self.get_cart_item_names()

    def is_cart_empty(self):
        return self.get_cart_item_count() == 0
