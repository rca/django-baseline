import typing

from json import load, loads

from rest_framework.renderers import JSONRenderer


def dumps(obj: typing.Any, as_str=True, **kwargs) -> typing.Union[str, bytes]:
    """
    Helper around JSONRenderer that handles things like dates

    Args:
        obj: the thing to serialize
        as_str: whether to return a string or bytes
        kwargs: additional options to pass to the renderer
    """
    dumped = JSONRenderer().render(obj, renderer_context=kwargs)

    if as_str:
        dumped = dumped.decode()

    return dumped
