from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        ("a", Parser.digit(), Failure),
        ("1a", Parser.digit(), Success("1", "a")),
        ("1a", Parser.digit_nonzero(), Success("1", "a")),
        ("0a", Parser.digit(), Success("0", "a")),
        ("0a", Parser.digit_nonzero(), Failure),
    ],
)
def test_char(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
