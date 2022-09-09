import logging
from dynamo_db_tokens_client import DynamoDbTokensClient

class TokensRepository:

    def __init__(self, tokensClient: DynamoDbTokensClient):
        self.__initLogging()
        self.logger.info(f"TokensRepository Constructor")

        self.tokensClient = tokensClient

    def get_tokens(self, email: str):
        return self.tokensClient.get_tokens(email)

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("TokensRepository")
        self.logger.setLevel(logging.DEBUG)
