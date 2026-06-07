import os
import base64
import pytest
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.cart_page import CartPage
from pytest_bdd import given, when, then, parsers

# ── Absolute paths anchored to this file ──────────────────────────────────────
ROOT_DIR        = Path(__file__).parent.resolve()
REPORTS_DIR     = ROOT_DIR / "reports"
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
REPORT_PATH     = REPORTS_DIR / "report.html"


# ──────────────────────────────────────────────────────────────────────────────
# CLI Options
# ──────────────────────────────────────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption("--browser",   action="store", default="chrome",
                     help="Browser: chrome | edge | firefox")
    parser.addoption("--headless",  action="store_true", default=False,
                     help="Run headless")


# ──────────────────────────────────────────────────────────────────────────────
# Create folders + force absolute report path before session starts
# ──────────────────────────────────────────────────────────────────────────────
def pytest_configure(config):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Override the --html path to always be absolute regardless of cwd
    # Works whether the user passed --html or not (pytest.ini sets a default)
    html_plugin = config.pluginmanager.get_plugin("html")
    if html_plugin:
        config.option.htmlpath = str(REPORT_PATH)
        config.option.self_contained_html = True


def pytest_html_report_title(report):
    report.title = "SauceDemo BDD Test Report"


# ──────────────────────────────────────────────────────────────────────────────
# Screenshot helper — always uses absolute path
# ──────────────────────────────────────────────────────────────────────────────
def _take_screenshot(driver, nodeid):
    safe = (nodeid
            .replace("/",  "_")
            .replace("\\", "_")
            .replace("::", "__")
            .replace(" ",  "_"))
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOTS_DIR / f"{safe}__{ts}.png"
    try:
        driver.save_screenshot(str(path))
        print(f"\n📸 Screenshot saved: {path}")
        return str(path)
    except Exception as e:
        print(f"\n⚠️  Screenshot failed: {e}")
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Hook: capture screenshot on failure + embed in HTML report
# ──────────────────────────────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep     = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            path = _take_screenshot(drv, item.nodeid)
            if path and os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        img_b64 = base64.b64encode(f.read()).decode("utf-8")
                    rep.extras = getattr(rep, "extras", []) + [{
                        "name":      "Screenshot",
                        "format":    "image",
                        "content":   img_b64,
                        "mime_type": "image/png",
                    }]
                except Exception as embed_err:
                    print(f"\n⚠️  Could not embed screenshot: {embed_err}")


# ──────────────────────────────────────────────────────────────────────────────
# Browser Fixture
# ──────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver(request):
    browser  = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--remote-debugging-port=9222")
        drv = webdriver.Chrome(options=options)   # Selenium Manager auto-downloads

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Edge(options=options)     # Selenium Manager auto-downloads

    elif browser == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        drv = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    drv.implicitly_wait(10)
    yield drv
    drv.quit()


# ══════════════════════════════════════════════════════════════════════════════
# SHARED STEP DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

@given(parsers.parse('I am logged in as "{user_type}"'))
def logged_in_as(driver, user_type):
    LoginPage(driver).login_as(user_type)
    assert InventoryPage(driver).is_on_inventory_page(), \
        f"Login failed, URL: {driver.current_url}"


@given(parsers.parse('I have added "{product_name}" to the cart'))
def add_item_precondition(driver, product_name):
    InventoryPage(driver).add_item_to_cart_by_name(product_name)


@then("I should be on the inventory page")
def on_inventory_page(driver):
    assert InventoryPage(driver).is_on_inventory_page(), \
        f"Not on inventory page: {driver.current_url}"


@then(parsers.parse('the cart badge should show "{count}"'))
def cart_badge_shows(driver, count):
    actual = InventoryPage(driver).get_cart_badge_count()
    assert actual == int(count), f"Expected badge {count}, got {actual}"


@then("the cart badge should not be visible")
def cart_badge_not_visible(driver):
    assert InventoryPage(driver).get_cart_badge_count() == 0, "Cart badge still visible"


@when("I navigate to the cart page")
def go_to_cart(driver):
    InventoryPage(driver).go_to_cart()


@when("I navigate to the inventory page")
def go_to_inventory(driver):
    InventoryPage(driver).open("/inventory.html")


@then("I should be on the login page")
def on_login_page(driver):
    assert LoginPage(driver).is_on_login_page(), \
        f"Not on login page: {driver.current_url}"


@then("I should be on the cart page")
def on_cart_page(driver):
    assert CartPage(driver).is_on_cart_page(), \
        f"Not on cart page: {driver.current_url}"
