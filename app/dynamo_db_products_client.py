import logging
import boto3
from boto3.dynamodb.conditions import Key


class DynamoDbProductsClient:

    def __init__(self):
        self.__init_logging()

        self.logger.info(f"DynamoDbProductsClient Constructor")

    def get_products(self, email: str):
        productsTable = self.__get_products_table()

        response = productsTable.query(
            KeyConditionExpression=Key('email').eq(email))

        self.logger.info(
            f"DynamoDbProductsClient got response from DynamoDB: {response}")

        products = response["Items"]

        return products

    def add_or_update_product(self, email, product):
        productsTable = self.__get_products_table()

        response = productsTable.update_item(
            Key={
                "email": email, "productId": 1
            },
            UpdateExpression="set info.price=:p, info.description=:n",
            ExpressionAttributeValues={
                ":p": "10", ":n": "myDescription"})

    def __get_products_table(self):
        dynamoDb = boto3.resource("dynamodb")
        return dynamoDb.Table("tgtgProducts")

    def __init_logging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("DynamoDbProductsClient")
        self.logger.setLevel(logging.DEBUG)
