from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from roles.models import Role


@receiver(m2m_changed, sender=Role.groups.through)
def sync_permissions_when_groups_change(
    sender, instance: "Role", action, reverse, **kwargs
):
    """
    When the groups in a role change, update the permissions in the role itself
    """
    if action not in ("post_add", "post_remove"):
        return

    print(f"sync permissions on role={instance}, action={action}")

    instance.sync_permissions()


@receiver(m2m_changed, sender=Group.permissions.through)
def sync_permissions_when_permissions_change(
    sender, instance: "Group", action, reverse, **kwargs
):
    """
    When the groups in a role change, update the permissions in the role itself
    """
    if action not in ("post_add", "post_remove"):
        return

    for role in Role.objects.filter(groups__in=[instance]):
        print(
            f"sync permissions on role={role}, includes group={instance}, action={action}"
        )
        role.sync_permissions()
