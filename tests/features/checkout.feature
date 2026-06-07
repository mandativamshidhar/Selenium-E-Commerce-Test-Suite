@regression @checkout
Feature: Checkout Flow
  As a logged-in user
  I want to complete the checkout process
  So that I can purchase items in my cart

  Background:
    Given I am logged in as "standard_user"
    And I have added "Sauce Labs Backpack" to the cart
    And I have navigated to checkout

  @smoke @regression
  Scenario: Complete full checkout flow
    When I fill in checkout info with first name "John" last name "Doe" and postal code "12345"
    And I continue to checkout overview
    And I finish the order
    Then I should see the order confirmation
    And the confirmation header should say "Thank you for your order!"

  @regression
  Scenario: Checkout info form validates empty first name
    When I leave first name empty and fill last name "Doe" and postal code "12345"
    And I continue to checkout overview
    Then I should see a checkout error containing "First Name is required"

  @regression
  Scenario: Checkout info form validates empty last name
    When I fill in first name "John" leave last name empty and postal code "12345"
    And I continue to checkout overview
    Then I should see a checkout error containing "Last Name is required"

  @regression
  Scenario: Checkout info form validates empty postal code
    When I fill in first name "John" last name "Doe" and leave postal code empty
    And I continue to checkout overview
    Then I should see a checkout error containing "Postal Code is required"

  @smoke @regression
  Scenario: Checkout overview shows correct item
    When I fill in checkout info with first name "John" last name "Doe" and postal code "12345"
    And I continue to checkout overview
    Then the overview should contain "Sauce Labs Backpack"

  @regression
  Scenario: Checkout overview shows price summary
    When I fill in checkout info with first name "Jane" last name "Smith" and postal code "90210"
    And I continue to checkout overview
    Then the overview should show item total
    And the overview should show tax
    And the overview should show order total

  @regression
  Scenario: Cancel checkout returns to cart
    When I cancel the checkout
    Then I should be on the cart page

  @regression
  Scenario: Cancel on overview returns to inventory
    When I fill in checkout info with first name "John" last name "Doe" and postal code "12345"
    And I continue to checkout overview
    And I cancel from the overview
    Then I should be on the inventory page

  @regression
  Scenario: Back to products after order completion
    When I fill in checkout info with first name "John" last name "Doe" and postal code "12345"
    And I continue to checkout overview
    And I finish the order
    And I click back to products
    Then I should be on the inventory page
