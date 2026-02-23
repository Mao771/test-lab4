import random

import boto3
from services import ShippingService
from services.publisher import ShippingPublisher

from services.repository import ShippingRepository
from services.config import AWS_ENDPOINT_URL, AWS_REGION, SHIPPING_TABLE_NAME, SHIPPING_QUEUE
from .eshop import Product, ShoppingCart, Order, Shipment
from datetime import datetime, timedelta, timezone
from time import sleep

due_date = datetime.now(timezone.utc) + timedelta(seconds=10)
ts = due_date.replace(tzinfo=timezone.utc).isoformat()
print(due_date, due_date + timedelta(seconds=3))


sqs_client = boto3.client(
    "sqs",
    endpoint_url=AWS_ENDPOINT_URL,    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)
dynamo_client = boto3.client(
    "dynamodb",
    endpoint_url=AWS_ENDPOINT_URL,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

response = sqs_client.create_queue(QueueName=SHIPPING_QUEUE)
queue_url = response["QueueUrl"]
existing_tables = dynamo_client.list_tables()["TableNames"]
if SHIPPING_TABLE_NAME not in existing_tables:
    dynamo_client.create_table(
        TableName=SHIPPING_TABLE_NAME,
        KeySchema=[{"AttributeName": "shipping_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "shipping_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    dynamo_client.get_waiter("table_exists").wait(TableName=SHIPPING_TABLE_NAME)

shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
shipments = []

for j in range(1, 12):
    cart = ShoppingCart()

    for i in range(1, 10):
        cart.add_product(Product(
            available_amount=i,
            name=f'Product_{j}_{i}',
            price=random.random() * 10000),
            amount=i
        )






    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(seconds=3)
    )

    shipments.append(Shipment(shipping_id, shipping_service))

while True:
    result = shipping_service.process_shipping_batch()
    print(len(result))

    for shipment in shipments:
        print("Shipment", shipment.shipping_id, shipment.check_shipping_status())

    if not result:
        break
    sleep(3)

dynamo_client.delete_table(TableName=SHIPPING_TABLE_NAME)
sqs_client.delete_queue(QueueUrl=queue_url)
