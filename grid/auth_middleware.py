import falcon


class AuthMiddleware:

    def __init__(self, token, account_id):
        self.token = token
        self.account_id = account_id

    async def process_request(self, req, resp):
        token = req.get_header('Authorization')
        account_id = req.get_header('Account-ID')

        challenges = ['Token type="Fernet"']

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized(title='Auth token required',
                                          description=description,
                                          challenges=challenges,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token, account_id):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized(title='Authentication required',
                                          description=description,
                                          challenges=challenges,
                                          href='http://docs.example.com/auth')

    def _token_is_valid(self, token, account_id):
        return True  # Suuuuuure it's valid...
