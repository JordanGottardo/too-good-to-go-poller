import logging
import boto3


class DynamoDbProductsClient:

    def __init__(self):
        self.__initLogging()

        self.logger.info(f"DynamoDbProductsClient Constructor")

    def get_products(self, email: str):
        dynamoDb = boto3.resource("dynamodb")
        
        # response = dynamodb_client.get_item(
        #     TableName="tgtgProducts",
        #     Key={
        #         'email': {'S': email}
        #     })
        productsTable = dynamoDb.Table("tgtgProducts")

        response = productsTable.query(
            KeyConditionExpression=Key('email').eq(email))

        self.logger.info(
            f"DynamoDbProductsClient got response from DynamoDB: {response}")

        products = response["Items"]

        return products
        # {
        # "email": item["email"]["S"],
        # "accessToken": item["accessToken"]["S"],
        # "refreshToken": item["refreshToken"]["S"],
        # "userId": item["userId"]["S"]
        # }

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("DynamoDbProductsClient")
        self.logger.setLevel(logging.DEBUG)
