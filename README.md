![CI](https://github.com/mandativamshidhar/Selenium-E-Commerce-Test-Suite/actions/workflows/test.yml/badge.svg)
# SauceDemo BDD Test Framework

A production-grade Selenium WebDriver framework using **Page Object Model (POM)** + **pytest-BDD (Gherkin)** for [saucedemo.com](https://www.saucedemo.com), with CI/CD via GitHub Actions.

---

## 🗂️ Project Structure

```
saucedemo-bdd/
├── .github/
│   └── workflows/
│       └── test.yml              # CI/CD pipeline (push, PR, manual)
├── tests/
│   ├── features/                 # Gherkin feature files
│   │   ├── login.feature         # 10 scenarios
│   │   ├── inventory.feature     # 12 scenarios
│   │   ├── cart.feature          # 7 scenarios
│   │   └── checkout.feature      # 9 scenarios
│   ├── pages/                    # Page Object Model classes
│   │   ├── base_page.py          # Shared Selenium helpers
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   ├── checkout_page.py      # Info + Overview + Complete
│   │   └── product_detail_page.py
│   └── step_defs/                # pytest-BDD step implementations
│       ├── test_login_steps.py
│       ├── test_inventory_steps.py
│       ├── test_cart_steps.py
│       └── test_checkout_steps.py
├── reports/                      # Auto-generated HTML reports
├── screenshots/                  # Failure screenshots (auto-captured)
├── conftest.py                   # Driver fixture, screenshot hook
├── pytest.ini                    # pytest + BDD config
├── requirements.txt
└── .env.example
```

---

## ✅ Test Coverage (40+ Scenarios)

| Feature    | Scenarios | Tags                        |
|------------|-----------|-----------------------------|
| Login      | 10        | `@smoke` `@regression`      |
| Inventory  | 12        | `@smoke` `@regression`      |
| Cart       | 7         | `@smoke` `@regression`      |
| Checkout   | 9         | `@smoke` `@regression`      |

### What's covered
- ✅ Login — valid users, locked user, wrong password, empty fields, error dismiss, all user types
- ✅ Inventory — product count, sort (A-Z, Z-A, price asc/desc), add/remove from cart, navigation
- ✅ Cart — add/remove items, cart persistence, item prices, continue shopping
- ✅ Checkout — full e2e flow, form validation, price summary, cancel/back flows

---

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone <your-repo>
cd saucedemo-bdd
pip install -r requirements.txt

# 2. Run smoke tests (headless Chrome)
pytest -m smoke --browser=chrome --headless

# 3. Run full regression
pytest -m regression --browser=chrome --headless

# 4. Run in Firefox
pytest -m regression --browser=firefox --headless

# 5. Run with visible browser (debugging)
pytest -m smoke --browser=chrome

# 6. Open the HTML report
open reports/report.html
```

---

## 🌐 Cross-Browser

```bash
# Chrome (default)
pytest --browser=chrome --headless

# Firefox
pytest --browser=firefox --headless

# Edge (Windows)
pytest --browser=edge --headless
```

---

## 🔁 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/test.yml`) runs:

1. **Smoke gate** — Chrome, every push/PR
2. **Regression matrix** — Chrome + Firefox in parallel (Ubuntu)
3. **Edge regression** — Windows runner
4. **Summary** — Aggregated pass/fail table posted to GitHub Actions summary

### Artifacts published per run
- `smoke-report/` — HTML report + screenshots
- `regression-chrome/` — HTML report + screenshots
- `regression-firefox/` — HTML report + screenshots
- `regression-edge/` — HTML report + screenshots
- `all-test-reports/` — All combined (30-day retention)

---

## 📸 Failure Screenshots

Screenshots are automatically captured on test failure and saved to `screenshots/` with the format:

```
screenshots/tests_step_defs_test_login_steps__login_with_locked_out__20240601_143022.png
```

They are also referenced in the HTML report when using `pytest-html`.

---

## ⚙️ Config

| Option | Default | Description |
|--------|---------|-------------|
| `--browser` | `chrome` | Browser: `chrome`, `firefox`, `edge` |
| `--headless` | `False` | Run headless (CI default) |
| `-m smoke` | — | Smoke tests only |
| `-m regression` | — | Full regression |

---

## 🧱 Architecture

```
Feature File (Gherkin)
       │
       ▼
Step Definitions (pytest-BDD)
       │  maps natural language → Python
       ▼
Page Objects (POM)
       │  encapsulate locators + actions
       ▼
Base Page (Selenium WebDriver)
       │  wait helpers, click, type, etc.
       ▼
WebDriver (Chrome / Firefox / Edge)
```
