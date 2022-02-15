import functools

from ..environment import MaintenanceEnvironmentSetting, get_setting as base_get_setting

get_setting = functools.partial(base_get_setting, MaintenanceEnvironmentSetting)
