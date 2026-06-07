@smoke @login
Feature: User Authentication
  As a user of SauceDemo
  I want to log in with valid credentials
  So that I can access the product inventory

  Background:
    Given I am on the SauceDemo login page

  @smoke @regression
  Scenario: Successful login with standard user
    When I enter username "standard_user" and password "secret_sauce"
    And I click the login button
    Then I should be redirected to the inventory page
    And the page title should be "Products"

  @regression
  Scenario: Login with locked out user shows error
    When I enter username "locked_out_user" and password "secret_sauce"
    And I click the login button
    Then I should see an error message "Epic sadface: Sorry, this user has been locked out."

  @regression
  Scenario: Login with wrong password shows error
    When I enter username "standard_user" and password "wrong_password"
    And I click the login button
    Then I should see an error message containing "Username and password do not match"

  @regression
  Scenario: Login with empty username shows error
    When I enter username "" and password "secret_sauce"
    And I click the login button
    Then I should see an error message containing "Username is required"

  @regression
  Scenario: Login with empty password shows error
    When I enter username "standard_user" and password ""
    And I click the login button
    Then I should see an error message containing "Password is required"

  @regression
  Scenario: Login with both fields empty shows error
    When I enter username "" and password ""
    And I click the login button
    Then I should see an error message containing "Username is required"

  @regression
  Scenario: Error message can be dismissed
    When I enter username "locked_out_user" and password "secret_sauce"
    And I click the login button
    And I close the error message
    Then the error message should not be visible

  @regression
  Scenario Outline: Multiple user types can log in successfully
    When I enter username "<username>" and password "secret_sauce"
    And I click the login button
    Then I should be redirected to the inventory page

    Examples:
      | username                  |
      | standard_user             |
      | problem_user              |
      | performance_glitch_user   |
      | error_user                |
      | visual_user               |

  @smoke @regression
  Scenario: User can logout successfully
    When I enter username "standard_user" and password "secret_sauce"
    And I click the login button
    And I open the burger menu
    And I click logout
    Then I should be on the login page

  @regression
  Scenario: Login page displays logo
    Then the SauceDemo logo should be visible
