import os
import typing

from . import tests

Any = typing.Any
Callable = typing.Callable


def get_setting(setting_cls, *args, **kwargs) -> Any:
    """
    Returns a setting using the given settings class
    """
    setting = setting_cls(*args, **kwargs)
    return setting.get()


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

    def get(self):
        value = self.default
        try:
            value = os.environ[self.name]
        except KeyError:
            if self.required and value is None:
                raise

        return value


class MaintenanceEnvironmentSetting(EnvironmentSetting):
    default_value = "MAINTENANCE_SETTING"

    def __init__(
        self,
        name: str,
        *args,
        default: Any = None,
        test_default: Any = None,
        required: bool = True,
        **kwargs,
    ):
        self.test_default = test_default

        super().__init__(
            name,
            *args,
            default=default,
            required=required,
            **kwargs,
        )

    def get(self):
        if self.is_test and self.default is None:
            self.default = self.test_default or self.default_value

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
                )
            )
        ):
            is_test = True
        elif tests.IS_PYTEST_RUNNING:
            is_test = True

        return is_test
