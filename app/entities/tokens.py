class TokenDTO(object):
    def __init__(self, tokensFromClient=None, tokensFromDatabase=None, userEmail=None):

        if (tokensFromClient is not None):
            self.accessToken = tokensFromClient["access_token"]
            self.refreshToken = tokensFromClient["refresh_token"]
            self.userId = tokensFromClient["user_id"]
            self.cookie = tokensFromClient["cookie"]
            self.userEmail = userEmail

        if (tokensFromDatabase is not None):
            self.accessToken = tokensFromDatabase["accessToken"]
            self.refreshToken = tokensFromDatabase["refreshToken"]
            self.userId = tokensFromDatabase["userId"]
            self.userEmail = tokensFromDatabase["email"]
            self.cookie = tokensFromClient["cookie"]


    @classmethod
    def from_client_tokens(cls, tokensFromClient, email):
        return cls(tokensFromClient, None, email)

    @classmethod
    def from_db_tokens(cls, tokensFromDb):
        return cls(None, tokensFromDb)
