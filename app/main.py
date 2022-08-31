import logging
import string
from fastapi import FastAPI
from mangum import Mangum
import boto3

from too_good_to_go_client import TooGoodToGoClient


logging.basicConfig(format="%(threadName)s:%(message)s")
logger = logging.getLogger("Controller")
logger.setLevel(logging.DEBUG)

logger.info("I setup complete")
logger.debug("D setup complete")

app = FastAPI()


@app.get("/items")
def get_items():
    # tgtgClient = TooGoodToGoClient("jordangottardo@libero.it")
    # items = tgtgClient.get_items()
    # logger.info(items)
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.get_item(
        TableName="tgtgTokens",
        Key={
            'email': {'S': 'test@gmail.com'}
        }
    )
    print(response['Item'])

    return {"message": "Hello World"}


@app.get("/credentials")
def get_credentials():
    email = "jordangottardo@libero.it"
    get_record_from_tokens_table(email)
    tgtgClient = TooGoodToGoClient(email)
    credentials = tgtgClient.get_credentials()
    logger.info(credentials)


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
