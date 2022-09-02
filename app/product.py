import datetime
from store import Store


class Product:
    def __init__(self, productFromClient):
        self.id = productFromClient["item"]["item_id"]
        self.price = productFromClient["item"]["price_including_taxes"]["minor_units"]
        self.decimals = productFromClient["item"]["price_including_taxes"]["decimals"]
        self.pickupLocation = productFromClient["pickup_location"]["address"]["address_line"]
        self.isAvailable = productFromClient["items_available"] > 0
        self.store = Store(productFromClient["store"])
        self.createdTime = datetime.now()