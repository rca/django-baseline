import pytest

from baseline.environment import MaintenanceEnvironmentSetting


TEST_ENVIRONMENT_VARIABLE_NAME = "TEST_ENV_ONE_TWO_THREE"


def test_test_default_in_normal_mode(monkeypatch):
    """
    Ensure getting the value blows up when not in test mode
    """
    monkeypatch.setattr(
        MaintenanceEnvironmentSetting, "is_test", property(lambda self: False)
    )
    setting = MaintenanceEnvironmentSetting(TEST_ENVIRONMENT_VARIABLE_NAME)

    with pytest.raises(KeyError):
        setting.get()


def test_test_default_in_normal_mode_with_test_override(monkeypatch):
    """
    Ensure the test value is returned in test mode
    """
    barfoo = "BARFOO"

    monkeypatch.setattr(
        MaintenanceEnvironmentSetting, "is_test", property(lambda self: False)
    )

    setting = MaintenanceEnvironmentSetting(
        TEST_ENVIRONMENT_VARIABLE_NAME, maintenance_default=barfoo
    )

    with pytest.raises(KeyError):
        setting.get()


def test_test_default_in_normal_mode_with_test_override_and_default(monkeypatch):
    """
    Ensure the test value is returned in test mode
    """
    barfoo = "BARFOO"

    monkeypatch.setattr(
        MaintenanceEnvironmentSetting, "is_test", property(lambda self: False)
    )

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


def test_environment_setting_catalog():
    """
    Ensure settings that come from the environment are cataloged in a single call
    """
    from baseline.environment import get_catalog

    settings = get_catalog()

    assert isinstance(settings, dict)

    assert len(settings) > 0
