from app.eshop import Product, ShoppingCart, Order
from unittest.mock import MagicMock
import unittest


def test_add_product():
    product = Product(name="Test", available_amount=10, price=100)
    cart = ShoppingCart()
    product.is_available = MagicMock()
    cart.add_product(product, 10)
    product.is_available.assert_called_with(10)


if __name__ == '__main__':
    unittest.main()
