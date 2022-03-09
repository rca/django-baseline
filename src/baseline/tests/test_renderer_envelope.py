from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from bltestapp.models import Widget


def test_detail_envelope(db):
    """
    ensure the response ends up in a `result` key
    """
    client = APIClient()

    widget = Widget.objects.create(name="test widget", quantity=1)

    url = reverse("widgets-detail", kwargs=dict(pk=widget.pk))
    response = client.get(url)

    assert "result" in response.data.keys()


def test_list_envelope(db):
    """
    ensure a list request does not re-wrap the `results` key
    """
    client = APIClient()

    widget = Widget.objects.create(name="test widget", quantity=1)

    url = reverse("widgets-list")
    response = client.get(url)

    assert "result" not in response.data.keys()
    assert "results" in response.data.keys()


def test_handle_empty_response(db):
    """
    ensure that a request without a response body succeeds
    """
    client = APIClient()

    widget = Widget.objects.create(name="test widget", quantity=1)

    url = reverse("widgets-detail", kwargs=dict(pk=widget.pk))
    response = client.delete(url)
