import typing

import pytest

from django.contrib.auth import get_user_model

from baseline import tests
from baseline.types import ModelType

if typing.TYPE_CHECKING:
    from django.db.models import Model

User = get_user_model()


class ModelError(Exception):
    """
    Raised below
    """


def pytest_configure(config):
    tests.IS_PYTEST_RUNNING = True


@pytest.fixture()
def get_model(db):
    """
    Returns a function to get / create a instance
    """

    def wrapper(
        model_cls: "ModelType", *args, create: bool = True, **kwargs
    ) -> "Model":
        """
        Gets / Creates a Django model instance

        Args:
            model_cls: The type of object to retrieve
            *args: any additional arguments to pass along to instance creation
            create: when False a newly created instance will raise an exception.
            **kwargs: any additional arguments to pass along to instance creation

        Returns:

        """
        instance, created = model_cls.objects.get_or_create(*args, **kwargs)
        if not create and created:
            raise ModelError(
                f"model_cls={model_cls}, args={args}, kwargs={kwargs} does not already exists"
            )

        return instance

    return wrapper
