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
email = "jordangottardo@libero.it"

app = FastAPI()


@app.get("/items")
def get_items():
    tokens = get_record_from_tokens_table(email)
    tgtgClient = TooGoodToGoClient(tokens["accessToken"], tokens["refreshToken"], tokens["userId"])
    items = tgtgClient.get_items()
    logger.info(items)

    return {"items": items}


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
