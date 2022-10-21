import logging
import os
from fastapi import FastAPI, status, Response
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

proxies = {
    "http": os.getenv("PROXY_HTTP"),
    "https": os.getenv("PROXY_HTTPS"),
}

app = FastAPI()


@app.get("/products")
def get_available_products(userEmail: str):
    available_products = productsService.get_available_products(userEmail)

    return list(map(__to_product_response, available_products))

@app.get("/products/{productId}")
def product_exists(userEmail: str, productId: str):
    return productsService.product_exists(userEmail, productId)


@app.post("/products/update", status_code=status.HTTP_201_CREATED)
def resilient_update_products_for_all_users(response: Response):
    logger.info(f"Main {resilient_update_products_for_all_users.__name__} invoked")

    
    tokensList = tokensRepository.get_all_tokens()
    
    for tokens in tokensList:
        for _ in range(5):
            try:
                __update_products_for(tokens)
                break
            except Exception as e:
                logger.error(
                    f"An error occurred while updating products for user {tokens.userEmail}. Error: {e}")
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR




@app.post("/products/update")
def update_products_for_user(userEmail: str):
    tokens = tokensRepository.get_tokens(userEmail)
    __update_products_for(tokens)


@app.post("/tokens/update")
def update_tokens(userEmail: str):
    tgtgClient = TooGoodToGoClient(userEmail, proxies)
    credentials = tgtgClient.get_credentials()
    logger.info(f"Gotten credentials {credentials}")

    tokensRepository.update_tokens(
        userEmail, TokenDTO.from_client_tokens(credentials, userEmail))

    return tokensRepository.get_tokens(userEmail)


@app.get("/credentials")
def get_credentials(userEmail: str):

    tgtgClient = TooGoodToGoClient(userEmail, proxies)
    credentials = tgtgClient.get_credentials()
    logger.info(credentials)

    return credentials


@app.get("/ping", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"Success": "Pong!!!!"}


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


def __update_products_for(tokens: TokenDTO):
    tgtgClient = TooGoodToGoClient(
        None, proxies, tokens.accessToken, tokens.refreshToken, tokens.userId)
    products = tgtgClient.get_items()

    logger.info(f"Products from TgTg: {products}")

    domainProducts = __to_products_dto(products)

    productsService.add_or_update_products(tokens.userEmail, domainProducts)


handler = Mangum(app)
