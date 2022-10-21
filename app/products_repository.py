import logging
from product import ProductDTO

from dynamo_db_products_client import DynamoDbProductsClient


class ProductsRepository:

    def __init__(self, productsClient: DynamoDbProductsClient):
        self.__initLogging()
        self.logger.info(f"ProductsRepository Constructor")

        self.productsClient = productsClient

    def get_available_products(self, email: str) -> list[ProductDTO]:
        return self.productsClient.get_available_products(email)

    def product_exists(self, email:str, productId: str) -> bool:
        return self.productsClient.product_exists(email, productId)

    def add_or_update_product(self, email: str, product: ProductDTO):
        return self.productsClient.add_product(email, product)

    def add_or_update_products(self, email: str, products: list[ProductDTO]):
        for product in products:
            self.logger.info(
                f"ProductsRepository add_or_update_products {product}")
            self.add_or_update_product(email, product)

    def update_last_gotten_at(self, email: str, products: list[ProductDTO]):
        for product in products:
            self.productsClient.update_last_gotten_at(email, product)

    def test(self):
        return self.productsClient.test()

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("ProductsRepository")
        self.logger.setLevel(logging.DEBUG)
