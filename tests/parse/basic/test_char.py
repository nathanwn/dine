from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        ("a", Parser.char("a"), Success("a", "")),
        ("abc", Parser.char("a"), Success("a", "bc")),
        ("1a", Parser.char("1"), Success("1", "a")),
    ],
)
def test_char(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
