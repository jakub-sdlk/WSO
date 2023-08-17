Feature: Test navigation between pages

  Scenario: Navigating from login page to signup page
    Given I am on the login page
    When I click on the "Register here" link
    Then I am on the signup page

  Scenario: Navigation from signup page to login page
    Given I am on the signup page
    When I click on the "Log in here" link
    Then I am on the login page