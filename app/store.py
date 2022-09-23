class Store:
    def __init__(self, storeFromClient):
        self.name = storeFromClient["store_name"]
        self.address = storeFromClient["store_location"]["address"]["address_line"]
        self.city = storeFromClient["store_location"]["address"]["city"]

    def __init__(self, name, address, city):
        self.name = name
        self.address = address
        self.city = city