from rest_framework import permissions


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    Permission class that also enforces get calls for listing objects and getting object details
    """

    perms_map = permissions.DjangoModelPermissions.perms_map.copy()
    perms_map.update({"GET": ["%(app_label)s.view_%(model_name)s"]})
