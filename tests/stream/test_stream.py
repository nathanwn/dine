from typing import Tuple

import pytest

from dine.stream import Location, Stream


@pytest.mark.parametrize(
    "input_text, loc_list",
    [
        ("a\nb\nc\n", [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)]),
        (
            "\n\n\nabcde\n",
            [(1, 1), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6)],
        ),
    ],
)
def test_stream(input_text: str, loc_list: list[Tuple[int, int]]):
    s = Stream(input_text)
    assert len(s.loc) == len(loc_list)
    for i in range(len(loc_list)):
        assert s.loc[i] == Location(*loc_list[i])


def test_stream_eq():
    assert Stream("hello") == "hello"
    assert Stream("hello") != "hi"
    assert Stream("42") != 42
