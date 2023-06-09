import datetime
import importlib
import os
import typing

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from baseline.types import ModelType, StringList

if typing.TYPE_CHECKING:
    from django.contrib.auth.models import Permission

Any = typing.Any
List = typing.List
PermissionList = typing.Iterable["Permission"]

EPOCH = datetime.datetime(1, 1, 1, 1, 1, 1)


class Chunker:
    """
    Iterator to split a given list into `chunk_size` chunks
    """

    def __init__(self, items: List[Any], chunk_size: int):
        self.chunk_size = chunk_size
        self.items = items
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        chunk, self.items = self.items[: self.chunk_size], self.items[self.chunk_size :]
        if not chunk:
            raise StopIteration()

        return chunk


def change_group_permissions(
    group_name: str,
    operation: str,
    permissions: PermissionList,
    group_cls: ModelType = Group,
    db_alias: str = "default",
) -> None:
    """
    Adds or removes the given permissions on the specified group
    Args:
        group_name: the name of the group to perform the operation on
        operation: "add" to add groups, "remove" to remove them
        permissions: the list of permissions to change
        group_cls: the group model class to use, by default use the direct import
        db_alias: the database alias to use
    """
    group = group_cls.objects.using(db_alias).get(name=group_name)

    operation_fn = getattr(group.permissions, operation)
    operation_fn(*permissions)


def get_permissions(
    app_name: str,
    model_name: str,
    permissions_verbs: StringList,
    content_type_cls: ModelType = ContentType,
    db_alias: str = "default",
) -> PermissionList:
    """
    Returns permission objects for the verbs provided for the given content type model

    Args:
        app_name:
        model_name:
        permissions_verbs:
        content_type_cls: the ContentType class to use to make the query; by default use the direct import
        db_alias: the database to use

    Returns:
        a list of permission objects
    """
    try:
        content_type = content_type_cls.objects.using(db_alias).get(
            app_label=app_name, model=model_name
        )
    except:
        print(
            f"unable to get content type from content_type_cls={content_type_cls}, db_alias={db_alias}, app_name={app_name}, model={model_name}"
        )

        raise

    content_type_queryset = content_type.permission_set.using(db_alias)

    permissions = []
    if "all" in permissions_verbs:
        permissions.extend(content_type_queryset.all())
    else:
        for verb in permissions_verbs:
            prefix = f"{verb}_"
            permissions.append(
                # get each permission in order to catch if one of the given verbs is
                # not in the db
                content_type_queryset.get(codename__startswith=prefix)
            )

    return permissions


def get_package_items(package_path: str, package_name: str, base: typing.Type):
    """
    Get the items in the given package path that match the requested type

    For example, the following code in <app>/views/__init__.py imports GenericViewSet subclasses from modules into
    the package:

    ```
    __locals = locals()
    for item in get_package_items(__file__, __name__, GenericViewSet):
        __locals[item.__name__] = item
    ```

    Args:
        package_path: the package's location on disk, i.e. __file__
        package_name: the package name, i.e. __name__
        base: the types of items to return
    """
    items = set()

    for filename in os.listdir(os.path.dirname(package_path)):
        # ignore files that start with underscores
        if filename.startswith("__"):
            continue

        module_name, _ = os.path.splitext(filename)
        full_name = f"{package_name}.{module_name}"
        _module = importlib.import_module(full_name)
        for attr_name in dir(_module):
            # ignore items that start with underscores
            if attr_name.startswith("__"):
                continue

            attr = getattr(_module, attr_name)

            try:
                if not issubclass(attr, base):
                    continue
            except TypeError:
                try:
                    if not isinstance(attr, base):
                        continue
                except TypeError:
                    continue

            # do not yield the same item more than once
            if attr in items:
                continue

            items.add(attr)

            yield attr


def get_user_serializer():
    module_name, class_name = settings.BASELINE_USER_SERIALIZER.rsplit(".", 1)

    module = importlib.import_module(module_name)

    return getattr(module, class_name)


def set_cookie(
    response,
    key,
    value,
    max_age=None,
    expires=None,
    domain=None,
    path=None,
    secure=True,
    httponly=True,
    samesite="None",
):
    domain = domain or settings.SESSION_COOKIE_DOMAIN
    path = path or settings.SESSION_COOKIE_PATH

    if not expires:
        expires = timezone.now() + datetime.timedelta(
            seconds=settings.SESSION_COOKIE_AGE
        )

    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=domain,
        path=path,
        secure=secure,
        httponly=httponly,
        samesite=samesite,
    )
