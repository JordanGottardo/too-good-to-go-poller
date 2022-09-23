from datetime import datetime
from store import Store


class ProductDTO(object):
    def __init__(self, productFromClient=None, productFromDb=None):
        if (productFromClient is not None):
            self.id = productFromClient["item"]["item_id"]
            self.price = productFromClient["item"]["price_including_taxes"]["minor_units"]
            self.decimals = productFromClient["item"]["price_including_taxes"]["decimals"]
            self.pickupLocation = productFromClient["pickup_location"]["address"]["address_line"]
            self.isAvailable = productFromClient["items_available"] > 0
            self.store = Store(productFromClient["store"])

        if (productFromDb is not None):
            self.id = productFromDb["productId"]
            self.price = productFromDb["price"]
            self.decimals = productFromDb["decimals"]
            self.pickupLocation = productFromDb["pickupLocation"]
            self.isAvailable = productFromDb["isAvailable"]
            self.store = Store(
                productFromDb["storeName"], productFromDb["storeAddress"], productFromDb["storeCity"])
            self.lastGottenAt = productFromDb["lastGottenAt"]
            self.lastUpdatedAt = productFromDb["lastUpdatedAt"]

    @classmethod
    def from_client_product(cls, productFromClient):
        return cls(productFromClient)

    @classmethod
    def from_db_product(cls, productFromDb):
        return cls(None, productFromDb)
