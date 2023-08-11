import typing

from django.db.models.base import ModelBase

if typing.TYPE_CHECKING:
    from datetime import date

ModelType = typing.Type[ModelBase]
OptionalDate = typing.Optional["date"]
StringList = typing.Iterable[str]
UUIDString = str
