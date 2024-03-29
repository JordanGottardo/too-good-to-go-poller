import datetime
import logging
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

from entities.tokens import TokenDTO


class DynamoDbTokensClient:

    def __init__(self):
        self.__init_logging()

        self.logger.info(f"DynamoDbTokensClient Constructor")

    def get_all_tokens(self) -> list[TokenDTO]:
        tokensTable = self.__get_tokens_table()

        response = tokensTable.scan()

        self.logger.info(
            f"DynamoDbTokensClient got response from DynamoDB: {response}")

        return list(map(lambda t : TokenDTO.from_db_tokens(t), response["Items"]))

    def get_tokens(self, email: str) -> TokenDTO:
        tokensTable = self.__get_tokens_table()

        response = tokensTable.query(
            KeyConditionExpression=Key('email').eq(email))

        self.logger.info(
            f"DynamoDbTokensClient got response from DynamoDB: {response}")

        if not response["Items"]:
            return None
        
        item = response["Items"][0]
        return TokenDTO.from_db_tokens(item)

    def update_tokens(self, email: str, tokens: TokenDTO):
        tokensTable = self.__get_tokens_table()

        response = tokensTable.update_item(
            Key={
                "email": email
            },
            UpdateExpression="set accessToken=:accessToken, refreshToken=:refreshToken, userId=:userId, cookie=:cookie, lastUpdatedAt=:lastUpdatedAt",
            ExpressionAttributeValues={
                ":accessToken": tokens.accessToken, ":refreshToken": tokens.refreshToken, ":userId": tokens.userId, ":cookie":tokens.cookie,  ":lastUpdatedAt": datetime.now().isoformat()})

    def __get_tokens_table(self):
        dynamoDb = boto3.resource("dynamodb")
        return dynamoDb.Table("tgtgTokens")

    def __init_logging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("DynamoDbTokensClient")
        self.logger.setLevel(logging.DEBUG)
