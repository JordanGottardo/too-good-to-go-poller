class TokenDTO(object):
    def __init__(self, tokensFromClient):
        self.accessToken = tokensFromClient["accessToken"]
        self.refreshToken = tokensFromClient["refreshToken"]
        self.userId = tokensFromClient["userId"]
