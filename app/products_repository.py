import logging
from product import Product

from dynamo_db_products_client import DynamoDbProductsClient



class ProductsRepository:

    def __init__(self, productsClient: DynamoDbProductsClient):
        self.__initLogging()
        self.logger.info(f"ProductsRepository Constructor")

        self.productsClient = productsClient

    def get_products(self, email: str):
        return self.productsClient.get_products(email)

    def add_or_update_product(self, email: str, product: Product):
        return self.productsClient.add_or_update_product(email, product)

    def add_or_update_products(self, email: str, products: list[Product]):
        for product in products:
            self.logger.info(f"ProductsRepository add_or_update_products {product}")
            self.add_or_update_product(email, product)

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("ProductsRepository")
        self.logger.setLevel(logging.DEBUG)
