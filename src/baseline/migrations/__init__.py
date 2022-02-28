import functools
import typing

from django.apps.registry import apps as global_apps
from django.contrib.auth.management import create_permissions
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations

if typing.TYPE_CHECKING:
    from django.db.migrations.operations.base import Operation
    from django.contrib.auth.models import Permission

Iterable = typing.Iterable


def change_permissions_in_group(
    operation: str,
    group_name: str,
    app_name: str,
    model_name: str,
    permissions_verbs: Iterable[str],
    apps,
    schema_editor,
) -> Iterable["Permission"]:
    """
    Changes the listed permissions to a group

    Using the ContentTypes framework get the permissions for the app and model name args, then
    iterate through that model's permissions and change any that match the verbs given, where the
    default verbs given to a model are: add, change, delete, view.

    They are added or removed per the `operation` arg, which can be: add, remove

    Args:
        operation: add or remove
        group_name:
        app_name:
        model_name:
        permissions_verbs:
        apps:
        schema_editor:

    Returns:
        the list of permissions added
    """
    db_alias = schema_editor.connection.alias

    if operation not in ("add", "remove"):
        raise ValueError("operation must be 'add' or 'remove'")

    Group = apps.get_model("auth", "Group")
    group = Group.objects.using(db_alias).get(name=group_name)

    ContentType = apps.get_model("contenttypes", "ContentType")
    content_type = ContentType.objects.using(db_alias).get(
        app_label=app_name, model=model_name
    )

    permissions = []
    for verb in permissions_verbs:
        prefix = f"{verb}_"
        permissions.append(
            # get each permission in order to catch if one of the given verbs is
            # not in the db
            content_type.permission_set.using(db_alias).get(codename__startswith=prefix)
        )

    operation_fn = getattr(group.permissions, operation)
    operation_fn(*permissions)

    return permissions


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


def migrate_permissions_in_group(
    group_name: str,
    app_name: str,
    model_name: str,
    permissions_verbs: Iterable[str],
) -> Iterable["Operation"]:
    """
    Returns a list of operations for setting group permissions

    The operations returned make sure that the content types and permissions have first been set
    in the database for the model these permissions correspond to, as well as the operation for
    setting the permissions in the group.

    Args:
        group_name: the name of the group to operate on; it must already exist
        app_name: the name of the app the model belongs to
        model_name: the name of the model the permissions belong to
        permissions_verbs: the permissions to set in the group, i.e. add, change, delete, view

    Returns:
        a list of operations that can be added to a Migration class's `operations` list
    """
    operations = [
        setup_content_types(app_name),
        migrations.RunPython(
            functools.partial(
                change_permissions_in_group,
                "add",
                group_name,
                app_name,
                model_name,
                permissions_verbs,
            ),
            functools.partial(
                change_permissions_in_group,
                "remove",
                group_name,
                app_name,
                model_name,
                permissions_verbs,
            ),
        ),
    ]

    return operations


def remove_content_types(app_name: str, apps, schema_editor):
    """
    Stub for removing content types; this is currently a no-op
    """
    pass


def setup_content_types(app_name: str) -> "Operation":
    """
    Sets content types and permissions in the database

    Before running any migration operation that relies on permissions being
    in the database, make sure all the app content types and permissions
    are created.

    Args:
        app_name: the name of the django app to create permissions for
    """
    return migrations.RunPython(
        functools.partial(create_content_types_and_permissions, app_name),
        functools.partial(remove_content_types, app_name),
    )
