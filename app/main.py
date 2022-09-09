import logging
import string
from fastapi import FastAPI
from mangum import Mangum
import boto3
from dynamo_db_products_client import DynamoDbProductsClient
from products_repository import ProductsRepository
from .tokens.dynamo_db_tokens_client import DynamoDbTokensClient
from .tokens.tokens_repository import TokensRepository


from too_good_to_go_client import TooGoodToGoClient


logging.basicConfig(format="%(threadName)s:%(message)s")
logger = logging.getLogger("Controller")
logger.setLevel(logging.DEBUG)

logger.info("I setup complete")
logger.debug("D setup complete")
email = "jordangottardo@libero.it"
productsClient = DynamoDbProductsClient()
productsRepository = ProductsRepository(productsClient)

tokensClient = DynamoDbTokensClient()
tokensRepository = TokensRepository(tokensClient)

app = FastAPI()


@app.get("/products")
def get_products():
    return productsRepository.get_products(email)


@app.post("/products/update")
def update_products():
    productsRepository.add_or_update_product(email, {})


@app.get("/tokens")
def get_tokens():
    return tokensRepository.get_tokens(email)


@app.get("/credentials")
def get_credentials():

    tgtgClient = TooGoodToGoClient(email)
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


handler = Mangum(app)
