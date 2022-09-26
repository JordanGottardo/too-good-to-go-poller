class TokenDTO(object):
    def __init__(self, tokensFromClient=None, tokensFromDatabase=None):

        if (tokensFromClient is not None):
            self.accessToken = tokensFromClient["access_token"]
            self.refreshToken = tokensFromClient["refresh_token"]
            self.userId = tokensFromClient["user_id"]

        if (tokensFromDatabase is not None):
            self.accessToken = tokensFromDatabase["accessToken"]
            self.refreshToken = tokensFromDatabase["refreshToken"]
            self.userId = tokensFromDatabase["userId"]


    @classmethod
    def from_client_tokens(cls, tokensFromClient):
        return cls(tokensFromClient)

    @classmethod
    def from_db_tokens(cls, tokensFromDb):
        return cls(None, tokensFromDb)
