import pytest

from baseline.environment import MaintenanceEnvironmentSetting


TEST_ENVIRONMENT_VARIABLE_NAME = "TEST_ENV_ONE_TWO_THREE"


@pytest.fixture()
def disable_maintenance(monkeypatch):
    monkeypatch.setattr("baseline.environment.is_maintenance", lambda: False)


def test_default_in_normal_mode(disable_maintenance):
    """
    Ensure getting the value blows up when not in test mode
    """
    setting = MaintenanceEnvironmentSetting(
        TEST_ENVIRONMENT_VARIABLE_NAME, default=None
    )

    value = setting.get()

    assert value is None


def test_test_default_in_normal_mode(disable_maintenance):
    """
    Ensure getting the value blows up when not in test mode
    """
    setting = MaintenanceEnvironmentSetting(TEST_ENVIRONMENT_VARIABLE_NAME)

    with pytest.raises(KeyError):
        setting.get()


def test_test_default_in_normal_mode_with_test_override(disable_maintenance):
    """
    Ensure the test value is returned in test mode
    """
    barfoo = "BARFOO"

    setting = MaintenanceEnvironmentSetting(
        TEST_ENVIRONMENT_VARIABLE_NAME, maintenance_default=barfoo
    )

    with pytest.raises(KeyError):
        setting.get()


def test_test_default_in_normal_mode_with_test_override_and_default(
    disable_maintenance,
):
    """
    Ensure the test value is returned in test mode
    """
    barfoo = "BARFOO"

    setting = MaintenanceEnvironmentSetting(
        TEST_ENVIRONMENT_VARIABLE_NAME, default=barfoo, maintenance_default=barfoo * 2
    )

    assert barfoo == setting.get()


def test_test_default_in_test_mode():
    """
    Ensure the test value is returned in test mode
    """
    setting = MaintenanceEnvironmentSetting(TEST_ENVIRONMENT_VARIABLE_NAME)

    assert setting.get() == MaintenanceEnvironmentSetting.default_value


def test_test_default_in_test_mode_with_test_override():
    """
    Ensure the test value is returned in test mode
    """
    barfoo = "BARFOO"
    setting = MaintenanceEnvironmentSetting(
        TEST_ENVIRONMENT_VARIABLE_NAME, maintenance_default=barfoo
    )

    assert setting.get() == barfoo


def test_test_default_in_test_mode_with_None_override():
    """
    Ensure None is returned in test mode
    """
    setting = MaintenanceEnvironmentSetting(
        TEST_ENVIRONMENT_VARIABLE_NAME, maintenance_default=None
    )

    assert setting.get() is None


def test_environment_setting_catalog():
    """
    Ensure settings that come from the environment are cataloged in a single call
    """
    from baseline.environment import get_catalog

    settings = get_catalog()

    assert isinstance(settings, dict)

    assert len(settings) > 0


def test_unset_setting_not_required():
    """
    Ensure setting not required returns None
    """
    setting = MaintenanceEnvironmentSetting(
        TEST_ENVIRONMENT_VARIABLE_NAME, required=False
    )

    assert setting.get() is None


def test_unset_setting_not_required_with_maintenance_default():
    """
    Ensure setting not required returns None
    """
    value = "i should get this"
    setting = MaintenanceEnvironmentSetting(
        TEST_ENVIRONMENT_VARIABLE_NAME, required=False, maintenance_default=value
    )

    assert setting.get() is value
