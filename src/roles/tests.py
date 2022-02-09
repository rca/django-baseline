from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from roles.models import Role


def test_role_create(db):
    role = Role.objects.create(name="test")

    assert "Role - test" == role.name


def test_role_gets_all_perms(db):
    content_type = ContentType.objects.get_for_model(Permission)
    permission = Permission.objects.create(name="can-buy", content_type=content_type)

    group, _ = Group.objects.get_or_create(name="buyer")
    group.permissions.add(permission)

    role = Role.objects.create(name="test", groups=[group])

    assert 1 == role.groups.count()

    # check to see that all the permissions from the groups associated to the role are in the role itself
    assert 1 == role.permissions.count()

    assert permission == role.permissions.get()

    # ensure that removing the permission syncs properly
    group.permissions.remove(permission)

    assert 0 == role.permissions.count()
