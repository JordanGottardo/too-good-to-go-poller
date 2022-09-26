import logging
from fastapi import FastAPI
from mangum import Mangum
from tokens import TokenDTO
from products_service import ProductsService
from product import ProductDTO
from dynamo_db_products_client import DynamoDbProductsClient
from products_repository import ProductsRepository
from dynamo_db_tokens_client import DynamoDbTokensClient
from tokens_repository import TokensRepository


from too_good_to_go_client import TooGoodToGoClient


logging.basicConfig(format="%(threadName)s:%(message)s")
logger = logging.getLogger("Controller")
logger.setLevel(logging.DEBUG)

logger.info("I setup complete")
logger.debug("D setup complete")
productsClient = DynamoDbProductsClient()
productsRepository = ProductsRepository(productsClient)
productsService = ProductsService(productsRepository)

tokensClient = DynamoDbTokensClient()
tokensRepository = TokensRepository(tokensClient)

app = FastAPI()


@app.get("/products")
def get_available_products(userEmail: str):
    available_products = productsService.get_available_products(userEmail)

    return list(map(__to_product_response, available_products))


@app.post("/products/update")
def update_products(userEmail: str):
    tokens = tokensRepository.get_tokens(userEmail)
    tgtgClient = TooGoodToGoClient(
        None, tokens["accessToken"], tokens["refreshToken"], tokens["userId"])
    products = tgtgClient.get_items()

    logger.info(f"Products from TgTg: {products}")

    domainProducts = __to_products_dto(products)

    productsService.add_or_update_products(userEmail, domainProducts)


@app.post("/tokens/update")
def update_tokens(userEmail: str):
    tgtgClient = TooGoodToGoClient(userEmail)
    credentials = tgtgClient.get_credentials_fake()
    logger.info(credentials)

    tokensRepository.update_tokens(userEmail, TokenDTO.from_client_tokens(credentials))

    return tokensRepository.get_tokens(userEmail)


@app.get("/credentials")
def get_credentials(userEmail: str):

    tgtgClient = TooGoodToGoClient(userEmail)
    credentials = tgtgClient.get_credentials()
    logger.info(credentials)

    return credentials


@app.post("/test")
def test():
    productsService.test()


@app.post("/test2")
def test():
    productsClient.test2()


@app.post("/test3")
def test():
    return productsClient.test3()


@app.get("/ping", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"Success": "Pong!!!!"}

@app.get("/", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck2():
    return {"Success2": "Pong2!!!!"}

def __to_products_dto(products):
    return map(__to_product_dto, products)


def __to_product_dto(product):
    return ProductDTO(product)


def __to_product_response(product: ProductDTO):

    return {
        "productId": product.id,
        "price": product.price,
        "decimals": product.decimals,
        "isAvailable": product.isAvailable,
        "lastGottenAt": product.lastGottenAt,
        "lastUpdateAt": product.lastUpdatedAt,
        "storeName": product.store.name

    }


handler = Mangum(app)
