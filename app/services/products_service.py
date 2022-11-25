import logging
from entities.product import ProductDTO
from repositories.products_repository import ProductsRepository


class ProductsService:

    def __init__(self, productsRepository: ProductsRepository):
        self.__initLogging()
        self.logger.info(f"ProductsService Constructor")

        self.productsRepository = productsRepository

    def get_available_products(self, email: str):
        available_products = self.productsRepository.get_available_products(
            email)

        self.productsRepository.update_last_gotten_at(
            email, available_products)

        return available_products

    def product_exists(self, email: str, productId: str) -> bool:
        return self.productsRepository.product_exists(email, productId)

    def add_or_update_products(self, email: str, newProducts: list[ProductDTO]):
        oldProducts = self.productsRepository.get_all_products(email)

        newProductsIds = list(map(lambda product: product.id, newProducts))

        self.productsRepository.add_or_update_products(email, newProducts)

        productsIdsToDelete = list(map(lambda product: product.id, filter(
            lambda product: product.id not in newProductsIds, oldProducts)))

        self.productsRepository.batch_delete_products(
            email, productsIdsToDelete)

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("ProductsService")
        self.logger.setLevel(logging.DEBUG)
