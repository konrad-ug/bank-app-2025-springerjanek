Feature: Account transfers

Scenario: User can make outgoing transfer from personal account
    Given Account registry is empty
    And I create an account using name: "John", last name: "Doe", pesel: "12345678910"
    When I make an outgoing transfer of 100 from account with pesel "12345678910"
    Then Account with pesel "12345678910" has balance equal to 0

Scenario: Outgoing transfer fails when balance is insufficient
    Given Account registry is empty
    And I create an account using name: "John", last name: "Doe", pesel: "12345678910"
    When I make an outgoing transfer of 100 from account with pesel "12345678910"
    Then Account with pesel "12345678910" has balance equal to 0

Scenario: User can make express transfer from personal account
    Given Account registry is empty
    And I create an account using name: "John", last name: "Doe", pesel: "12345678910"
    And I make an incoming transfer of 100 to account with pesel "12345678910"
    When I make an express transfer of 50 from account with pesel "12345678910"
    Then Account with pesel "12345678910" has balance equal to 49

Scenario: Incoming transfer increases account balance
    Given Account registry is empty
    And I create an account using name: "Anna", last name: "Smith", pesel: "99988877766"
    When I make an incoming transfer of 200 to account with pesel "99988877766"
    Then Account with pesel "99988877766" has balance equal to 200
