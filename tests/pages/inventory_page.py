from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tests.pages.base_page import BasePage


class InventoryPage(BasePage):
    # ── Locators ─────────────────────────────────
    PAGE_TITLE         = (By.CLASS_NAME, "title")
    INVENTORY_LIST     = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEMS    = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES         = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES        = (By.CLASS_NAME, "inventory_item_price")
    ITEM_DESC          = (By.CLASS_NAME, "inventory_item_desc")
    ITEM_IMAGES        = (By.CLASS_NAME, "inventory_item_img")
    ADD_TO_CART_BTNS   = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    REMOVE_BTNS        = (By.CSS_SELECTOR, "[data-test^='remove']")
    SORT_DROPDOWN      = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE         = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK          = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU        = (By.ID, "react-burger-menu-btn")
    MENU_LOGOUT        = (By.ID, "logout_sidebar_link")
    MENU_ABOUT         = (By.ID, "about_sidebar_link")
    MENU_RESET         = (By.ID, "reset_sidebar_link")
    MENU_ALL_ITEMS     = (By.ID, "inventory_sidebar_link")
    MENU_CLOSE         = (By.ID, "react-burger-cross-btn")

    SORT_OPTIONS = {
        "az": "az",
        "za": "za",
        "low_to_high": "lohi",
        "high_to_low": "hilo",
    }

    def is_on_inventory_page(self):
        return self.is_element_present(self.INVENTORY_LIST)

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def get_all_item_names(self):
        return [el.text for el in self.get_elements(self.ITEM_NAMES)]

    def get_all_item_prices(self):
        prices = [el.text for el in self.get_elements(self.ITEM_PRICES)]
        return [float(p.replace("$", "")) for p in prices]

    def get_item_count(self):
        return len(self.get_elements(self.INVENTORY_ITEMS))

    def add_item_to_cart_by_index(self, index=0):
        btns = self.get_elements(self.ADD_TO_CART_BTNS)
        btns[index].click()

    def add_item_to_cart_by_name(self, name):
        # Use contains() on class to handle multi-class elements, and
        # search the full page (not just inventory_item ancestor) for robustness
        locator = (By.XPATH,
            f"//div[contains(@class,'inventory_item_name') and text()='{name}']"
            f"/following::button[contains(@data-test,'add-to-cart')]"
        )
        self.click(locator)

    def remove_item_by_name(self, name):
        locator = (By.XPATH,
            f"//div[contains(@class,'inventory_item_name') and text()='{name}']"
            f"/following::button[contains(@data-test,'remove')]"
        )
        self.click(locator)

    def get_cart_badge_count(self):
        if self.is_element_present(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def sort_products(self, sort_key):
        value = self.SORT_OPTIONS.get(sort_key, sort_key)
        dropdown = Select(self.wait_for_element(self.SORT_DROPDOWN))
        dropdown.select_by_value(value)

    def open_burger_menu(self):
        self.click(self.BURGER_MENU)
        # Wait until the logout link is visible before returning
        self.wait_for_visible(self.MENU_LOGOUT)

    def logout(self):
        self.open_burger_menu()
        self.click(self.MENU_LOGOUT)

    def reset_app_state(self):
        self.open_burger_menu()
        self.click(self.MENU_RESET)
        self.click(self.MENU_CLOSE)

    def click_item_name(self, name):
        # Use contains() to avoid exact class match failures
        locator = (By.XPATH, f"//div[contains(@class,'inventory_item_name') and text()='{name}']")
        self.click(locator)

    def add_all_items_to_cart(self):
        btns = self.get_elements(self.ADD_TO_CART_BTNS)
        for btn in btns:
            btn.click()
