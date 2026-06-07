from pytest_bdd import given, when, then, parsers, scenarios
from tests.pages.cart_page import CartPage
from tests.pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage

scenarios("../features/checkout.feature")


@given("I have navigated to checkout")
def navigate_to_checkout(driver):
    from tests.pages.inventory_page import InventoryPage
    # Must navigate to cart page first, then proceed to checkout
    inv = InventoryPage(driver)
    inv.go_to_cart()
    cart = CartPage(driver)
    cart.proceed_to_checkout()
    info = CheckoutInfoPage(driver)
    assert info.is_on_checkout_info_page(), f"Not on checkout: {driver.current_url}"


@when(parsers.parse('I fill in checkout info with first name "{first}" last name "{last}" and postal code "{postal}"'))
def fill_checkout_info(driver, first, last, postal):
    CheckoutInfoPage(driver).fill_info(first, last, postal)


@when(parsers.parse('I leave first name empty and fill last name "{last}" and postal code "{postal}"'))
def fill_no_first(driver, last, postal):
    CheckoutInfoPage(driver).fill_info("", last, postal)


@when(parsers.parse('I fill in first name "{first}" leave last name empty and postal code "{postal}"'))
def fill_no_last(driver, first, postal):
    CheckoutInfoPage(driver).fill_info(first, "", postal)


@when(parsers.parse('I fill in first name "{first}" last name "{last}" and leave postal code empty'))
def fill_no_postal(driver, first, last):
    CheckoutInfoPage(driver).fill_info(first, last, "")


@when("I continue to checkout overview")
def continue_to_overview(driver):
    CheckoutInfoPage(driver).continue_checkout()


@when("I finish the order")
def finish_order(driver):
    CheckoutOverviewPage(driver).finish_order()


@then("I should see the order confirmation")
def order_confirmation(driver):
    page = CheckoutCompletePage(driver)
    assert page.is_on_complete_page(), f"Not on complete page: {driver.current_url}"


@then(parsers.parse('the confirmation header should say "{text}"'))
def confirmation_header(driver, text):
    actual = CheckoutCompletePage(driver).get_complete_header()
    assert actual == text, f"Expected '{text}', got '{actual}'"


@then(parsers.parse('I should see a checkout error containing "{text}"'))
def checkout_error_contains(driver, text):
    page = CheckoutInfoPage(driver)
    assert page.is_error_displayed(), "No error displayed"
    actual = page.get_error_message()
    assert text in actual, f"Expected '{text}' in '{actual}'"


@then(parsers.parse('the overview should contain "{item_name}"'))
def overview_contains(driver, item_name):
    page = CheckoutOverviewPage(driver)
    assert page.is_on_overview_page(), f"Not on overview: {driver.current_url}"
    names = page.get_item_names()
    assert item_name in names, f"'{item_name}' not in overview: {names}"


@then("the overview should show item total")
def overview_has_subtotal(driver):
    assert CheckoutOverviewPage(driver).get_subtotal() > 0, "Subtotal is 0"


@then("the overview should show tax")
def overview_has_tax(driver):
    assert CheckoutOverviewPage(driver).get_tax() > 0, "Tax is 0"


@then("the overview should show order total")
def overview_has_total(driver):
    assert CheckoutOverviewPage(driver).get_total() > 0, "Total is 0"


@when("I cancel the checkout")
def cancel_checkout(driver):
    CheckoutInfoPage(driver).cancel()


@when("I cancel from the overview")
def cancel_from_overview(driver):
    CheckoutOverviewPage(driver).cancel()


@when("I click back to products")
def back_to_products(driver):
    CheckoutCompletePage(driver).back_to_products()
