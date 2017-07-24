from rest_framework.authentication import TokenAuthentication

from wifidb.settings import AUTH_API_KEY_PARAM


class TokenAuthSupportQueryString(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?key=<token_key>"
    """

    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        if AUTH_API_KEY_PARAM in request.query_params:
            return self.authenticate_credentials(request.query_params.get(AUTH_API_KEY_PARAM))
        else:
            return super(TokenAuthSupportQueryString, self).authenticate(request)
