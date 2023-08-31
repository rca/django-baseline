"""
Module for API request helpers
"""
import requests

from baseline.types import JSON


class APIClient:
    """
    Wrapper around requests to handle API calls
    """

    def __init__(self, *args, headers: dict = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = requests.session()

        if headers:
            self.session.headers.update(headers)

    def get_response(
        self, method: str, url: str, json: dict = None, params: dict = None
    ) -> "requests.Response":
        """
        Returns the response JSON

        Args:
            method: the HTTP method to call
            url: the URL to request
            json: the data being past into the post body
            params: query params in the URL
        """
        method_fn = getattr(self.session, method)
        response = method_fn(url, json=json, params=params)

        try:
            response.raise_for_status()
        except:
            print(response.content)

            raise

        return response

    def get_response_json(self, *args, **kwargs) -> JSON:
        """
        Returns the JSON blob for this request's response

        Args:
            *args: passed into get_response()
            **kwargs: passed into get_response

        Returns:
            JSON response
        """
        response = self.get_response(*args, **kwargs)

        return response.json()
