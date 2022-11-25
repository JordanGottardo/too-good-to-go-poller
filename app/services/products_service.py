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

        for newProduct in newProducts:
            self.logger.info(f"New product: {newProduct}")

        newProductsIds = list(map(lambda product: product.id, newProducts))

        self.productsRepository.add_or_update_products(email, newProducts)

        self.logger.info(f"Added products ids {newProductsIds}")
        for newProductId in newProductsIds:
            self.logger.info(f"Added product id: {newProductId}")

        productsIdsToDelete = list(map(lambda product: product.id, filter(
            lambda product: product.id not in newProductsIds, oldProducts)))

        self.logger.info(f"Will delete product ids {productsIdsToDelete}")
        for productIdToDelete in productsIdsToDelete:
            self.logger.info(f"Will delete product id: {productIdToDelete}")

        self.productsRepository.batch_delete_products(
            email, productsIdsToDelete)

    def test(self):
        return self.productsRepository.batch_delete_products("jordangottardo@libero.it", ["530766", "569352"])

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("ProductsService")
        self.logger.setLevel(logging.DEBUG)
