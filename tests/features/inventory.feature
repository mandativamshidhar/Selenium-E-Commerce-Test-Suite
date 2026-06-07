@regression @inventory
Feature: Product Inventory
  As a logged-in user
  I want to browse and sort products
  So that I can find items I want to purchase

  Background:
    Given I am logged in as "standard_user"

  @smoke @regression
  Scenario: Inventory page displays 6 products
    Then the inventory page should show 6 products

  @regression
  Scenario: All products have names, prices, and descriptions
    Then all products should have names
    And all products should have prices
    And all products should have descriptions

  @smoke @regression
  Scenario: Sort products by price low to high
    When I sort products by "low_to_high"
    Then products should be sorted by price ascending

  @regression
  Scenario: Sort products by price high to low
    When I sort products by "high_to_low"
    Then products should be sorted by price descending

  @regression
  Scenario: Sort products by name A to Z
    When I sort products by "az"
    Then products should be sorted alphabetically ascending

  @regression
  Scenario: Sort products by name Z to A
    When I sort products by "za"
    Then products should be sorted alphabetically descending

  @smoke @regression
  Scenario: Add single item to cart
    When I add product "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"

  @regression
  Scenario: Add multiple items to cart
    When I add product "Sauce Labs Backpack" to the cart
    And I add product "Sauce Labs Bike Light" to the cart
    Then the cart badge should show "2"

  @regression
  Scenario: Remove item from inventory page
    When I add product "Sauce Labs Backpack" to the cart
    And I remove product "Sauce Labs Backpack" from the inventory
    Then the cart badge should not be visible

  @regression
  Scenario: Add all products to cart
    When I add all products to the cart
    Then the cart badge should show "6"

  @regression
  Scenario: Click product name navigates to detail page
    When I click on product "Sauce Labs Backpack"
    Then I should be on the product detail page
    And the product name should be "Sauce Labs Backpack"
