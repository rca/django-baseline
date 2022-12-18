import functools
import typing

from django.apps.registry import apps as global_apps
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations

from baseline.utils import get_permissions, change_group_permissions
from roles.models import Role

if typing.TYPE_CHECKING:
    from django.db.migrations.operations.base import Operation


Iterable = typing.Iterable
List = typing.List


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

    # get the permissions
    ContentType = get_schema_model("contenttypes", "ContentType", apps, schema_editor)
    permissions = get_permissions(
        app_name,
        model_name,
        permissions_verbs,
        content_type_cls=ContentType,
        db_alias=db_alias,
    )

    Group = get_schema_model("auth", "Group", apps, schema_editor)
    change_group_permissions(
        group_name, operation, permissions, group_cls=Group, db_alias=db_alias
    )

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


def get_group(group_name: str, apps, schema_editor):
    """
    Returns the requested group
    """
    return get_schema_model_instance(
        "auth", "Group", apps, schema_editor, name=group_name
    )


def get_role(role_name: str, apps, schema_editor) -> "Role":
    """
    Returns the requested role
    """
    return get_schema_model_instance(
        "roles", "Role", apps, schema_editor, codename=role_name
    )


def get_schema_model(app_name: str, model_name: str, apps, schema_editor):
    """
    Returns the schema model instance

    Args:
        app_name: the name of the app
        model_name: the name of the models
        apps: the apps instance passed into migrations functions
        schema_editor: the schema editor instance passed into migrations functions

    Returns:
        the schema model instance
    """
    return apps.get_model(app_name, model_name)


def get_schema_model_instance(app_name, model_name, apps, schema_editor, **kwargs):
    """
    Returns a record for the given model instance

    Args:
        app_name: the name of the app
        model_name: the name of the models
        apps: the apps instance passed into migrations functions
        schema_editor: the schema editor instance passed into migrations functions
        **kwargs: passed directly into .get()

    Returns:
        the schema model instance
    """
    db_alias = schema_editor.connection.alias

    # create a group for firebase functions that permissions can be added to
    SchemaModel = get_schema_model(app_name, model_name, apps, schema_editor)

    return SchemaModel.objects.using(db_alias).get(**kwargs)


def group_add(group_name: str, apps, schema_editor) -> "Group":
    """
    Adds a group

    Args:
        group_name: the name of the group
        apps: apps object provided by the migrations run
        schema_editor: the schema_editor object provided by the migrations run
    """
    db_alias = schema_editor.connection.alias

    # create a group for firebase functions that permissions can be added to
    Group = get_schema_model("auth", "Group", apps, schema_editor)

    return Group.objects.using(db_alias).create(name=group_name)


def group_remove(group_name: str, apps, schema_editor):
    """
    Removes a group

    Args:
        group_name: the name of the group
        apps: apps object provided by the migrations run
        schema_editor: the schema_editor object provided by the migrations run
    """
    return get_group(group_name, apps, schema_editor).delete()


def migrate_group(group_name: str) -> List["Operation"]:
    """
    Returns a list of operations for setting up a new group

    Args:
        group_name: the name of the group to operate on

    Returns:
        a list of operations that can be added to a Migration class's `operations` list
    """
    operations = [
        migrations.RunPython(
            functools.partial(
                group_add,
                group_name,
            ),
            functools.partial(
                group_remove,
                group_name,
            ),
        ),
    ]

    return operations


def migrate_permissions_in_group(
    group_name: str,
    app_name: str,
    model_name: str,
    permissions_verbs: Iterable[str],
) -> "List[Operation]":
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
        List[Operation]:
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
        migrations.RunPython(
            functools.partial(
                sync_group_roles,
                group_name,
            ),
            lambda *args, **kwargs: None,
        ),
    ]

    return operations


def migrate_role(role_name: str) -> List["Operation"]:
    """
    Returns a list of operations for setting up a new role

    Args:
        role_name: the name of the role to operate on

    Returns:
        a list of operations that can be added to a Migration class's `operations` list
    """
    operations = [
        migrations.RunPython(
            functools.partial(
                role_create,
                role_name,
            ),
            functools.partial(
                role_delete,
                role_name,
            ),
        ),
    ]

    return operations


def migrate_role_group(role_name: str, group_name: str) -> List["Operation"]:
    """
    Returns a list of operations for managing a group within a role

    Args:
        role_name: the name of the role to operate on; it must already exist
        group_name: the name of the group to operate on within the role

    Returns:
        a list of operations that can be added to a Migration class's `operations` list
    """
    operations = [
        migrations.RunPython(
            functools.partial(
                role_add_group,
                role_name,
                group_name,
            ),
            functools.partial(
                role_remove_group,
                role_name,
                group_name,
            ),
        ),
        migrations.RunPython(
            functools.partial(
                sync_role,
                role_name,
            ),
            functools.partial(
                sync_role,
                role_name,
            ),
        ),
    ]

    return operations


def remove_content_types(app_name: str, apps, schema_editor):
    """
    Stub for removing content types; this is currently a no-op
    """
    pass


def role_create(role_name: str, apps, schema_editor):
    """
    Creates a role
    """
    db_alias = schema_editor.connection.alias

    # create a group for firebase functions that permissions can be added to
    SchemaRole = get_schema_model("roles", "Role", apps, schema_editor)

    return SchemaRole.objects.using(db_alias).create(codename=role_name)


def role_delete(role_name: str, apps, schema_editor):
    """
    Removes a role
    """
    return get_role(role_name, apps, schema_editor).delete()


def role_add_group(role_name: str, group_name: str, apps, schema_editor):
    """
    Adds a group to a role
    """
    role = get_role(role_name, apps, schema_editor)
    group = get_group(group_name, apps, schema_editor)

    role.groups.add(group)


def role_remove_group(role_name: str, group_name: str, apps, schema_editor):
    """
    Removes a group from a role
    """
    role = get_role(role_name, apps, schema_editor)
    group = get_group(group_name, apps, schema_editor)

    role.groups.remove(group)


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


def sync_group_roles(group_name: str, apps, schema_editor):
    """
    Explicitly sync roles the given group is associated with

    Because signals are not called automatically by migrations

    Args:
        group_name: the name of the group
    """
    group = Group.objects.get(name=group_name)
    roles = Role.objects.filter(groups__in=[group])

    for role in roles:
        role.sync_permissions()


def sync_role(role_name: str, apps, schema_editor):
    """
    Syncs the permissions in the given role

    Args:
        role_name: the name of the role
    """
    role = Role.objects.get(name=role_name)
    role.sync_permissions()
