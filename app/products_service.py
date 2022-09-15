from datetime import datetime
import logging
from product import ProductDTO
from products_repository import ProductsRepository


class ProductsService:

    def __init__(self, productsRepository: ProductsRepository):
        self.__initLogging()
        self.logger.info(f"ProductsService Constructor")

        self.productsRepository = productsRepository

    def get_available_products(self, email: str):
        available_products = self.productsRepository.get_available_products(
            email)

        self.productsRepository.add_or_update_products(available_products)

        return available_products

    def add_or_update_product(self, email: str, product: ProductDTO):
        return self.productsRepository.add_or_update_product(email, product)

    def add_or_update_products(self, email: str, products: list[ProductDTO]):
        return self.productsRepository.add_or_update_products(email, products)

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("ProductsService")
        self.logger.setLevel(logging.DEBUG)
