from rest_framework.reverse import reverse
from rest_framework import status


def test_login(get_api_client, get_user):
    email = "test@test.com"
    password = "test123"

    user = get_user(username=email, password=password)

    client = get_api_client()

    url = reverse("authrrr-list")

    data = {
        "username": email,
        "password": password,
    }

    response = client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK, response.content

    assert response.cookies["auth"].value == user.auth_token.key
