Feature:Product
  We want to test that product availability functionality works correctly

  Scenario: Successfully creating a product with valid data
    Given A product with name MacBook 16, price 40000.0, and availability 14
    Then The product should have the correct name, price, and availability

  Scenario: Failing to create a product with invalid price
    Given A product with name MacBook 16, price NaN, and availability 100
    Then The product creation should raise a ValueError due to invalid price

  Scenario: Availability check for a product
    Given A product with name MacBook 16, price 40000.0, and availability 14
    When I check if the product is available with requested amount 5
    Then The availability check should return True

  Scenario: Failing availability check for a product when requested amount exceeds availability
    Given A product with name MacBook 16, price 40000.0, and availability 14
    When I check if the product is available with requested amount 15
    Then The availability check should return False

  Scenario: Comparing two products with the same name
    Given A first product with name MacBook 16, price 40000.0, and availability 14
    And A second product with the same name MacBook 16, price 40000.0, and availability 14
    When I compare the two products
    Then The products should be considered equal

  Scenario: Updating the price of a product
   Given A product with name MacBook 16, price 40000.0, and availability 14
    When I update the price of the product to 45000.0
    Then The product price should be updated to 45000.0
