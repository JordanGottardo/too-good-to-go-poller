import logging
import boto3


class DynamoDbProductsClient:

    def __init__(self):
        self.__initLogging()

        self.logger.info(f"DynamoDbProductsClient Constructor")

    def get_items(self, email: str):
        dynamodb_client = boto3.client("dynamodb")

        response = dynamodb_client.get_item(
            TableName="tgtgProducts",
            Key={
                'email': {'S': email}
            })

        self.logger.info(f"DynamoDbProductsClient got response from DynamoDB: {response}")

        items = response["Item"]
      
        return items
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
