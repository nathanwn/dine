from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        ("a", Parser.just("a"), Success("a", "a")),
        ("abc", Parser.just("a"), Success("a", "abc")),
        ("1a", Parser.just("hi"), Success("hi", "1a")),
        ("", Parser.just("hi"), Success("hi", "")),
    ],
)
def test_just(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
