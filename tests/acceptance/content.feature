Feature: Test that pages gave correct content
  Scenario: Login page has a correct title and subtitle
    Given I am on the login page
    Then The h1 title has content "Workout Stats"
    And The h2 subtitle has content "Log into your account"

  Scenario: Signup has a correct title and subtitle
    Given I am on the signup page
    Then The h1 title has content "Workout Stats"
    And The h2 subtitle has content "Join us today!"