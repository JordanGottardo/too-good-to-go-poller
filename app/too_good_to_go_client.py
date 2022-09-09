import logging
from tgtg import TgtgClient


class TooGoodToGoClient:

    def __init__(self, email):
        self.__initLogging()

        self.logger.info(
            f"TooGoodToGoClient Constructor: initializing for user {email}")

        self.email = email
        self.client = TgtgClient(email=email)

    def __init__(self, accessToken, refreshToken, userId):
        self.__initLogging()

        self.logger.info(
            f"TooGoodToGoClient Constructor: initializing for user with id {userId}, access token {accessToken}, refresh token {refreshToken}")

        self.client = TgtgClient(
            access_token=accessToken, refresh_token=refreshToken, user_id=userId)

    def get_items(self):
        return self.client.get_items()

    def get_credentials(self):
        return self.client.get_credentials()

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("TooGoodToGoClient")
        self.logger.setLevel(logging.DEBUG)
