import logging

from dynamo_db_products_client import DynamoDbProductsClient


class ProductsRepository:

    def __init__(self, productsClient: DynamoDbProductsClient):
        self.__initLogging()
        self.logger.info(f"ProductsRepository Constructor")

        self.productsClient = productsClient

    def get_products(self, email: str):
        return self.productsClient.get_products(email)

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("ProductsRepository")
        self.logger.setLevel(logging.DEBUG)
