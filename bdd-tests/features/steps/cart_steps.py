# import os, sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from behave import given, when, then
from app.eshop import Product, ShoppingCart


@given("The product has availability of {availability}")
def create_product_for_cart(context, availability):
    availability_int = int(availability.strip())
    context.product = Product(name="any", price=123, available_amount=availability_int)

@given('An empty shopping cart')
def empty_cart(context):
    context.cart = ShoppingCart()

@when("I add product to the cart in amount {product_amount}")
def add_product(context, product_amount):
    try:
        amount_int = int(product_amount)
        print(context.cart.products, product_amount, context.product, context.product.available_amount)
        context.cart.add_product(context.product, amount_int)
        context.add_successfully = True
    except ValueError as e:
        print(e)
        context.add_successfully = False

@then("Product is added to the cart successfully")
def add_successful(context):
    assert context.add_successfully == True

@then("Product is not added to cart successfully")
def add_failed(context):
    assert context.add_successfully == False


@given("The new product has availability of {availability} and product price is {price}")
def create_product_with_amount_and_price(context, availability, price):
    avail_int = int(availability)
    price = int(price)
    context.product = Product(name="any", price=price, available_amount=avail_int)


@then("Cart total price is {total_price}")
def cart_total_price(context, total_price):
    total_price = int(total_price)
    assert context.cart.calculate_total() == total_price


if __name__ == '__main__':
    print("hello")