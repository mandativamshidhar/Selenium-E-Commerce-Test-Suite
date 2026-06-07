from pytest_bdd import given, when, then, parsers, scenarios
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage

scenarios("../features/login.feature")


@given("I am on the SauceDemo login page")
def open_login_page(driver):
    LoginPage(driver).open_login_page()


@when(parsers.re(r'I enter username "(?P<username>[^"]*)" and password "(?P<password>[^"]*)"'))
def enter_credentials(driver, username, password):
    page = LoginPage(driver)
    page.enter_username(username)
    page.enter_password(password)


@when("I click the login button")
def click_login(driver):
    LoginPage(driver).click_login()


@then("I should be redirected to the inventory page")
def verify_inventory_page(driver):
    page = InventoryPage(driver)
    assert page.is_on_inventory_page(), f"Expected inventory page, got: {driver.current_url}"


@then(parsers.parse('the page title should be "{title}"'))
def verify_page_title(driver, title):
    page = InventoryPage(driver)
    actual = page.get_page_title()
    assert actual == title, f"Expected '{title}', got '{actual}'"


@then(parsers.parse('I should see an error message "{message}"'))
def verify_exact_error(driver, message):
    page = LoginPage(driver)
    assert page.is_error_displayed(), "Error message not displayed"
    actual = page.get_error_message()
    assert actual == message, f"Expected '{message}', got '{actual}'"


@then(parsers.parse('I should see an error message containing "{text}"'))
def verify_error_contains(driver, text):
    page = LoginPage(driver)
    assert page.is_error_displayed(), "Error message not displayed"
    actual = page.get_error_message()
    assert text in actual, f"Expected '{text}' in '{actual}'"


@when("I close the error message")
def close_error(driver):
    LoginPage(driver).close_error()


@then("the error message should not be visible")
def error_not_visible(driver):
    assert not LoginPage(driver).is_error_displayed(), "Error still visible"


@when("I open the burger menu")
def open_burger_menu(driver):
    InventoryPage(driver).open_burger_menu()


@when("I click logout")
def click_logout(driver):
    # Use the page's logout() which handles burger menu + wait internally
    page = InventoryPage(driver)
    page.click(InventoryPage.MENU_LOGOUT)
    # Wait for login page to fully load
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "login-button"))
        )
    except Exception:
        # Fallback: just wait for URL to be root
        WebDriverWait(driver, 15).until(
            lambda d: d.current_url.rstrip("/") == "https://www.saucedemo.com"
        )


@then("the SauceDemo logo should be visible")
def logo_visible(driver):
    assert LoginPage(driver).is_logo_displayed(), "Login logo not visible"
