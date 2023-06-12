import typing

from django.db.models.base import ModelBase

ModelType = typing.Type[ModelBase]
StringList = typing.Iterable[str]
UUIDString = str
