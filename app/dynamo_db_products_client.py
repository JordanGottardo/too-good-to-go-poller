from datetime import datetime, timedelta
import logging
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

from product import ProductDTO


class DynamoDbProductsClient:

    def __init__(self):
        self.__init_logging()

        self.logger.info(f"DynamoDbProductsClient Constructor")

    def get_available_products(self, email: str) -> list[ProductDTO]:
        productsTable = self.__get_products_table()

        lastGottenAtAttribute = Attr("lastGottenAt")
        isAvailableAttribute = Attr("isAvailable")

        oneDayAgo = datetime.now() - timedelta(days=1)

        response = productsTable.query(
            KeyConditionExpression=Key('email').eq(email),
            FilterExpression=isAvailableAttribute.eq(True) & (lastGottenAtAttribute.eq(
                None) | lastGottenAtAttribute.lt(oneDayAgo.isoformat()))
        )

        return list(map(lambda p: ProductDTO.from_db_product(p), response["Items"]))

    def product_exists(self, email: str, productId: str) -> bool:
        productsTable = self.__get_products_table()

        response = productsTable.get_item(
            Key={
                "email": email, "productId": productId
            },
            ProjectionExpression="productId")

        self.logger.info(f"get response={response}")
        
        return True

    def add_product(self, email, product: ProductDTO):
        productsTable = self.__get_products_table()

        response = productsTable.update_item(
            Key={
                "email": email, "productId": product.id
            },
            UpdateExpression="set storeName=:storeName, storeAddress=:storeAddress, isAvailable=:isAvailable,  lastUpdatedAt=:lastUpdatedAt, lastGottenAt=:lastGottenAt, price=:price, decimals=:decimals, pickupLocation=:pickupLocation, storeCity=:storeCity",
            ExpressionAttributeValues={
                ":storeName": product.store.name, ":storeAddress": product.store.address, ":isAvailable": product.isAvailable, ":lastUpdatedAt": datetime.now().isoformat(), ":lastGottenAt": None, ":price": product.price, ":decimals": product.decimals, ":pickupLocation": product.pickupLocation, ":storeCity": product.store.city, })

    def update_product(self, email, product: ProductDTO):
        productsTable = self.__get_products_table()

        response = productsTable.update_item(
            Key={
                "email": email, "productId": product.id
            },
            UpdateExpression="set storeName=:storeName, storeAddress=:storeAddress, isAvailable=:isAvailable,  lastUpdatedAt=:lastUpdatedAt, price=:price, decimals=:decimals, pickupLocation=:pickupLocation, storeCity=:storeCity",
            ExpressionAttributeValues={
                ":storeName": product.store.name, ":storeAddress": product.store.address, ":isAvailable": product.isAvailable, ":lastUpdatedAt": datetime.now().isoformat(), ":price": product.price, ":decimals": product.decimals, ":pickupLocation": product.pickupLocation, ":storeCity": product.store.city, })

    def update_last_gotten_at(self, email: str, product: ProductDTO):
        productsTable = self.__get_products_table()
        print(product)
        response = productsTable.update_item(
            Key={
                "email": email, "productId": product.id
            },
            UpdateExpression="set lastGottenAt=:lastGottenAt",
            ExpressionAttributeValues={
                ":lastGottenAt": datetime.now().isoformat()})

    def __get_products_table(self):
        dynamoDb = boto3.resource("dynamodb")
        return dynamoDb.Table("tgtgProducts")

    def test(self):
        productsTable = self.__get_products_table()

        productsTable.update_item(
            Key={
                "email": "jordangottardo@libero.it", "productId": "389956"
            },
            UpdateExpression="set lastGottenAt=:lastGottenAt",
            ExpressionAttributeValues={
                ":lastGottenAt": str(datetime.now().isoformat())})

    def test2(self):
        productsTable = self.__get_products_table()

        productsTable.update_item(
            Key={
                "email": "jordangottardo@libero.it", "productId": "389956"
            },
            UpdateExpression="set lastGottenAt=:lastGottenAt",
            ExpressionAttributeValues={
                ":lastGottenAt": None})

    def test3(self):
        productsTable = self.__get_products_table()

        oneDayAgo = datetime.now() - timedelta(days=1)

        response = productsTable.query(
            KeyConditionExpression=Key('email').eq("jordangottardo@libero.it"),
            FilterExpression=Attr('lastGottenAt').exists() & Attr('lastGottenAt').ne(
                None) & Attr('lastGottenAt').lt(oneDayAgo.isoformat())
        )

        return response["Items"]

    def __init_logging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("DynamoDbProductsClient")
        self.logger.setLevel(logging.DEBUG)
