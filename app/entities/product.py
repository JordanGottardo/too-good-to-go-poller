from datetime import datetime
from entities.store import Store


class ProductDTO(object):
    def __init__(self, productFromClient=None, productFromDb=None):
        if (productFromClient is not None):
            self.id = productFromClient["item"]["item_id"]
            self.price = productFromClient["item"]["price_including_taxes"]["minor_units"]
            self.decimals = productFromClient["item"]["price_including_taxes"]["decimals"]
            self.pickupLocation = productFromClient["pickup_location"]["address"]["address_line"]
            self.isAvailable = productFromClient["items_available"] > 0
            store = productFromClient["store"]
            
            self.store = Store(store["store_name"], store["store_location"]["address"]["address_line"], store["store_location"]["address"]["city"])

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

    def __str__(self):
     return f"id: {self.id}, pickupLocation= {self.pickupLocation}, storeName={self.store.name}"

    @classmethod
    def from_client_product(cls, productFromClient):
        return cls(productFromClient)

    @classmethod
    def from_db_product(cls, productFromDb):
        return cls(None, productFromDb)
