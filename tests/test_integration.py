import boto3
from app.eshop import Product, ShoppingCart, Order
import random
from services import ShippingService
from datetime import datetime, timedelta, timezone
from services.config import AWS_ENDPOINT_URL, AWS_REGION, SHIPPING_QUEUE
import pytest


def test_when_place_order_then_shipping_in_queue(dynamo_resource):
    shipping_service = ShippingService()
    cart = ShoppingCart()

    cart.add_product(Product(
        available_amount=10,
        name='Product',
        price=random.random() * 10000),
        amount=9
    )

    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(seconds=3)
    )

    sqs_client = boto3.client(
        "sqs",
        endpoint_url=AWS_ENDPOINT_URL,
        region_name=AWS_REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    queue_url = sqs_client.get_queue_url(QueueName=SHIPPING_QUEUE)["QueueUrl"]
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get("Messages", [])
    assert len(messages) == 1, "Expected 1 SQS message"

    body = messages[0]["Body"]
    assert shipping_id == body


def test_place_order_with_unavailable_shipping_type_fails(dynamo_resource):
    shipping_service = ShippingService()
    cart = ShoppingCart()
    cart.add_product(Product(
        available_amount=10,
        name='Product',
        price=random.random() * 10000),
        amount=9
    )
    order = Order(cart, shipping_service)
    shipping_id = None

    with pytest.raises(ValueError) as excinfo:
        shipping_id = order.place_order(
            "Новий тип доставки",
            due_date=datetime.now(timezone.utc) + timedelta(seconds=3)
        )
    assert shipping_id is None, "Shipping id must not be assigned"
    assert "Shipping type is not available" in str(excinfo.value)
