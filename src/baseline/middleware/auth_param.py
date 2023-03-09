"""
Middleware to authenticate with a GET parameter
"""
import json

AUTHORIZATION_HEADER = "HTTP_AUTHORIZATION"


class AuthParamMiddleware:
    """
    Middleware to check for auth param
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        auth_token = request.GET.get("auth_token")
        if (
            request.content_type == "application/json"
            and request.method.upper() == "POST"
            and request.body
        ):
            data = json.loads(request.body)
            auth_token = data.get("auth_token")

        if not auth_token:  # check cookie
            auth_token = request.COOKIES.get("auth_token")

        if auth_token:
            request.META[AUTHORIZATION_HEADER] = f"Token {auth_token}"

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
