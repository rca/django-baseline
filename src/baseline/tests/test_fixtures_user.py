from unittest import mock

from django.contrib.auth.models import Group


def test_get_user(get_user):
    """
    Ensures a user is returned without being saved to the database
    """
    user = get_user(username="test_user", _save=False)

    assert user.pk is None


def test_get_user_with_dynamic_username(db, get_user):
    """
    Ensures a user is returned without being saved to the database
    """
    user = get_user(_save=False)

    assert user.pk is None
    assert user.username == "test_user"

    # once a user is in the database, usernames must be unique
    user.save()

    user2 = get_user()

    assert user2.username == "test_user2"


def test_get_user_with_group(db, get_user):
    """
    Ensures a user is returned without being saved to the database
    """
    group = Group.objects.create(name="test_group")

    user = get_user(groups=[group])

    assert user.pk is not None
    assert user.username == "test_user"

    assert user.groups.count() == 1


def test_get_username(get_username, monkeypatch):
    """
    ensure the given prefix is used when there are no users in the database with that prefix
    """
    user_mock = mock.Mock()

    monkeypatch.setattr("conftest.User", user_mock)

    # when there are 0 users in the database with the prefix, the prefix itself is returned
    user_mock.objects.filter.return_value.count.return_value = 0

    username = get_username()

    assert username == "test_user"


def test_get_username_custom_prefix(get_username, monkeypatch):
    """
    ensure the given prefix is used when there are no users in the database with that prefix
    """
    user_mock = mock.Mock()

    monkeypatch.setattr("conftest.User", user_mock)

    # when there are 0 users in the database with the prefix, the prefix itself is returned
    user_mock.objects.filter.return_value.count.return_value = 0

    username = get_username(prefix="foo")

    assert username == "foo"


def test_get_username_with_count(get_username, monkeypatch):
    """
    ensure the given prefix is used when there are no users in the database with that prefix
    """
    user_mock = mock.Mock()

    monkeypatch.setattr("conftest.User", user_mock)

    # when there are 0 users in the database with the prefix, the prefix itself is returned
    user_mock.objects.filter.return_value.count.return_value = 1

    username = get_username()

    assert username == "test_user2"
