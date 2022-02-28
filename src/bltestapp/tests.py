from rest_framework import status
from rest_framework.reverse import reverse

from bltestapp.fixtures import *


def test_widget_filtering(get_api_client, get_widget):
    """
    Ensure filtering configuration works
    """
    for i in range(3):
        get_widget(name=f"thing {i}")

    client = get_api_client()

    url = reverse("widgets-list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]

    assert len(results) == 3

    # filter by a full name
    filter_name = "thing 1"
    response = client.get(url, data=dict(name=filter_name))

    results = response.data["results"]

    assert len(results) == 1

    assert results[0]["name"] == filter_name

    # filter by a partial name
    filter_name = " 2"
    response = client.get(url, data=dict(name=filter_name))

    results = response.data["results"]

    assert len(results) == 1

    assert results[0]["name"] == "thing 2"


def test_widget_search(get_api_client, get_widget):
    """
    Ensure search works
    """
    for i in range(3):
        get_widget(name=f"thing {i}")

    client = get_api_client()

    url = reverse("widgets-list")

    filter_name = " 2"
    response = client.get(url, data=dict(search=filter_name))

    results = response.data["results"]

    assert len(results) == 1, results
