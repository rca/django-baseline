import functools

from ..environment import MaintenanceEnvironmentSetting, get_setting as base_get_setting

get_setting = functools.partial(base_get_setting, MaintenanceEnvironmentSetting)


def is_maintenance() -> bool:
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
                "startapp",
            )
        )
    ):
        is_test = True
    elif "pytest" in sys.argv[0]:
        is_test = True

    return is_test
