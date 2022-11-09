import logging
from entities.tokens import TokenDTO
from clients.dynamo_db_tokens_client import DynamoDbTokensClient


class TokensRepository:

    def __init__(self, tokensClient: DynamoDbTokensClient):
        self.__initLogging()
        self.logger.info(f"TokensRepository Constructor")

        self.tokensClient = tokensClient

    def get_all_tokens(self) -> list[TokenDTO]:
        return self.tokensClient.get_all_tokens()

    def get_tokens(self, email: str) -> TokenDTO:
        return self.tokensClient.get_tokens(email)

    def update_tokens(self, email: str, tokens: TokenDTO):
        return self.tokensClient.update_tokens(email, tokens)

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("TokensRepository")
        self.logger.setLevel(logging.DEBUG)
