import typing

from django.db.models.base import ModelBase

if typing.TYPE_CHECKING:
    from datetime import date

ModelType = typing.Type[ModelBase]
OptionalDate = typing.Optional["date"]
StringDict = typing.Dict[str, str]
StringList = typing.Iterable[str]
StringOrList = typing.Union[str, list]
UUIDString = str

JSON = typing.Union[
    typing.Dict[str, "JSON"], typing.List["JSON"], str, int, float, bool, None
]
