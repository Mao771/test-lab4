from app.eshop import Product, ShoppingCart, Order
import pytest


@pytest.fixture
def product():
    return Product(name="Test product", price=123, available_amount=10)

@pytest.fixture
def cart():
    return ShoppingCart()

def test_add_product_to_cart_successful(cart, product):
    cart.add_product(product, 9)
    assert cart.contains_product(product)
    

def test_add_product_to_cart_failed(cart, product):
    with pytest.raises(ValueError) as excinfo:
        cart.add_product(product, 11)
    assert str(excinfo.value) == f"Product {product.name} has only {product.available_amount} items"

if __name__ == "__main__":
    pytest.main()