from pytest_bdd import given, when, then, parsers, scenarios
from tests.pages.cart_page import CartPage

scenarios("../features/cart.feature")


@then(parsers.parse('the cart should contain "{item_name}"'))
def cart_contains_item(driver, item_name):
    assert CartPage(driver).is_item_in_cart(item_name), f"'{item_name}' not found in cart"


@then(parsers.parse("the cart should have {count:d} items"))
def cart_has_n_items(driver, count):
    actual = CartPage(driver).get_cart_item_count()
    assert actual == count, f"Expected {count} items, got {actual}"


@when(parsers.parse('I remove "{item_name}" from the cart'))
def remove_from_cart(driver, item_name):
    CartPage(driver).remove_item_by_name(item_name)


@then("the cart should be empty")
def cart_is_empty(driver):
    assert CartPage(driver).is_cart_empty(), "Cart is not empty"


@when("I click continue shopping")
def click_continue_shopping(driver):
    CartPage(driver).continue_shopping()


@then(parsers.parse('the cart item price should be "{price}"'))
def cart_item_price(driver, price):
    prices = CartPage(driver).get_cart_item_prices()
    assert float(price) in prices, f"Price {price} not found in cart: {prices}"
