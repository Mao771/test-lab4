from behave import given, when, then
from app.eshop import Product

#  Scenario: Successfully creating a product with valid data
@given("A product with name {name}, price {price}, and availability {availability}")
def create_valid_product(context, name, price,availability):
    try:
        context.product = Product(name=name,
     price=float(price), available_amount=int(availability))
    except:
        context.product_creation_failed = True

@then("The product should have the correct name, price, and availability")
def verify_product_attributes(context):
    assert context.product.name == "MacBook 16"
    assert context.product.price == 40000.0
    assert context.product.available_amount == 14

#  Scenario: Failing to create a product with invalid price
@then("The product creation should raise a ValueError due to invalid price")
def check_invalid_price_creation(context):
    assert hasattr(context, 'product_creation_failed') and context.product_creation_failed

#  Scenario: Availability check for a product
@when("I check if the product is available with requested amount {amount}")
def check_product_availability(context, amount):
    context.is_available = context.product.is_available((int(amount)))

@then("The availability check should return True")
def verify_product_availability(context):
    assert context.is_available is True

#  Scenario: Availability check for a product
@then("The availability check should return False")
def verify_product_availability(context):
    assert context.is_available is False

@given("A first product with name {name}, price {price}, and availability {availability}")
def create_first_product(context, name, price, availability):
    context.product1 = Product(name=name,
     price=float(price), available_amount=int(availability))

# Scenario: Comparing two products with the same name
@given("A second product with the same name {name}, price {price}, and availability {availability}")
def create_second_product(context, name, price,
                                              availability):
    context.product2 = Product(name=name,
     price=float(price), available_amount=int(availability))

@when("I compare the two products")
def compare_products(context):
    context.are_equal = (context.product1 == context.product2)

@then("The products should be considered equal")
def verify_products_are_equal(context):
    assert context.are_equal is True

#   Scenario: Updating the price of a product
@when("I update the price of the product to {new_price}")
def update_product_price(context, new_price):
    context.product.price = float(new_price)

@then("The product price should be updated to {new_price}")
def verify_updated_product_price(context, new_price):
    assert context.product.price == float(new_price)