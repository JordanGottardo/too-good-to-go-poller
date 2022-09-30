import logging
from tgtg import TgtgClient


class TooGoodToGoClient:

    def __init__(self, email, proxies, accessToken=None, refreshToken=None, userId=None):
        self.__initLogging()

        if (accessToken is not None):
            self.logger.info(
                f"TooGoodToGoClient Constructor: initializing for user with id {userId}, access token {accessToken}, refresh token {refreshToken}")
            self.client = TgtgClient(
                access_token=accessToken, refresh_token=refreshToken, user_id=userId, proxies=proxies)
        else:
            self.logger.info(
                f"TooGoodToGoClient Constructor: initializing for user with email {email}")
            self.email = email
            self.client = TgtgClient(email=email, proxies=proxies)

    def get_items(self):
        return self.client.get_items()

    def get_credentials(self):
        return self.client.get_credentials()

    def get_credentials_fake(self):
        return {"access_token": 1, "refresh_token": 2, "user_id": 3}

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("TooGoodToGoClient")
        self.logger.setLevel(logging.DEBUG)
