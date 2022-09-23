from datetime import datetime
from store import Store


class ProductEntity:
    def __init__(self, productFromDb):
        self.storeCity = productFromDb["storeCity"]
        self.pickupLocation = productFromDb["pickupLocation"]
        self.lastGottenAt = productFromDb["lastGottenAt"]
        self.decimals = productFromDb["decimals"]
        self.storeName = productFromDb["storeName"]
        self.lastUpdatedAt = productFromDb["lastUpdatedAt"]
        self.price = productFromDb["price"]
        self.storeAddress = productFromDb["storeAddress"]
        self.isAvailable = productFromDb["isAvailable"]
        self.id = productFromDb["productId"]
