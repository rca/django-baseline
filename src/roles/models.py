from django.contrib.auth.models import Group
from django.db import models

ROLE_NAME_PREFIX = "Role - "


class RoleQuerySet(models.QuerySet):
    def create(self, **kwargs):
        """
        Handles groups argument and properly sets the m2m relation
        """
        groups = kwargs.pop("groups", None)

        role = super().create(**kwargs)

        if groups:
            role.groups.set(groups)

        return role


class RoleManager(models.Manager.from_queryset(RoleQuerySet)):
    """
    A custom manager that can be used in migrations

    https://docs.djangoproject.com/en/4.0/topics/migrations/#model-managers
    """

    use_in_migrations = True


class Role(Group):
    """
    A role, which comprises zero or more Django groups
    """

    groups = models.ManyToManyField(Group, related_name="role_groups")

    objects = RoleManager()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Setup conventions for the role itself
        """
        if not self.name.startswith(ROLE_NAME_PREFIX):
            self.name = f"{ROLE_NAME_PREFIX}{self.name}"

        super().save(force_insert, force_update, using, update_fields)

    def sync_permissions(self):
        """
        Get all the permissions from the associated groups and sync them into the role
        """
        new_permissions = []
        for group in self.groups.all():
            new_permissions.extend(group.permissions.all())

        self.permissions.set(new_permissions)
