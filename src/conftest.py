import typing

import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import connections
from rest_framework.test import APIClient

from baseline import tests
from baseline.types import ModelType

if typing.TYPE_CHECKING:
    from django.contrib.auth.models import Permission
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
def closed_test_transaction(db):
    """
    rolls back the outer test transaction and starts a fresh transaction
    """
    connection_name = "default"

    # manually reset the connection that the django TestCase creates in order to
    # create some objects that are available in a thread
    connection = connections[connection_name]
    connection.in_atomic_block = False
    connection.rollback()

    yield

    # in order to let the upstream teardown work properly, make the connection
    # appear as if it's in an atomic block
    connection = connections[connection_name]
    connection.in_atomic_block = True


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
def get_group(db, get_group_name):
    """
    Returns a function to get / create a group
    """

    def fixture(
        *args,
        _permissions: Iterable["Permission"] = None,
        _save: bool = True,
        **kwargs,
    ) -> "User":
        """

        Args:
            *args: Passed to User constructor
            _permissions: a list of permissions to add to the instance
            _save: whether to save the instance
            **kwargs: Passed to User constructor

        Returns:
            a Group instance
        """
        defaults = dict(
            name=get_group_name,
        )
        for k, v_callable in defaults.items():
            if k not in kwargs or kwargs[k] is None:
                kwargs[k] = v_callable()

        instance = Group(*args, **kwargs)

        # save the user object if needed
        if _save:
            instance.save()

        if _permissions:
            for permission in _permissions:
                instance.permissions.add(permission)

        return instance

    return fixture


@pytest.fixture()
def get_group_name(db) -> "Callable":
    """
    Returns a function to get a unique group name
    """

    def fixture(prefix: str = "test_group") -> str:
        """
        Returns a unique group name

        Args:
            prefix: the group name prefix

        Returns:
            a group name
        """
        count = Group.objects.filter(name__startswith=prefix).count()
        if count:
            counter = count + 1
            return f"{prefix}{counter}"

        return prefix

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
        *args,
        groups: Iterable["Group"] = None,
        _permissions: Iterable["Permission"] = None,
        _save: bool = True,
        **kwargs,
    ) -> "User":
        """

        Args:
            *args: Passed to User constructor
            groups: a list of groups to be added to the user
            _permissions: a list of permissions to add to the user
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
            if k not in kwargs or kwargs[k] is None:
                kwargs[k] = v_callable()

        user = User(*args, **kwargs)

        # save the user object if needed
        if groups or _save:
            user.save()

        if groups:
            user.groups.set(groups)

        if _permissions:
            for permission in _permissions:
                user.user_permissions.add(permission)

        return user

    return fixture


@pytest.fixture()
def get_username(db) -> "Callable":
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


@pytest.fixture(autouse=True)
def reset_cache():
    yield

    cache.clear()


@pytest.fixture(scope="function", autouse=True)
def request_mock():
    """
    mock out the request() function, which is the call that all HTTP methods make
    """
    with mock.patch("requests.api.request") as request_mock:
        yield request_mock


@pytest.fixture(scope="session", autouse=True)
def requests_get_adapter():
    web_patcher = mock.patch("requests.sessions.Session.get_adapter", spec=True)
    _mock = web_patcher.start()

    try:
        yield _mock
    finally:
        web_patcher.stop()


@pytest.fixture(scope="session", autouse=True)
def sleep_mock():
    """
    mock out the request() function, which is the call that all HTTP methods make
    """
    with mock.patch("time.sleep") as mocked:
        yield mocked


# any custom configuration below
