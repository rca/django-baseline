import os
import typing

from dataclasses import dataclass

from .settings.utils import is_maintenance

Any = typing.Any
Callable = typing.Callable

# this dictionary holds all the environment variables requested
catalog = {}


def get_catalog():
    """
    Returns a dictionary of all the environment settings requested
    """
    return catalog


def get_setting(setting_cls, name: str, *args, **kwargs) -> str:
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
        default: Any = None,
        required: bool = True,
    ):
        self.default = default
        self.name = name
        self.required = required

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

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
        default: Any = None,
        maintenance_default: Any = None,
        required: bool = True,
    ):
        self.maintenance_default = maintenance_default or self.default_value

        super().__init__(
            name,
            default=default,
            required=required,
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
        try:
            value = super().get()
        except KeyError:
            if is_maintenance():
                value = self.maintenance_default
            else:
                raise

        return value


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
