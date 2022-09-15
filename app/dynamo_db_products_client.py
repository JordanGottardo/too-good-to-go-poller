from datetime import datetime
import logging
import boto3
from boto3.dynamodb.conditions import Key

from product import Product


class DynamoDbProductsClient:

    def __init__(self):
        self.__init_logging()

        self.logger.info(f"DynamoDbProductsClient Constructor")

    def get_available_products(self, email: str):
        productsTable = self.__get_products_table()

        response = productsTable.query(
            KeyConditionExpression=Key('email').eq(email))

        self.logger.info(
            f"DynamoDbProductsClient got response from DynamoDB: {response}")

        products = response["Items"]

        return products

    def add_or_update_product(self, email, product: Product):
        productsTable = self.__get_products_table()

        response = productsTable.update_item(
            Key={
                "email": email, "productId": product.id
            },
            UpdateExpression="set storeName=:storeName, storeAddress=:storeAddress, isAvailable=:isAvailable,  lastUpdatedAt=:lastUpdatedAt, lastGottenAt=:lastGottenAt price=:price, decimals=:decimals, pickupLocation=:pickupLocation, storeCity=:storeCity",
            ExpressionAttributeValues={
                ":storeName": product.store.name, ":storeAddress": product.store.address, ":isAvailable": product.isAvailable, ":lastUpdatedAt": str(product.createdTime), ":lastGottenAt": None, ":price": product.price, ":decimals": product.decimals, ":pickupLocation": product.pickupLocation, ":storeCity": product.store.city, })

    def __get_products_table(self):
        dynamoDb = boto3.resource("dynamodb")
        return dynamoDb.Table("tgtgProducts")

    def __init_logging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("DynamoDbProductsClient")
        self.logger.setLevel(logging.DEBUG)
