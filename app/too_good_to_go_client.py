import logging
from tgtg import TgtgClient


class TooGoodToGoClient:

    def __init__(self, email):
        self.__initLogging()

        self.logger.info(
            f"TooGoodToGoClient Constructor: initializing for user {email}")

        self.email = email
        self.client = TgtgClient(email=email)

    def get_items(self):
        return self.client.get_items()

    def get_credentials(self):
        return self.client.get_credentials()

    def __initLogging(self):
        logging.basicConfig(format="%(threadName)s:%(message)s")
        self.logger = logging.getLogger("TooGoodToGoClient")
        self.logger.setLevel(logging.DEBUG)
