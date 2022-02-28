import pytest

from .models import Widget


@pytest.fixture()
def get_widget():
    def fixture(name: str = "Thing", quantity=1):
        return Widget.objects.create(name=name, quantity=quantity)

    return fixture
