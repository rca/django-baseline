def get_setting(*args, **kwargs) -> str:
    """
    Returns the value for the given setting

    Args:
        *args: args to be passed to the setting class
        **kwargs: kwargs to be passed to the setting class

    Returns:
        str: the setting's value
    """
    from ..environment import (
        MaintenanceEnvironmentSetting,
        get_setting as base_get_setting,
    )

    return base_get_setting(MaintenanceEnvironmentSetting, *args, **kwargs)


def is_maintenance() -> bool:
    """
    Returns whether the current process is a test run
    """
    import sys

    maintenance = False
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
        maintenance = True
    elif is_test():
        maintenance = True

    return maintenance


def is_test() -> bool:
    """
    Returns whether tests are being run
    """
    import sys

    return "pytest" in sys.argv[0]
