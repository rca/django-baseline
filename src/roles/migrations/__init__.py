import typing

import functools
from django.db import migrations

from roles.models import Role

List = typing.List


def get_role_and_group(
    role_codename: str, group_name: str, apps, schema_editor
) -> ["Role", "Group"]:
    """
    Returns role and group objects for the specified args

    Args:
        role_codename: the role's codename
        group_name: the groups name
        apps: apps object provided by the migrations run
        schema_editor: the schema_editor object provided by the migrations run

    Returns:
        role and group objects
    """
    db_alias = schema_editor.connection.alias

    # create a group for firebase functions that permissions can be added to
    MigrationGroup = apps.get_model("auth", "Group")
    MigrationRole = apps.get_model("roles", "Role")

    print(f"getting role_codename={role_codename}, group_name={group_name}...", end="")

    role = MigrationRole.objects.using(db_alias).get(codename=role_codename)
    group = MigrationGroup.objects.using(db_alias).get(name=group_name)

    return role, group


def migrate_group_in_role(role_name: str, group_name: str) -> List["Operation"]:
    """
    Returns a list of operations for setting up a group within a role

    Args:
        group_name: the name of the group to migrate into the role
        role_name: the name of the role to migrate the group into

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
    ]

    return operations


def role_add_group(role_codename: str, group_name: str, apps, schema_editor) -> None:
    """
    Adds the group to the role

    Args:
        role_codename: the name of the role
        group_name: the name of the group
        apps: apps object provided by the migrations run
        schema_editor: the schema_editor object provided by the migrations run
    """
    role, group = get_role_and_group(role_codename, group_name, apps, schema_editor)

    role.groups.add(group)

    Role.sync_permissions(role)


def role_remove_group(role_codename: str, group_name: str, apps, schema_editor) -> None:
    """
    Removes the group from the role

    Args:
        role_codename: the name of the role
        group_name: the name of the group
        apps: apps object provided by the migrations run
        schema_editor: the schema_editor object provided by the migrations run
    """
    role, group = get_role_and_group(role_codename, group_name, apps, schema_editor)

    role.groups.remove(group)

    Role.sync_permissions(role)
