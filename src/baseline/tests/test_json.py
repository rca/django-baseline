import datetime

from baseline import json


def test_dump_fancy_types():
    """
    see that this can serialize dates
    """
    stuff = {"today": datetime.date(2023, 6, 8)}

    content = json.dumps(stuff)

    assert content == '{"today":"2023-06-08"}'


def test_dump_fancy_types_as_bytes():
    """
    see that this can serialize dates
    """
    stuff = {"today": datetime.date(2023, 6, 8)}

    content = json.dumps(stuff, as_str=False)

    assert content == b'{"today":"2023-06-08"}'


def test_dump_fancy_types_indented():
    """
    see that this can serialize dates
    """
    stuff = {"today": datetime.date(2023, 6, 8)}

    content = json.dumps(stuff, indent=4)

    assert content == '{\n    "today": "2023-06-08"\n}'
