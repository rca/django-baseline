import os
import typing

from dataclasses import dataclass

from . import tests

Any = typing.Any
Callable = typing.Callable

# this dictionary holds all the environment variables requested
catalog = {}


def get_catalog():
    """
    Returns a dictionary of all the environment settings requested
    """
    return catalog


def get_setting(setting_cls, name: str, *args, **kwargs) -> Any:
    """
    Returns a setting using the given settings class

    This adds the setting to the catalog and if the setting is already
    in the catalog the existing value will be used.
    """
    catalog_setting = catalog.get(name)
    if not catalog_setting:
        setting = setting_cls(name, *args, **kwargs)
        value = setting.get()

        catalog_setting = CatalogSetting(name, setting, value)
        catalog[name] = catalog_setting

    value = catalog_setting.value

    return value


class EnvironmentSetting:
    """
    A environment variable lazy loader
    """

    def __init__(
        self,
        name: str,
        *args,
        default: Any = None,
        required: bool = True,
        **kwargs,
    ):
        self.default = default
        self.name = name
        self.required = required

    @property
    def attributes(self) -> dict:
        """
        Returns the default values for this setting

        Note, this is a list of defaults because subclasses may have different
        defaults based on different situations
        """
        return {"default": self.default, "required": self.required}

    def get(self):
        value = self.default
        try:
            value = os.environ[self.name]
        except KeyError:
            if self.required and value is None:
                raise

        return value


class MaintenanceEnvironmentSetting(EnvironmentSetting):
    """
    Abstraction for getting settings from the environment with an extra check for maintenance commands

    When certain commands are being run, such as running tests, or creating migrations, all of the settings
    do not need to have real values.  In fact, some of them should not have real values as they may have
    adverse effects, such as making upstream calls or using real, valid secrets.  In the case of running
    tests, most settings are stubbed out or explicitly set to test a particular thing.

    Once a project grows large, it is sometimes difficult to come up with a set of environment variables
    needed to get the project up and running.  Gathering settings with this class makes it easier, as it's
    possible to get a catalog of settings that use this object (see the `show_environment_settings` management
    command).
    """

    default_value = "MAINTENANCE_SETTING"

    def __init__(
        self,
        name: str,
        *args,
        default: Any = None,
        maintenance_default: Any = None,
        required: bool = True,
        **kwargs,
    ):
        self.maintenance_default = maintenance_default

        super().__init__(
            name,
            *args,
            default=default,
            required=required,
            **kwargs,
        )

    @property
    def attributes(self) -> dict:
        """
        Returns the setting attributes
        """
        attributes = super().attributes
        attributes.update({"maintenance_default": self.maintenance_default})

        return attributes

    def get(self):
        if self.is_test and self.default is None:
            self.default = self.maintenance_default or self.default_value

        return super().get()

    @property
    def is_test(self):
        """
        Returns whether the current process is a test run
        """
        import sys

        is_test = False
        if sys.argv[0].endswith("manage.py") and (
            len(sys.argv) == 1
            or (
                len(sys.argv) > 1
                and sys.argv[1]
                in (
                    "collectstatic",
                    "makemigrations",
                    "migrate",
                    "show_environment_settings",
                )
            )
        ):
            is_test = True
        elif tests.IS_PYTEST_RUNNING:
            is_test = True

        return is_test


@dataclass
class CatalogSetting:
    """
    A setting that has been requested and is in the catalog
    """

    name: str
    setting: EnvironmentSetting
    value: str

    def __str__(self):
        return str(self.value)
