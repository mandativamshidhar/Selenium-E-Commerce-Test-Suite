from pytest_bdd import given, when, then, parsers, scenarios
from tests.pages.inventory_page import InventoryPage
from tests.pages.product_detail_page import ProductDetailPage

scenarios("../features/inventory.feature")


@then("the inventory page should show 6 products")
def verify_six_products(driver):
    count = InventoryPage(driver).get_item_count()
    assert count == 6, f"Expected 6 products, got {count}"


@then("all products should have names")
def products_have_names(driver):
    names = InventoryPage(driver).get_all_item_names()
    assert all(n.strip() for n in names), "Some products have empty names"


@then("all products should have prices")
def products_have_prices(driver):
    prices = InventoryPage(driver).get_all_item_prices()
    assert all(p > 0 for p in prices), "Some products have zero/negative prices"


@then("all products should have descriptions")
def products_have_descriptions(driver):
    page = InventoryPage(driver)
    descs = [el.text for el in page.get_elements(InventoryPage.ITEM_DESC)]
    assert all(d.strip() for d in descs), "Some products have empty descriptions"


@when(parsers.parse('I sort products by "{sort_key}"'))
def sort_products(driver, sort_key):
    InventoryPage(driver).sort_products(sort_key)


@then("products should be sorted by price ascending")
def sorted_price_asc(driver):
    prices = InventoryPage(driver).get_all_item_prices()
    assert prices == sorted(prices), f"Prices not ascending: {prices}"


@then("products should be sorted by price descending")
def sorted_price_desc(driver):
    prices = InventoryPage(driver).get_all_item_prices()
    assert prices == sorted(prices, reverse=True), f"Prices not descending: {prices}"


@then("products should be sorted alphabetically ascending")
def sorted_alpha_asc(driver):
    names = InventoryPage(driver).get_all_item_names()
    assert names == sorted(names), f"Names not sorted A-Z: {names}"


@then("products should be sorted alphabetically descending")
def sorted_alpha_desc(driver):
    names = InventoryPage(driver).get_all_item_names()
    assert names == sorted(names, reverse=True), f"Names not sorted Z-A: {names}"


@when(parsers.parse('I add product "{product_name}" to the cart'))
def add_product_to_cart(driver, product_name):
    InventoryPage(driver).add_item_to_cart_by_name(product_name)


@when(parsers.parse('I remove product "{product_name}" from the inventory'))
def remove_product_from_inventory(driver, product_name):
    InventoryPage(driver).remove_item_by_name(product_name)


@when("I add all products to the cart")
def add_all_to_cart(driver):
    InventoryPage(driver).add_all_items_to_cart()


@when(parsers.parse('I click on product "{product_name}"'))
def click_product(driver, product_name):
    InventoryPage(driver).click_item_name(product_name)


@then("I should be on the product detail page")
def on_product_detail(driver):
    page = ProductDetailPage(driver)
    assert page.is_on_product_page(), f"Not on product page: {driver.current_url}"


@then(parsers.parse('the product name should be "{name}"'))
def product_name_is(driver, name):
    actual = ProductDetailPage(driver).get_product_name()
    assert actual == name, f"Expected '{name}', got '{actual}'"
