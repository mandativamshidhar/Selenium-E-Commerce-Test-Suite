@regression @cart
Feature: Shopping Cart
  As a logged-in user
  I want to manage my shopping cart
  So that I can review items before checkout

  Background:
    Given I am logged in as "standard_user"

  @smoke @regression
  Scenario: Cart page shows added item
    Given I have added "Sauce Labs Backpack" to the cart
    When I navigate to the cart page
    Then the cart should contain "Sauce Labs Backpack"

  @regression
  Scenario: Cart shows correct item count
    Given I have added "Sauce Labs Backpack" to the cart
    And I have added "Sauce Labs Bike Light" to the cart
    When I navigate to the cart page
    Then the cart should have 2 items

  @regression
  Scenario: Remove item from cart
    Given I have added "Sauce Labs Backpack" to the cart
    When I navigate to the cart page
    And I remove "Sauce Labs Backpack" from the cart
    Then the cart should be empty

  @regression
  Scenario: Continue shopping from cart returns to inventory
    Given I have added "Sauce Labs Backpack" to the cart
    When I navigate to the cart page
    And I click continue shopping
    Then I should be on the inventory page

  @smoke @regression
  Scenario: Cart persists items after navigation
    Given I have added "Sauce Labs Backpack" to the cart
    When I navigate to the inventory page
    Then the cart badge should show "1"

  @regression
  Scenario: Cart item shows correct price
    Given I have added "Sauce Labs Backpack" to the cart
    When I navigate to the cart page
    Then the cart item price should be "29.99"

  @regression
  Scenario: Empty cart has no badge
    When I navigate to the cart page
    Then the cart should be empty
    And the cart badge should not be visible
