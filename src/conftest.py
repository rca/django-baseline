import typing

import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from baseline import tests
from baseline.types import ModelType

if typing.TYPE_CHECKING:
    from django.contrib.auth.models import Group
    from django.db.models import Model

Callable = typing.Callable
Iterable = typing.Iterable
User = get_user_model()


class ModelError(Exception):
    """
    Raised below
    """


def pytest_configure(config):
    tests.IS_PYTEST_RUNNING = True


@pytest.fixture()
def get_api_client(get_user) -> "Callable":
    """
    Returns a test API client instance

    Args:
        get_user: fixture to create a user

    Returns:
        Callable
    """

    def fixture(user: "User" = None, create_user: bool = False) -> "APIClient":
        """
        Returns a rest framework API client instance

        Args:
            user: optional user to login to the client
            create_user: whether to create a new user

        Returns:
            an API client instance
        """
        if create_user:
            if user:
                raise ValueError("Cannot set create_user and provide a user instance")

            user = get_user(username="test_user")

        client = APIClient()

        # when there is a user instance, authenticate the client
        if user:
            client.force_authenticate(user)

        return client

    return fixture


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


@pytest.fixture()
def get_user(db, get_username) -> "Callable":
    """
    Fixture to return a user instance
    """

    def fixture(
        *args, groups: Iterable["Group"] = None, _save: bool = True, **kwargs
    ) -> "User":
        """

        Args:
            *args: Passed to User constructor
            groups: a list of groups to be added to the user
            _save: whether to save the user object
            **kwargs: Passed to User constructor

        If groups are passed in or a username not specified, the user must be saved to the database, in which case the test
        using this fixture must include the db fixture.

        Returns:
            a User instance
        """
        defaults = dict(
            username=get_username,
        )
        for k, v_callable in defaults.items():
            if k not in kwargs:
                kwargs[k] = v_callable()

        user = User(*args, **kwargs)

        # save the user object if needed
        if groups or _save:
            user.save()

        if groups:
            user.groups.set(groups)

        return user

    return fixture


@pytest.fixture()
def get_username() -> "Callable":
    def fixture(prefix: str = "test_user") -> str:
        """
        Returns a unique username

        Args:
            prefix: the username prefix

        Returns:
            a username
        """
        user_count = User.objects.filter(username__startswith=prefix).count()
        if user_count:
            counter = user_count + 1
            return f"{prefix}{counter}"

        return prefix

    return fixture


# any custom configuration below
