import logging
import string
from fastapi import FastAPI
from mangum import Mangum
import boto3
from products_service import ProductsService
from product import Product
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
def get_products(userEmail: str):
    return productsRepository.get_products(userEmail)


@app.post("/products/update")
def update_products(userEmail: str):
    tokens = tokensRepository.get_tokens(userEmail)
    tgtgClient = TooGoodToGoClient(
        tokens["accessToken"], tokens["refreshToken"], tokens["userId"])
    products = tgtgClient.get_items()

    logger.info(f"Products from TgTg: {products}")

    domainProducts = __to_domain_products(products)

    productsService.add_or_update_products(userEmail, domainProducts)


@app.get("/tokens")
def get_tokens(userEmail: str):
    return tokensRepository.get_tokens(userEmail)


@app.get("/credentials")
def get_credentials(userEmail: str):

    tgtgClient = TooGoodToGoClient(userEmail)
    credentials = tgtgClient.get_credentials()
    logger.info(credentials)

    return credentials


@app.get("/ping", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"Success": "Pong!!!!"}


def get_record_from_tokens_table(email: string):
    dynamodb_client = boto3.client("dynamodb")

    response = dynamodb_client.get_item(
        TableName="tgtgTokens",
        Key={
            'email': {'S': email}
        })

    print(response)

    item = response["Item"]
    return {
        "email": item["email"]["S"],
        "accessToken": item["accessToken"]["S"],
        "refreshToken": item["refreshToken"]["S"],
        "userId": item["userId"]["S"]
    }


def __to_domain_products(products):
    return map(__to_domain_product, products)


def __to_domain_product(product):
    return Product(product)


handler = Mangum(app)
