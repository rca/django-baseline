import inspect
import json
import os
import typing

List = typing.List


def get_content(
    path: str, mode: str = "r", parent_path: str = None, _stack_depth: int = 1
) -> str:
    """
    Returns the content of the file at the given path

    Args:
        path: path relative to the caller
        mode: the mode of the file to return the contents of
        _stack_depth: how far into the stack to inspect to determine the parent directory

    Returns:
        the file's content
    """
    if not parent_path:
        stack = inspect.stack()
        parent_frame = stack[_stack_depth]
        parent_filename = parent_frame.filename
        parent_path = os.path.dirname(parent_filename)

    content_path = os.path.join(parent_path, "files", path)

    return open(content_path, mode=mode).read()


def get_data(path: str) -> dict:
    """
    Returns JSON data from the given path

    Args:
        path: location of the test file

    Returns:
        a data dictionary from the JSON file
    """
    content = get_content(path, _stack_depth=2)

    return json.loads(content)


def get_lines(path: str) -> List[str]:
    """
    Returns the contents of the given path as a list of lines
    Args:
        path: path relative to the caller

    Returns:
        a list of strings
    """
    return get_content(path, _stack_depth=2).splitlines(keepends=False)
