from django.apps.registry import apps as global_apps
from django.contrib.auth.management import create_permissions
from django.contrib.contenttypes.management import create_contenttypes


def create_content_types_and_permissions(app_name: str, apps, schema_editor):
    """
    Creates content types and permissions for all of the models in the given application name

    This can be useful when migrations require the content types and permissions to be available
    In order to run data migrations that use the automatically-created django model permissions

    Args:
        app_name: the name of the application that you need permissions from
        apps: apps object provided by the migrations run
        schema_editor: the schema_editor object provided by the migrations run
    """
    app_config = global_apps.get_app_config(app_name)
    create_contenttypes(app_config)

    # in addition to creating the content types, the permissions have to be force-fed as well
    # https://medium.com/@gauravtoshniwal/how-to-create-content-types-and-permissions-for-already-created-tables-89a3647ff720
    create_permissions(app_config)


def remove_content_types(app_name: str, apps, schema_editor):
    """
    Stub for removing content types; this is currently a no-op
    """
    pass
