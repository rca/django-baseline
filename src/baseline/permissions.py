from rest_framework import permissions


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    Permission class that also enforces get calls for listing objects and getting object details
    """

    perms_map = permissions.DjangoModelPermissions.perms_map.copy()
    perms_map.update({"GET": ["%(app_label)s.view_%(model_name)s"]})

    def has_permission(self, request, view):
        # when there is no queryset in the view, bail
        try:
            model_cls = view.queryset.model
        except AttributeError:
            return

        kwargs = {
            "action": view.action,
            "app_label": model_cls._meta.app_label,
            "model_name": model_cls._meta.model_name,
        }

        perms = ["{app_label}.{action}_{model_name}".format(**kwargs)]

        has_perms = request.user.has_perms(perms)
        if not has_perms:
            return super().has_permission(request, view)

        return has_perms
