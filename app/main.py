import asyncio
import logging
import os
from fastapi import FastAPI, status, Response
from mangum import Mangum
from entities.tokens import TokenDTO
from services.products_service import ProductsService
from entities.product import ProductDTO
from clients.dynamo_db_products_client import DynamoDbProductsClient
from repositories.products_repository import ProductsRepository
from clients.dynamo_db_tokens_client import DynamoDbTokensClient
from repositories.tokens_repository import TokensRepository


from clients.too_good_to_go_client import TooGoodToGoClient


MAX_RETRIES_COUNT = 5
RETRY_SLEEP_IN_SECONDS = 15

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
async def resilient_update_products_for_all_users(response: Response):
    logger.info(
        f"Main {resilient_update_products_for_all_users.__name__} invoked")

    allUsersCompleted = True

    tokensList = tokensRepository.get_all_tokens()

    for userTokens in tokensList:
        singleUserCompleted = False
        for i in range(MAX_RETRIES_COUNT):
            try:
                __update_products_for(userTokens)
                singleUserCompleted = True
                break
            except Exception as e:
                logger.error(
                    f"[Try {i+1}/{MAX_RETRIES_COUNT}] An error occurred while updating products for user {userTokens.userEmail}. Error: {e}")
                await asyncio.sleep(RETRY_SLEEP_IN_SECONDS)

        allUsersCompleted = allUsersCompleted and singleUserCompleted

    if not allUsersCompleted:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.post("/products/update")
def update_products_for_user(userEmail: str):
    tokens = tokensRepository.get_tokens(userEmail)
    __update_products_for(tokens)


@app.get("/tokens")
def get_tokens(userEmail: str, response: Response):
    try:
        tokens = tokensRepository.get_tokens(userEmail)

        if not tokens:
            response.status_code = status.HTTP_404_NOT_FOUND
            return

        return tokens
    except Exception as e:
        logger.error(
            f"An error occurred while retrieving tokens for user {userEmail}. Error: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.post("/tokens/update")
async def resilient_update_tokens(userEmail: str, response: Response):
    logger.info(f"Updating tokens for user {userEmail}")

    tgtgClient = TooGoodToGoClient(userEmail, proxies)
    for i in range(MAX_RETRIES_COUNT):
        try:
            credentials = tgtgClient.get_credentials()
            logger.info(f"Gotten credentials {credentials}")

            tokensRepository.update_tokens(
                userEmail, TokenDTO.from_client_tokens(credentials, userEmail))

            return tokensRepository.get_tokens(userEmail)

        except Exception as e:
            logger.error(
                f"[Try {i+1}/{MAX_RETRIES_COUNT}] An error occurred while updating tokens for user {userEmail}. Error: {e}")
            await asyncio.sleep(RETRY_SLEEP_IN_SECONDS)
    
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    logger.info(f"Successfully updated tokens for user {userEmail}")


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
    return list(map(__to_product_dto, products))


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
        None, proxies, tokens.accessToken, tokens.refreshToken, tokens.userId, tokens.cookie)
    products = tgtgClient.get_items()

    logger.info(f"Products from TgTg: {products}")

    domainProducts = __to_products_dto(products)

    productsService.add_or_update_products(tokens.userEmail, domainProducts)


handler = Mangum(app)
