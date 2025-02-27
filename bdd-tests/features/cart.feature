Feature:Shopping cart
  We want to test that shopping cart functionality works correctly

  Scenario: Successful add product to cart
    Given The product has availability of 123
    And An empty shopping cart
    When I add product to the cart in amount 123
    Then Product is added to the cart successfully

  Scenario: Failed add product to cart
    Given The product has availability of 123
    And An empty shopping cart
    When I add product to the cart in amount 124
    Then Product is not added to cart successfully

  Scenario: Cart total calculated correctly
    Given The new product has availability of 10 and product price is 123
    And An empty shopping cart
    When I add product to the cart in amount 9
    Then Product is added to the cart successfully
    And Cart total price is 1107
